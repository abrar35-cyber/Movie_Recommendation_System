"""
Build the lightweight recommendation artifacts used by the API.

Input : data/source/movies.pkl   (columns: movie_id, title, tags, title_clean)
Output: data/movies.json         (id + title per movie)
        data/neighbors.json      (top-K most similar movies for every movie)

Why: instead of shipping a huge N x N similarity matrix (~180 MB), we keep only
the top-K neighbours per movie (~1-2 MB). The API then needs no scikit-learn,
no pandas and no pickle at runtime.

Run from the backend/ folder:
    pip install -r requirements-dev.txt
    python scripts/build_model.py
"""

import json
import pickle
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE = BASE_DIR / "data" / "source" / "movies.pkl"
MOVIES_OUT = BASE_DIR / "data" / "movies.json"
NEIGHBORS_OUT = BASE_DIR / "data" / "neighbors.json"

TOP_K = 20
MAX_FEATURES = 5000


def main() -> None:
    with open(SOURCE, "rb") as f:
        movies = pickle.load(f)

    movies = movies.dropna(subset=["title", "tags"]).reset_index(drop=True)
    print(f"Loaded {len(movies)} movies")

    vectorizer = CountVectorizer(max_features=MAX_FEATURES, stop_words="english")
    vectors = vectorizer.fit_transform(movies["tags"])
    print(f"Vector matrix: {vectors.shape}")

    similarity = cosine_similarity(vectors).astype(np.float32)
    np.fill_diagonal(similarity, -1.0)  # a movie is never its own neighbour

    neighbors = []
    for row in similarity:
        top = np.argpartition(row, -TOP_K)[-TOP_K:]
        top = top[np.argsort(row[top])[::-1]]
        neighbors.append([[int(i), round(float(row[i]), 4)] for i in top])

    movies_out = [
        {"movie_id": int(r.movie_id), "title": str(r.title)}
        for r in movies.itertuples(index=False)
    ]

    MOVIES_OUT.write_text(json.dumps(movies_out, ensure_ascii=False), encoding="utf-8")
    NEIGHBORS_OUT.write_text(json.dumps(neighbors), encoding="utf-8")

    print(f"Wrote {MOVIES_OUT.name}    ({MOVIES_OUT.stat().st_size / 1e6:.2f} MB)")
    print(f"Wrote {NEIGHBORS_OUT.name} ({NEIGHBORS_OUT.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
