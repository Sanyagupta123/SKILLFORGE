import joblib

from sklearn.ensemble import RandomForestClassifier

from app.config import MODEL_PATH


def test_model_file_exists() -> None:
    assert MODEL_PATH.exists()


def test_model_can_be_loaded() -> None:
    model = joblib.load(MODEL_PATH)
    assert isinstance(model, RandomForestClassifier)


def test_model_can_predict() -> None:
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([[5.1, 3.5, 1.4, 0.2]])
    assert prediction[0] in {0, 1, 2}


def test_probability_output_is_available() -> None:
    model = joblib.load(MODEL_PATH)
    probabilities = model.predict_proba([[5.1, 3.5, 1.4, 0.2]])
    assert probabilities.shape == (1, 3)
    assert probabilities[0].sum() > 0.99
