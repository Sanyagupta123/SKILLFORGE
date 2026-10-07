from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "SkillForge"


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_endpoint() -> None:
    payload = {
        "job_description": "Looking for a Python developer with FastAPI, PostgreSQL, Docker, AWS and machine learning experience.",
        "resume": "B.Tech student with experience in Python, FastAPI, PostgreSQL, REST APIs and Machine Learning. Built backend applications using Python and FastAPI.",
    }

    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["score"] > 0
    assert "Python" in data["matched"]
    assert "FastAPI" in data["matched"]
    assert "PostgreSQL" in data["matched"]
    assert "Machine Learning" in data["matched"]
    assert "Docker" in data["missing"]
    assert "AWS" in data["missing"]


def test_analyse_history_endpoint() -> None:
    response = client.get("/analyses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
