"""
app/screening/screening_engine.py

Connects every module into a single end-to-end screening pipeline:

    Resume file -> ResumeParser -> resume text
    resume text -> ResumeAnalyzer -> structured resume
    job text -> JobDescriptionAnalyzer -> structured job requirements
    structured resume + job -> DynamicAIMatcher -> skill matches
    structured resume + job -> QualificationMatcher -> qualification result
    everything -> final, explainable screening result
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from app.ai.job_analyzer import JobDescriptionAnalyzer
from app.ai.model_manager import ModelManager
from app.ai.resume_analyzer import ResumeAnalyzer
from app.core.config import SCORING_CONFIG
from app.extraction.resume_parser import ResumeParser, ResumeParserError
from app.matching.matcher import DynamicAIMatcher
from app.qualification.experience_calculator import calculate_total_experience_months
from app.qualification.qualification_matcher import QualificationMatcher


class ScreeningEngine:
    """Single orchestration point for the full resume-screening workflow."""

    def __init__(self) -> None:
        # The shared model is loaded exactly once here and reused by
        # every sub-component - no module loads its own copy.
        self.model_manager = ModelManager.get_instance()
        self.resume_parser = ResumeParser()
        self.resume_analyzer = ResumeAnalyzer(self.model_manager)
        self.job_analyzer = JobDescriptionAnalyzer(self.model_manager)
        self.matcher = DynamicAIMatcher(self.model_manager)
        self.qualification_matcher = QualificationMatcher(self.model_manager)

    def screen_resume_file(self, resume_path: str, job_description_text: str) -> Dict[str, Any]:
        print("Extracting resume text...")
        try:
            resume_text = self.resume_parser.parse(resume_path)
        except ResumeParserError as exc:
            return self._error_result(f"Resume extraction failed: {exc}")

        return self.screen_resume_text(resume_text, job_description_text)

    def screen_resume_text(self, resume_text: str, job_description_text: str) -> Dict[str, Any]:
        print("Analyzing resume...")
        structured_resume = self.resume_analyzer.analyze(resume_text)

        print("Analyzing job description...")
        structured_job = self.job_analyzer.analyze(job_description_text)

        resume_skills = self.resume_analyzer.flat_skills(structured_resume)

        print("Running semantic matching...")
        required_matches = self.matcher.match_skill_list(
            structured_job["required_skills"], resume_skills
        )
        preferred_matches = self.matcher.match_skill_list(
            structured_job["preferred_skills"], resume_skills
        )

        required_score = self.matcher.score_skill_matches(required_matches)
        preferred_score = self.matcher.score_skill_matches(preferred_matches)
        skill_score = round(
            required_score * SCORING_CONFIG.REQUIRED_SKILL_WEIGHT
            + preferred_score * SCORING_CONFIG.PREFERRED_SKILL_WEIGHT,
            2,
        )

        candidate_months = calculate_total_experience_months(structured_resume["experience"])
        experience_result = self.qualification_matcher.match_experience(
            structured_job["experience_months"], candidate_months
        )
        education_result = self.qualification_matcher.match_education(
            structured_job["education"], structured_resume["education"]
        )
        qualification_score = self.qualification_matcher.qualification_score(
            experience_result, education_result
        )

        final_score = round(
            skill_score * SCORING_CONFIG.SKILL_SCORE_WEIGHT
            + qualification_score * SCORING_CONFIG.QUALIFICATION_SCORE_WEIGHT,
            2,
        )

        matched_required = [m["required_skill"] for m in required_matches if m["matched"]]
        missing_required = [m["required_skill"] for m in required_matches if not m["matched"]]
        matched_preferred = [m["required_skill"] for m in preferred_matches if m["matched"]]
        missing_preferred = [m["required_skill"] for m in preferred_matches if not m["matched"]]

        strengths, missing_areas, evidence = self._build_explanation(
            matched_required, missing_required, matched_preferred,
            experience_result, education_result,
        )
        recommendation = self._recommendation(final_score, missing_required)

        return {
            "candidate": {
                "summary": structured_resume.get("summary", ""),
                "skills": resume_skills,
                "experience": structured_resume.get("experience", []),
                "education": structured_resume.get("education", []),
                "projects": structured_resume.get("projects", []),
                "certifications": structured_resume.get("certifications", []),
            },
            "job_requirements": {
                "required_skills": structured_job["required_skills"],
                "preferred_skills": structured_job["preferred_skills"],
                "experience_months": structured_job["experience_months"],
                "education": structured_job["education"],
                "responsibilities": structured_job["responsibilities"],
            },
            "skill_matching": {
                "required_matches": required_matches,
                "preferred_matches": preferred_matches,
                "matched_required_skills": matched_required,
                "missing_required_skills": missing_required,
                "matched_preferred_skills": matched_preferred,
                "missing_preferred_skills": missing_preferred,
                "required_skill_score": required_score,
                "preferred_skill_score": preferred_score,
                "skill_score": skill_score,
            },
            "qualification": {
                "experience": experience_result,
                "education": education_result,
                "qualification_score": qualification_score,
            },
            "final_score": final_score,
            "strengths": strengths,
            "missing_areas": missing_areas,
            "evidence": evidence,
            "recommendation": recommendation,
            "error": None,
        }

    def _build_explanation(
        self,
        matched_required: List[str],
        missing_required: List[str],
        matched_preferred: List[str],
        experience_result: Dict[str, Any],
        education_result: Dict[str, Any],
    ) -> Tuple[List[str], List[str], List[str]]:
        strengths: List[str] = []
        missing_areas: List[str] = []
        evidence: List[str] = []

        if matched_required:
            strengths.append(f"Matched required skills: {', '.join(matched_required)}")
            evidence.append(f"Resume demonstrates: {', '.join(matched_required)}")
        if matched_preferred:
            strengths.append(f"Matched preferred skills: {', '.join(matched_preferred)}")
        if missing_required:
            missing_areas.append(f"Missing required skills: {', '.join(missing_required)}")

        if experience_result["matched"]:
            strengths.append(
                f"Meets/exceeds required experience "
                f"({experience_result['candidate_months']} vs "
                f"{experience_result['required_months']} months required)."
            )
        else:
            missing_areas.append(
                f"Below required experience "
                f"({experience_result['candidate_months']} vs "
                f"{experience_result['required_months']} months required)."
            )

        if education_result["matched"] and education_result["best_match"]:
            strengths.append(f"Meets education requirement via: {education_result['best_match']}")
            evidence.append(f"Education on resume: {education_result['best_match']}")
        elif not education_result["matched"] and education_result["requirement"]:
            missing_areas.append(
                f"Does not clearly meet education requirement: {education_result['requirement']}"
            )

        return strengths, missing_areas, evidence

    def _recommendation(self, final_score: float, missing_required: List[str]) -> str:
        if final_score >= 80 and not missing_required:
            return "Strong match - recommend advancing to interview."
        if final_score >= 60:
            return "Moderate match - consider advancing with awareness of gaps."
        return "Weak match - significant gaps against job requirements."

    def _error_result(self, message: str) -> Dict[str, Any]:
        print(f"[ERROR] {message}")
        return {"error": message}
