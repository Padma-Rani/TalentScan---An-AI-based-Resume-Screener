"""
app/matching/matcher.py

DynamicAIMatcher compares job-required/preferred skills against a
candidate's extracted resume skills using a layered strategy:

    1. Exact match (case/whitespace-normalized)
    2. Alias match (small, explicit equivalence table - e.g. "JS" <-> "JavaScript")
    3. Semantic match (sentence-transformer embeddings, conservative threshold)

It deliberately avoids treating moderately-similar-but-different
technologies as matches - e.g. "Spring Boot" must NOT match "Java",
"SQL" must NOT match "Java", "Docker" must NOT match "AWS".
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from app.ai.model_manager import ModelManager
from app.core.config import MATCHING_CONFIG
from app.core.similarity import cosine_similarity


# A small, explicit table of alternate NAMES for the SAME technology.
# This is NOT a skill database - it never asserts that two different
# technologies are interchangeable, only that these strings refer to
# one and the same thing.
KNOWN_ALIASES: Dict[str, set] = {
    "javascript": {"js"},
    "typescript": {"ts"},
    "kubernetes": {"k8s"},
    "postgresql": {"postgres"},
    "amazon web services": {"aws"},
    "microsoft azure": {"azure"},
    "google cloud platform": {"gcp", "google cloud"},
    "node.js": {"nodejs", "node"},
    "vue.js": {"vuejs", "vue"},
    "c#": {"csharp", "c sharp"},
    "c++": {"cpp", "c plus plus"},
}


def _normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[\s\-_]+", " ", text)
    text = re.sub(r"[^\w\s#+.]", "", text)
    return text.strip()


def _canonical_alias(normalized: str) -> str:
    for canonical, aliases in KNOWN_ALIASES.items():
        if normalized == canonical or normalized in aliases:
            return canonical
    return normalized


class DynamicAIMatcher:
    """Matches job skills against resume skills with false-positive avoidance."""

    def __init__(self, model_manager: Optional[ModelManager] = None) -> None:
        self.model_manager = model_manager or ModelManager.get_instance()

    def match_skill_list(
        self, target_skills: List[str], resume_skills: List[str]
    ) -> List[Dict[str, Any]]:
        return [self.match_single_skill(skill, resume_skills) for skill in target_skills]

    def match_single_skill(self, target_skill: str, resume_skills: List[str]) -> Dict[str, Any]:
        target_norm = _normalize(target_skill)
        target_canonical = _canonical_alias(target_norm)

        for resume_skill in resume_skills:
            resume_norm = _normalize(resume_skill)
            resume_canonical = _canonical_alias(resume_norm)

            if target_norm == resume_norm:
                return self._result(target_skill, resume_skill, 1.0, "exact")

            if target_canonical == resume_canonical:
                return self._result(target_skill, resume_skill, 0.97, "normalized")

        if resume_skills:
            semantic_result = self._semantic_match(target_skill, resume_skills)
            if semantic_result is not None:
                return semantic_result

        return self._result(target_skill, None, 0.0, "no_match", matched=False)

    def _semantic_match(self, target_skill: str, resume_skills: List[str]) -> Optional[Dict[str, Any]]:
        try:
            embeddings = self.model_manager.embed([target_skill] + resume_skills)
        except Exception as exc:
            print(f"[WARN] Semantic matching unavailable ({exc}); skipping for '{target_skill}'.")
            return None

        target_vec = embeddings[0]
        best_score = -1.0
        best_skill = None

        for idx, resume_skill in enumerate(resume_skills, start=1):
            score = cosine_similarity(target_vec, embeddings[idx])
            if score > best_score:
                best_score = score
                best_skill = resume_skill

        if best_score >= MATCHING_CONFIG.SEMANTIC_MATCH_THRESHOLD:
            return self._result(target_skill, best_skill, round(float(best_score), 2), "semantic")

        if best_skill is not None:
            # Report the closest candidate transparently, but do NOT
            # count it as a match - this is how "Spring Boot" vs "Java"
            # or "Docker" vs "AWS" stays a documented non-match instead
            # of a silent false positive.
            return self._result(
                target_skill, None, round(float(best_score), 2), "no_match", matched=False
            )
        return None

    @staticmethod
    def _result(
        required_skill: str,
        matched_skill: Optional[str],
        score: float,
        match_type: str,
        matched: bool = True,
    ) -> Dict[str, Any]:
        return {
            "required_skill": required_skill,
            "matched_skill": matched_skill,
            "score": score,
            "match_type": match_type,
            "matched": bool(matched and matched_skill is not None),
        }

    @staticmethod
    def score_skill_matches(match_results: List[Dict[str, Any]]) -> float:
        """Percentage (0-100) of the given skill list that was matched."""
        if not match_results:
            return 100.0  # Nothing was required, so nothing is missing.
        matched_count = sum(1 for r in match_results if r["matched"])
        return round((matched_count / len(match_results)) * 100, 2)
