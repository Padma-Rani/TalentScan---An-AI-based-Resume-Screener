"""
app/qualification/qualification_matcher.py

Compares candidate experience/education against job requirements.

Experience: numeric comparison in months (deterministic).
Education: intelligent matching using semantic similarity between the
job's education requirement and the candidate's degree/field/
institution entries - NOT an exact-string comparison. This is what
lets "BS Computer Science, University of Georgia" satisfy a
requirement phrased as "Bachelor's degree in Computer Science or a
related field".
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.ai.model_manager import ModelManager
from app.core.config import MATCHING_CONFIG, SCORING_CONFIG
from app.core.similarity import cosine_similarity


class QualificationMatcher:
    def __init__(self, model_manager: Optional[ModelManager] = None) -> None:
        self.model_manager = model_manager or ModelManager.get_instance()

    def match_experience(self, required_months: int, candidate_months: int) -> Dict[str, Any]:
        if required_months <= 0:
            return {
                "required_months": required_months,
                "candidate_months": candidate_months,
                "matched": True,
                "score": 100.0,
            }

        matched = candidate_months >= required_months
        score = min(100.0, round((candidate_months / required_months) * 100, 2))
        return {
            "required_months": required_months,
            "candidate_months": candidate_months,
            "matched": matched,
            "score": score,
        }

    def match_education(
        self,
        required_education: List[str],
        candidate_education: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        if not required_education:
            return {"matched": True, "score": 100.0, "best_match": None, "requirement": None}

        candidate_strings = []
        for entry in candidate_education:
            parts = [
                str(entry.get("degree", "")),
                str(entry.get("field", "")),
                str(entry.get("institution", "")),
            ]
            joined = " ".join(p for p in parts if p).strip()
            if joined:
                candidate_strings.append(joined)

        if not candidate_strings:
            return {
                "matched": False,
                "score": 0.0,
                "best_match": None,
                "requirement": required_education[0],
            }

        best_score = 0.0
        best_requirement = required_education[0]
        best_candidate = candidate_strings[0]

        for requirement in required_education:
            try:
                embeddings = self.model_manager.embed([requirement] + candidate_strings)
            except Exception as exc:
                print(f"[WARN] Education semantic matching unavailable: {exc}")
                continue

            requirement_vec = embeddings[0]
            for idx, candidate_text in enumerate(candidate_strings, start=1):
                score = cosine_similarity(requirement_vec, embeddings[idx])
                if score > best_score:
                    best_score = score
                    best_requirement = requirement
                    best_candidate = candidate_text

        matched = best_score >= MATCHING_CONFIG.SEMANTIC_MATCH_THRESHOLD
        return {
            "matched": matched,
            "score": round(best_score * 100, 2),
            "best_match": best_candidate,
            "requirement": best_requirement,
        }

    def qualification_score(
        self, experience_result: Dict[str, Any], education_result: Dict[str, Any]
    ) -> float:
        score = (
            experience_result["score"] * SCORING_CONFIG.EXPERIENCE_WEIGHT
            + education_result["score"] * SCORING_CONFIG.EDUCATION_WEIGHT
        )
        return round(score, 2)
