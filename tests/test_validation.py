from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_missing_field_is_rejected() -> None:
    response = client.post("/analyze", json={"resume": "Python, FastAPI"})
    assert response.status_code == 422


def test_wrong_type_is_rejected() -> None:
    response = client.post("/analyze", json={"job_description": 123, "resume": "Python"})
    assert response.status_code == 422


def test_empty_body_is_rejected() -> None:
    response = client.post("/analyze", content="")
    assert response.status_code == 422


def test_empty_job_and_resume_are_rejected() -> None:
    response = client.post("/analyze", json={"job_description": "", "resume": ""})
    assert response.status_code == 422
