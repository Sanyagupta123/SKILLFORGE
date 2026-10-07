from app.database import AnalysisDatabase


def test_database_can_store_analysis() -> None:
    db = AnalysisDatabase(database_path="/tmp/skillforge_test.db")
    analysis_id = db.create_analysis(
        job_description="Looking for a Python developer with FastAPI and Docker.",
        resume_text="I know Python, FastAPI, and Git.",
        match_score=75.0,
        matched_skills=["Python", "FastAPI"],
        missing_skills=["Docker"],
    )
    record = db.get_analysis(analysis_id)
    assert record is not None
    assert record["match_score"] == 75.0
    assert record["matched_skills"] == ["Python", "FastAPI"]
    assert record["missing_skills"] == ["Docker"]
