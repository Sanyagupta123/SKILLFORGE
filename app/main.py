from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.analyzer import (
    calculate_category_coverage,
    calculate_matching,
    extract_skills,
    generate_recommendations,
)
from app.config import APP_NAME, APP_VERSION, CORS_ORIGINS
from app.database import AnalysisDatabase
from app.schemas import (
    AnalysisHistoryItem,
    AnalysisRequest,
    AnalysisResponse,
    HealthResponse,
    SkillRecommendation,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.db = AnalysisDatabase()
    yield


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db() -> AnalysisDatabase:
    if not hasattr(app.state, "db"):
        app.state.db = AnalysisDatabase()
    return app.state.db


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(service=APP_NAME, status="ok", version=APP_VERSION)


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(payload: AnalysisRequest) -> AnalysisResponse:
    job_description = payload.job_description.strip()
    resume_text = payload.resume.strip()

    if not job_description:
        raise HTTPException(status_code=422, detail="Please provide a job description.")
    if not resume_text:
        raise HTTPException(status_code=422, detail="Please provide a resume.")

    job_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)
    comparison = calculate_matching(job_skills, resume_skills)
    categories = calculate_category_coverage(job_skills, comparison["matched"])
    recommendations = generate_recommendations(comparison["missing"])

    analysis_id = get_db().create_analysis(
        job_description=job_description,
        resume_text=resume_text,
        match_score=float(comparison["score"]),
        matched_skills=list(comparison["matched"]),
        missing_skills=list(comparison["missing"]),
    )

    return AnalysisResponse(
        id=analysis_id,
        score=float(comparison["score"]),
        matched=list(comparison["matched"]),
        missing=list(comparison["missing"]),
        categories=categories,
        recommendations=[SkillRecommendation(**item) for item in recommendations],
        job_skills=job_skills,
        resume_skills=resume_skills,
    )


@app.get("/analyses", response_model=list[AnalysisHistoryItem])
def list_analyses() -> list[AnalysisHistoryItem]:
    analyses = get_db().list_analyses()
    return [AnalysisHistoryItem(**analysis) for analysis in analyses]


@app.get("/analyses/{analysis_id}", response_model=AnalysisHistoryItem)
def get_analysis(analysis_id: int) -> AnalysisHistoryItem:
    analysis = get_db().get_analysis(analysis_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return AnalysisHistoryItem(**analysis)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": APP_NAME, "status": "running", "version": APP_VERSION}
