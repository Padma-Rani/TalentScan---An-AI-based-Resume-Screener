"""
app/api/schemas.py

Response shape for POST /api/analyze, matching Spring Boot's
AiAnalysisResult.java field-for-field (camelCase over the wire).
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AnalyzeResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    candidate_name: str = Field(alias="candidateName")
    match_score: float = Field(alias="matchScore")
    eligible: bool
    matched_skills: list[str] = Field(alias="matchedSkills")
    missing_skills: list[str] = Field(alias="missingSkills")
    summary: str
