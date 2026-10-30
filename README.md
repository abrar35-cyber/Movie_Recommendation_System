# 🎬 CineMatch: Movie Recommendation System

A full-stack, content-based movie recommender. Pick a movie and CineMatch returns similar titles with posters, ratings and a match percentage.

**Live demo:** _add your Vercel link here_ &nbsp;|&nbsp; **API docs:** _add your backend link_ + `/docs`

## How it works

```
 Next.js frontend  ──HTTP──▶  FastAPI backend  ──▶  neighbors.json (top-20 similar movies per movie)
   (Vercel)                     (Vercel)  └─▶  TMDB API (posters, rating, overview)
```

1. **Offline (once):** `scripts/build_model.py` turns each movie's `tags` (overview + genres + keywords + cast + director) into a bag-of-words vector (`CountVectorizer`, 5000 features), computes **cosine similarity**, and stores only the **top-20 neighbours** per movie (~1.5 MB instead of a ~180 MB matrix).
2. **Online:** the API looks up the selected movie, takes its neighbours, fetches poster/rating/overview from TMDB **concurrently**, and returns JSON.

## Tech stack

| Layer | Tools |
|---|---|
| Frontend | Next.js 16, React 19, Tailwind CSS 4 |
| Backend | Python, FastAPI, Uvicorn, Requests |
| ML | scikit-learn (CountVectorizer, cosine similarity), pandas, NumPy |
| Data | TMDB 5000 Movies & Credits (Kaggle) + TMDB API |
| Testing | pytest + FastAPI TestClient |

## Repository structure

```
Movie_Recommendation_System/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── requirements.txt        # runtime deps
│   ├── requirements-dev.txt    # + deps to rebuild the model & run tests
│   ├── .vercelignore
│   ├── .env.example
│   ├── data/
│   │   ├── movies.json         # id + title (served by API)
│   │   ├── neighbors.json      # top-20 neighbours per movie (served by API)
│   │   └── source/movies.pkl   # processed dataset used to rebuild the model
│   ├── scripts/build_model.py  # regenerates the two JSON files
│   └── tests/test_api.py
├── frontend/                   # Next.js app (app/, components/)
└── README.md
```

## Run locally

**Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate            # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env           # macOS/Linux: cp .env.example .env  -> add your TMDB key
uvicorn main:app --reload
```
API runs at http://127.0.0.1:8000 (interactive docs at `/docs`). Get a free TMDB key at https://www.themoviedb.org/settings/api. Without a key the API still works but returns no posters.

**Frontend**
```bash
cd frontend
npm install
copy .env.example .env.local     # macOS/Linux: cp .env.example .env.local
npm run dev
```
Open http://localhost:3000.

**Tests / rebuild the model**
```bash
cd backend
pip install -r requirements-dev.txt
pytest
python scripts/build_model.py
```

## API

| Endpoint | Description |
|---|---|
| `GET /api/health` | status + number of movies loaded |
| `GET /api/movies` | sorted list of all movie titles |
| `GET /api/recommend?title=Avatar&limit=10` | recommendations (`limit` 1-20), 404 if title unknown |

## Deployment (both on Vercel, free)

Two separate Vercel projects from the same GitHub repo:

1. **Backend:** root directory `backend`, env var `TMDB_API_KEY`. Vercel auto-detects FastAPI (`main.py` exposes `app`).
2. **Frontend:** root directory `frontend`, env var `NEXT_PUBLIC_API_URL` = backend URL (no trailing slash).

## Dataset

[TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) (Kaggle). Raw CSVs are not stored in this repo.

This product uses the TMDB API but is not endorsed or certified by TMDB.

## License

MIT
