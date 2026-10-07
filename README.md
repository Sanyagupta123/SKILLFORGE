# SkillForge

## Overview

SkillForge is a lightweight career intelligence platform that compares a job description against a candidate resume, extracts relevant skills, normalizes aliases, calculates a dynamic match score, surfaces missing skills, and recommends targeted learning next steps. The core product works without an LLM and uses deterministic rule-based analysis.

## Problem

Job seekers often struggle to understand the gap between a role they want and the skills they currently have. The data is fragmented across job descriptions and resumes, and it can be difficult to measure readiness without a structured comparison process.

## Solution

SkillForge extracts skills from both the job description and resume, normalizes common aliases such as ReactJS, Postgres, and JS, compares required vs. candidate skills, and calculates a score. It then surfaces matched and missing skills, category-level coverage, and deterministic learning recommendations.

## Features

- Job description and resume analysis
- Deterministic skill extraction and normalization
- Skill categorization across programming, backend, frontend, database, cloud, devops, and AI/ML
- Dynamic match scoring
- Matched and missing skill display
- Recommendation engine for missing skills
- Analysis history persistence in SQLite
- Light premium dashboard UI

## Demo

The app is designed to run locally as a FastAPI backend plus a Vite React frontend.

## Architecture

```text
Job description + resume
        ↓
Skill extraction
        ↓
Normalization and alias mapping
        ↓
Skill categorization
        ↓
Skill comparison
        ↓
Match score + missing skills
        ↓
Recommendations + SQLite history
        ↓
React dashboard
```

## Tech Stack

- Python
- FastAPI
- SQLite
- React
- Vite
- JavaScript
- CSS
- Pytest

## Skill Analysis Pipeline

1. Clean and normalize input text.
2. Detect known skills using alias-aware vocabulary matching.
3. Map each skill to a category.
4. Compare required vs. candidate skill sets.
5. Compute match score and skill gap.
6. Generate recommendations from missing skills.

## Match Score

The match score is computed as:

$$
\text{score} = \frac{\text{matched required skills}}{\text{total required skills}} \times 100
$$

## Skill Gap Analysis

The comparison engine returns both matched and missing skills and reports category-level coverage where relevant.

## Recommendation Engine

Deterministic recommendations are generated from a skill-to-guidance map. This allows the app to suggest practical learning topics without depending on a third-party model.

## Database

The MVP uses SQLite with an `analyses` table storing:

- `id`
- `job_description`
- `resume_text`
- `match_score`
- `matched_skills`
- `missing_skills`
- `created_at`

## API Endpoints

### GET /health
Returns service health information.

### POST /analyze
Accepts a job description and resume.

Example request:

```json
{
  "job_description": "Looking for a Python developer with FastAPI, PostgreSQL, Docker, AWS and machine learning experience.",
  "resume": "B.Tech student with experience in Python, FastAPI, PostgreSQL, REST APIs and Machine Learning."
}
```

### GET /analyses
Returns saved analysis history.

### GET /analyses/{id}
Returns a single saved analysis.

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
│   └── test_skillforge.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── skillforge.db
└── .venv/
```

## Installation

1. Create and activate a Python virtual environment.
2. Install backend requirements:

```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Environment Variables

Use the sample file `.env.example`:

```env
APP_NAME=SkillForge
APP_VERSION=1.0.0
DATABASE_PATH=./skillforge.db
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## Running Backend

```bash
.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Running Frontend

```bash
cd frontend
npm install
npm run dev
```

## Running Tests

```bash
.venv\Scripts\python -m pytest -q
```

## Docker

Docker is not required for the MVP and is intentionally left out to keep the setup lightweight and reproducible.

## Screenshots

The project includes a light SaaS dashboard with input panels and the analysis result layout.

## Limitations

- Skill extraction is dictionary/rule based for the MVP.
- Resume parsing depends on the supplied text content.
- The match score is derived from detected required skills.
- Recommendations are deterministic unless a future LLM layer is added.
- Authentication is intentionally not required for the MVP.

## Future Improvements

- Add resume upload parsing and richer text extraction
- Add a user-friendly history detail view
- Expand the skill taxonomy
- Add optional LLM-powered personalized recommendations
- Add deployment configuration for cloud hosting

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

