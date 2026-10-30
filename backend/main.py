"""CineMatch API: content-based movie recommendations enriched with TMDB data."""

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("cinematch")

# ---------------------------------------------------------------- config ----
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "").strip()
TMDB_API_URL = "https://api.themoviedb.org/3/movie"
POSTER_BASE = "https://image.tmdb.org/t/p/w500"
BACKDROP_BASE = "https://image.tmdb.org/t/p/original"

# Comma-separated list, e.g. "https://cinematch.vercel.app". Defaults to "*"
# (any site) because this is a public, read-only API with no cookies/logins.
ALLOWED_ORIGINS = [
    o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()
]

CACHE_LIMIT = 3000

if not TMDB_API_KEY:
    log.warning("TMDB_API_KEY is not set: recommendations will have no posters.")

# ------------------------------------------------------------------- app ----
app = FastAPI(
    title="CineMatch API",
    description="Content-based movie recommendation API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ------------------------------------------------------------ model data ----
with open(DATA_DIR / "movies.json", encoding="utf-8") as f:
    MOVIES = json.load(f)

with open(DATA_DIR / "neighbors.json", encoding="utf-8") as f:
    NEIGHBORS = json.load(f)

TITLE_TO_INDEX = {}
for idx, movie in enumerate(MOVIES):
    TITLE_TO_INDEX.setdefault(movie["title"].lower().strip(), idx)

SORTED_TITLES = sorted({m["title"] for m in MOVIES})
log.info("Loaded %d movies", len(MOVIES))

# ------------------------------------------------------------ TMDB layer ----
_tmdb_cache = {}
_session = requests.Session()
_executor = ThreadPoolExecutor(max_workers=10)


def fetch_tmdb(movie_id):
    """Return TMDB details for a movie, or None. Successful results are cached."""
    if not TMDB_API_KEY:
        return None
    if movie_id in _tmdb_cache:
        return _tmdb_cache[movie_id]
    try:
        resp = _session.get(
            f"{TMDB_API_URL}/{movie_id}",
            params={"api_key": TMDB_API_KEY, "language": "en-US"},
            timeout=8,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
    except (requests.RequestException, ValueError):
        return None

    if len(_tmdb_cache) >= CACHE_LIMIT:
        _tmdb_cache.pop(next(iter(_tmdb_cache)))  # drop oldest entry
    _tmdb_cache[movie_id] = data
    return data


def build_card(movie, score, details):
    details = details or {}
    poster = details.get("poster_path")
    backdrop = details.get("backdrop_path")
    release = details.get("release_date") or ""
    return {
        "movie_id": movie["movie_id"],
        "title": details.get("title") or movie["title"],
        "poster_url": POSTER_BASE + poster if poster else None,
        "backdrop_url": BACKDROP_BASE + backdrop if backdrop else None,
        "release_year": release[:4] or None,
        "rating": round(float(details.get("vote_average") or 0), 1),
        "match_percentage": round(float(score) * 100, 1),
        "overview": details.get("overview") or "",
    }


# ---------------------------------------------------------------- routes ----
@app.get("/")
def root():
    return {"message": "CineMatch API is running", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "movies_loaded": len(MOVIES),
        "tmdb_enabled": bool(TMDB_API_KEY),
    }


@app.get("/api/movies")
def list_movies():
    return {"movies": SORTED_TITLES}


@app.get("/api/recommend")
def recommend(title: str, limit: int = Query(10, ge=1, le=20)):
    index = TITLE_TO_INDEX.get(title.lower().strip())
    if index is None:
        raise HTTPException(status_code=404, detail=f"Movie '{title}' not found.")

    picks = NEIGHBORS[index][:limit]
    movies = [MOVIES[i] for i, _ in picks]
    details = list(_executor.map(lambda m: fetch_tmdb(m["movie_id"]), movies))

    return {
        "selected_movie": MOVIES[index]["title"],
        "recommendations": [
            build_card(m, score, d)
            for m, (_, score), d in zip(movies, picks, details)
        ],
    }
