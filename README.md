# ModelServe

> A machine-learning model serving API that trains, serializes, loads, and serves an Iris classification model through FastAPI.

ModelServe demonstrates the path from notebook experimentation to a production-style ML service. It trains a Random Forest classifier on the Iris dataset, saves the model with joblib, loads it on startup, and serves predictions through a clean FastAPI API.

## The difference between notebook ML and production ML serving

Notebook ML usually stops at a local model call such as `model.predict()` inside a notebook. That is useful for experimentation, but it does not create an accessible service for other applications.

Production-style ML serving adds several layers:

- Client request
- FastAPI API
- Input validation
- Model loading on startup
- ML inference
- JSON response

This project shows the full serving flow:

```text
Client
  ↓
FastAPI
  ↓
Validation
  ↓
Loaded ML Model
  ↓
Prediction
  ↓
JSON Response
```

## Core concepts

### Training
Training means learning patterns from data so the model can generalize to new inputs.

### Inference
Inference is the process of using a trained model to generate predictions for new data.

### Model serialization
Model serialization saves the trained model so it can be reused later instead of retraining it every time.

### Model serving
Model serving exposes the trained model through an API so other applications can request predictions.

## Architecture

```text
                 TRAINING
                    │
                    ▼
               IRIS DATASET
                    │
                    ▼
             RANDOM FOREST
                    │
                    ▼
              MODEL.JOBLIB
                    │
                    ▼
              FASTAPI SERVER
                    │
                    ▼
              POST /PREDICT
                    │
                    ▼
             INPUT VALIDATION
                    │
                    ▼
              ML INFERENCE
                    │
                    ▼
          PREDICTION + CONFIDENCE
```

## Project structure

```text
modelserve/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── model_service.py
│   └── schemas.py
├── ml/
│   ├── train.py
│   └── model.joblib
├── tests/
│   ├── test_api.py
│   ├── test_model.py
│   └── test_validation.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── .venv/
```

## Installation

```bash
git clone <repository-url>
cd modelserve

python -m venv venv
```

For Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python ml/train.py
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open the API documentation at:

```text
http://127.0.0.1:8000/docs
```

Open the dashboard at:

```text
http://127.0.0.1:8000/ui
```

## API endpoints

### GET /
Purpose: health check for the service.

Request: no body

Response:

```json
{
  "message": "ModelServe is running"
}
```

Possible errors: none in normal operation.

### POST /predict
Purpose: generate a single flower prediction.

Request:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Response:

```json
{
  "prediction": "setosa",
  "confidence": 0.98
}
```

Possible errors: malformed payload, validation errors, or missing model file.

### GET /model-info
Purpose: return metadata about the loaded model and dataset.

Response:

```json
{
  "model": "RandomForestClassifier",
  "dataset": "Iris",
  "features": 4,
  "classes": 3,
  "feature_names": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
  "class_names": ["setosa", "versicolor", "virginica"]
}
```

Possible errors: model not found or failed to load.

### POST /predict/batch
Purpose: run inference for multiple flower samples in one request.

Request:

```json
[
  {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  },
  {
    "sepal_length": 6.2,
    "sepal_width": 2.8,
    "petal_length": 4.8,
    "petal_width": 1.8
  }
]
```

Response:

```json
[
  {
    "prediction": "setosa",
    "confidence": 0.98
  },
  {
    "prediction": "virginica",
    "confidence": 0.91
  }
]
```

Possible errors: validation errors or empty batch.

## Testing

This project uses `pytest` to validate the API behavior and the model object itself.

Run tests with:

```bash
pytest
```

The automated tests cover:

- root endpoint status and response
- single prediction behavior
- batch prediction behavior
- model metadata endpoint
- validation failures for missing fields and bad payloads
- model file existence and prediction output

## README demo

### ModelServe Dashboard

Input
 ↓
Prediction
 ↓
Confidence

A light-themed dashboard is available at `/ui` and communicates with the API using real model results.

## Model limitations

This project uses the Iris dataset, which is small and educational. It is intended to demonstrate ML serving architecture rather than to perform real-world biological classification. Confidence values represent model probability, not certainty.

## Future upgrades

Possible next improvements include:

- model versioning
- a model registry
- Docker support
- cloud deployment
- authentication
- monitoring and logging
- Prometheus metrics
- multiple ML models
- CI/CD integration

## Final note

ModelServe is designed as a clean, portfolio-ready foundation for serving machine learning models through APIs.
