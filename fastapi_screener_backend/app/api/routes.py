"""
app/api/routes.py

HTTP surface for the screening pipeline. Wraps ScreeningEngine so
Spring Boot's AiScreeningService (multipart POST /api/analyze) gets
back exactly the fields the React frontend renders.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.api.schemas import AnalyzeResponse
from app.extraction.resume_parser import SUPPORTED_EXTENSIONS
from app.screening.screening_engine import ScreeningEngine

router = APIRouter()

# Mirrors the "Moderate match" cutoff already used in
# ScreeningEngine._recommendation for a consistent eligible/not-eligible line.
ELIGIBILITY_SCORE_THRESHOLD = 60

_engine: ScreeningEngine | None = None


def get_engine() -> ScreeningEngine:
    global _engine
    if _engine is None:
        _engine = ScreeningEngine()
    return _engine


@router.post("/api/analyze", response_model=AnalyzeResponse, response_model_by_alias=True)
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalyzeResponse:
    extension = Path(resume.filename or "").suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type '{extension}'. "
            f"Supported types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
        )

    tmp_path = None
    try:
        contents = await resume.read()
        with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as tmp_file:
            tmp_file.write(contents)
            tmp_path = tmp_file.name

        result = get_engine().screen_resume_file(tmp_path, job_description)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    if result.get("error"):
        raise HTTPException(status_code=422, detail=result["error"])

    skill_matching = result["skill_matching"]

    return AnalyzeResponse(
        candidateName="",
        matchScore=result["final_score"],
        eligible=result["final_score"] >= ELIGIBILITY_SCORE_THRESHOLD,
        matchedSkills=skill_matching["matched_required_skills"] + skill_matching["matched_preferred_skills"],
        missingSkills=skill_matching["missing_required_skills"] + skill_matching["missing_preferred_skills"],
        summary=result["recommendation"],
    )
