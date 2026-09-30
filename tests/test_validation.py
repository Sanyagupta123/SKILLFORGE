from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_missing_field_is_rejected() -> None:
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_wrong_type_is_rejected() -> None:
    payload = {
        "sepal_length": "hello",
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_empty_body_is_rejected() -> None:
    response = client.post("/predict", content="")
    assert response.status_code == 422


def test_empty_batch_is_rejected() -> None:
    response = client.post("/predict/batch", json=[])
    assert response.status_code == 422
