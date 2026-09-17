from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import pandas as pd
import pickle
import requests
import os


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise RuntimeError(
        "TMDB_API_KEY is missing. Add it to backend/.env"
    )


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="CineMatch API",
    description="AI-powered movie recommendation API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# TMDB
# ============================================================

TMDB_API_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


# ============================================================
# LOAD ML DATA
# ============================================================

print("Loading movie recommendation model...")

with open("movies.pkl", "rb") as file:
    movies = pickle.load(file)

with open("similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

print(f"Loaded {len(movies)} movies successfully.")


# ============================================================
# MOVIE INDEX
# ============================================================

movie_indices = pd.Series(
    movies.index,
    index=movies["title_clean"]
).drop_duplicates()


# ============================================================
# TMDB CACHE
# ============================================================

tmdb_cache = {}


# ============================================================
# GET TMDB DETAILS
# ============================================================

def get_movie_details(movie_id):

    if movie_id in tmdb_cache:
        return tmdb_cache[movie_id]

    try:

        response = requests.get(
            f"{TMDB_API_URL}/{movie_id}",
            params={
                "api_key": TMDB_API_KEY,
                "language": "en-US"
            },
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        tmdb_cache[movie_id] = data

        return data

    except requests.RequestException:
        return None


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "CineMatch API is running",
        "version": "1.0.0"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "movies_loaded": len(movies)
    }


# ============================================================
# MOVIE SEARCH
# ============================================================

@app.get("/api/movies")
def get_movies():

    movie_list = sorted(
        movies["title"]
        .dropna()
        .unique()
        .tolist()
    )

    return {
        "movies": movie_list
    }


# ============================================================
# RECOMMENDATIONS
# ============================================================

@app.get("/api/recommend")
def recommend(
    title: str,
    limit: int = 10
):

    title_clean = title.lower().strip()

    if title_clean not in movie_indices:

        raise HTTPException(
            status_code=404,
            detail=f"Movie '{title}' not found."
        )

    movie_index = movie_indices[title_clean]

    similarity_scores = list(
        enumerate(similarity[movie_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove selected movie
    similarity_scores = similarity_scores[
        1:limit + 1
    ]

    recommendations = []

    for index, score in similarity_scores:

        movie = movies.iloc[index]

        movie_id = int(movie["movie_id"])

        details = get_movie_details(movie_id)

        # ----------------------------------------------------
        # DEFAULT VALUES
        # ----------------------------------------------------

        title_value = str(movie["title"])

        poster_url = None

        rating = 0

        release_year = None

        overview = ""

        backdrop_url = None

        # ----------------------------------------------------
        # TMDB DETAILS
        # ----------------------------------------------------

        if details:

            title_value = details.get(
                "title",
                title_value
            )

            poster_path = details.get(
                "poster_path"
            )

            backdrop_path = details.get(
                "backdrop_path"
            )

            rating = details.get(
                "vote_average",
                0
            )

            release_date = details.get(
                "release_date",
                ""
            )

            overview = details.get(
                "overview",
                ""
            )

            if release_date:
                release_year = release_date[:4]

            if poster_path:

                poster_url = (
                    TMDB_IMAGE_BASE +
                    poster_path
                )

            if backdrop_path:

                backdrop_url = (
                    "https://image.tmdb.org/t/p/original"
                    + backdrop_path
                )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        recommendations.append({

            "movie_id": movie_id,

            "title": title_value,

            "poster_url": poster_url,

            "backdrop_url": backdrop_url,

            "release_year": release_year,

            "rating": round(
                float(rating),
                1
            ),

            "match_percentage": round(
                float(score) * 100,
                1
            ),

            "overview": overview

        })

    return {
        "selected_movie": title,
        "recommendations": recommendations
    }