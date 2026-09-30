from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "ml" / "model.joblib"


def train_and_save_model() -> float:
    iris = load_iris()
    features, targets = iris.data, iris.target

    features_train, features_test, targets_train, targets_test = train_test_split(
        features,
        targets,
        test_size=0.2,
        random_state=42,
        stratify=targets,
    )

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(features_train, targets_train)

    prediction = model.predict(features_test)
    accuracy = accuracy_score(targets_test, prediction)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model accuracy: {accuracy * 100:.2f}%")
    print(f"Model saved successfully: {MODEL_PATH}")
    return accuracy


if __name__ == "__main__":
    train_and_save_model()
