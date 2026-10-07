# SkillForge

SkillForge is a deterministic job-to-resume intelligence platform that compares a role against a candidate profile, extracts relevant skills, normalizes aliases, calculates a match score, surfaces missing skills, and recommends next learning steps.

## Overview

The application is built to help job seekers evaluate how closely their experience aligns with a target role without relying on an LLM. It combines a rule-based skill extraction engine with a lightweight dashboard and persistent analysis history.

## Features

- Resume and job description analysis
- Alias-aware skill normalization
- Category-based skill matching for programming, backend, frontend, databases, cloud, and DevOps
- Match score calculation with matched and missing skill output
- Recommendation engine for missing skills
- SQLite-backed analysis history
- Responsive React dashboard
- FastAPI backend with validation

## Tech Stack

- Python
- FastAPI
- SQLite
- React
- Vite
- JavaScript
- CSS
- Pytest

## Architecture

```text
Job description + resume
        ↓
Skill extraction
        ↓
Alias normalization
        ↓
Skill categorization
        ↓
Required vs. candidate comparison
        ↓
Score + missing skills
        ↓
Recommendations + history
        ↓
React dashboard
```

## Match Score

The score is calculated as a ratio between matched required skills and total required skills:

$$
score = \frac{matched\ required\ skills}{total\ required\ skills} \times 100
$$

## API Endpoints

### GET /health
Returns the service status and version information.

### POST /analyze
Accepts JSON input with `job_description` and `resume` and returns the skill-gap analysis.

Example request:

```json
{
  "job_description": "Looking for a Python developer with FastAPI, PostgreSQL, Docker, AWS and machine learning experience.",
  "resume": "B.Tech student with experience in Python, FastAPI, PostgreSQL, REST APIs and Machine Learning."
}
```

### GET /analyses
Returns saved analysis entries.

### GET /analyses/{id}
Returns one saved analysis by ID.

## Project Structure

```text
modelserve/
├── app/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── schemas.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
├── tests/
│   ├── __init__.py
│   └── test_skillforge.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── skillforge.db
└── .venv/
```

## Local Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
```

## Run the App

### Backend

```bash
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

## Environment Variables

Use the sample file `.env.example`:

```env
APP_NAME=SkillForge
APP_VERSION=1.0.0
DATABASE_PATH=./skillforge.db
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Testing

```bash
.venv\Scripts\python -m pytest -q
```

## Notes

- This MVP intentionally uses deterministic rules instead of an LLM.
- SQLite is used for local persistence.
- The recommendation engine is intentionally explainable and lightweight.

## Future Improvements

- Resume upload and PDF parsing
- More advanced skill taxonomy expansion
- User authentication and saved profiles
- Deeper analytics and trend tracking
- Optional LLM-enhanced recommendation layer

├── .gitignore
├── README.md
├── requirements.txt
└── .venv/
```

## Installation

```bash
git clone <repository-url>
cd modelserve
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Training Pipeline

```bash
python ml/train.py
```

This trains the Random Forest model and saves `ml/model.joblib`.

## Running the API

```bash
uvicorn app.main:app --reload
```

Then open:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/ui

## Running Tests

```bash
pytest -q
```

## UI

The UI is a clean, light-themed dashboard with a prediction form, result section, model metadata, and accessibility-friendly controls. It submits requests to the backend and displays the predicted class and confidence.

## Model Serving Flow

```text
Client request
  ↓
FastAPI validation
  ↓
ModelService loads trained model once at startup
  ↓
Prediction generated using model.predict()
  ↓
Probability computed with model.predict_proba()
  ↓
JSON response returned to client
```

## Error Handling

The API handles malformed JSON, missing fields, wrong types, empty batches, missing model files, and runtime inference issues with clear 4xx/5xx responses. Internal stack traces are not exposed in the public API responses.

## Limitations

- This is a local, single-instance model serving example.
- The model state is local to the running API process.
- The model is trained on the Iris dataset for demonstration purposes.
- This project is designed for learning and portfolio use, not a distributed production inference platform.

## Future Improvements

- Docker containerization
- Redis and request queueing
- Model versioning
- Cloud deployment
- Authentication and authorization
- Monitoring and metrics
- Prometheus and Grafana
- CI/CD pipeline
- Model registry integration
- A/B model testing
- GPU-enabled inference

