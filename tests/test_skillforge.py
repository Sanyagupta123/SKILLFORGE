import pytest
from fastapi.testclient import TestClient

from app.analyzer import (
    analyze_text,
    calculate_matching,
    extract_skills,
    normalize_skill_name,
)
from app.main import app


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("python", "Python"),
        ("PYTHON", "Python"),
        (" Python ", "Python"),
        ("nodejs", "Node.js"),
        ("Postgres", "PostgreSQL"),
        ("ReactJS", "React"),
        ("JS", "JavaScript"),
        ("ML", "Machine Learning"),
    ],
)
def test_skill_normalization(raw: str, expected: str) -> None:
    assert normalize_skill_name(raw) == expected


def test_extract_known_skills() -> None:
    text = "Python, FastAPI, PostgreSQL, Docker, AWS, machine learning"
    skills = extract_skills(text)
    assert skills == [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Docker",
        "AWS",
        "Machine Learning",
    ]


def test_avoid_java_script_confusion() -> None:
    text = "Java and JavaScript"
    skills = extract_skills(text)
    assert "Java" in skills
    assert "JavaScript" in skills
    assert skills.count("Java") == 1
    assert skills.count("JavaScript") == 1


def test_compare_skills_and_score() -> None:
    result = calculate_matching(
        required=["python", "fastapi", "docker"],
        candidate=["python", "fastapi"],
    )
    assert result["matched"] == ["Python", "FastAPI"]
    assert result["missing"] == ["Docker"]
    assert abs(result["score"] - 66.67) < 0.01


def test_empty_input_is_handled() -> None:
    assert extract_skills("") == []
    assert analyze_text("") == []


client = TestClient(app)


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


def test_invalid_body_returns_validation_error() -> None:
    response = client.post("/analyze", json={"resume": "hello"})
    assert response.status_code == 422


def test_history_endpoint() -> None:
    response = client.get("/analyses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
