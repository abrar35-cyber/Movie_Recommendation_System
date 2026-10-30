import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402

client = TestClient(main.app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["movies_loaded"] > 4000


def test_movie_list_contains_avatar():
    r = client.get("/api/movies")
    assert "Avatar" in r.json()["movies"]


def test_recommend_returns_requested_limit(monkeypatch):
    monkeypatch.setattr(main, "fetch_tmdb", lambda movie_id: None)
    r = client.get("/api/recommend", params={"title": "The Dark Knight", "limit": 5})
    assert r.status_code == 200
    recs = r.json()["recommendations"]
    assert len(recs) == 5
    assert all(0 <= x["match_percentage"] <= 100 for x in recs)
    assert "The Dark Knight" not in [x["title"] for x in recs]


def test_recommend_is_case_insensitive(monkeypatch):
    monkeypatch.setattr(main, "fetch_tmdb", lambda movie_id: None)
    assert client.get("/api/recommend", params={"title": "avatar"}).status_code == 200


def test_unknown_movie_returns_404():
    assert client.get("/api/recommend", params={"title": "zzz not a movie"}).status_code == 404


def test_limit_validation():
    assert client.get("/api/recommend", params={"title": "Avatar", "limit": 99}).status_code == 422
