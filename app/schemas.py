from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class HealthResponse(BaseModel):
    service: str
    status: str
    version: str


class AnalysisRequest(BaseModel):
    job_description: str
    resume: str

    @field_validator("job_description", "resume")
    @classmethod
    def validate_required_text(cls, value: str, info) -> str:
        field_name = "job description" if info.field_name == "job_description" else "resume"
        if value is None or not str(value).strip():
            raise ValueError(f"Please provide a {field_name}.")
        return str(value).strip()


class SkillRecommendation(BaseModel):
    skill: str
    recommendations: list[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    id: int | None = None
    score: float
    matched: list[str] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)
    categories: dict[str, float] = Field(default_factory=dict)
    recommendations: list[SkillRecommendation] = Field(default_factory=list)
    job_skills: list[str] = Field(default_factory=list)
    resume_skills: list[str] = Field(default_factory=list)


class AnalysisHistoryItem(BaseModel):
    id: int
    job_description: str
    resume_text: str
    match_score: float
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    created_at: str
