from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "ModelServe is running"}


def test_predict_endpoint() -> None:
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert isinstance(data["confidence"], (int, float))
    assert data["prediction"] in {"setosa", "versicolor", "virginica"}


def test_model_info_endpoint() -> None:
    response = client.get("/model-info")
    assert response.status_code == 200

    data = response.json()
    assert data["model"] == "RandomForestClassifier"
    assert data["dataset"] == "Iris"
    assert data["features"] == 4
    assert data["classes"] == 3
    assert data["feature_names"] == [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
    ]


def test_batch_prediction_endpoint() -> None:
    payload = [
        {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
        {
            "sepal_length": 6.2,
            "sepal_width": 2.8,
            "petal_length": 4.8,
            "petal_width": 1.8,
        },
    ]

    response = client.post("/predict/batch", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(payload)

    for item in data:
        assert "prediction" in item
        assert "confidence" in item
        assert item["prediction"] in {"setosa", "versicolor", "virginica"}
        assert isinstance(item["confidence"], (int, float))
