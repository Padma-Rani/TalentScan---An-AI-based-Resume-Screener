"""
app/core/config.py

Centralized configuration for the AI Resume Screening System.

Every model name, matching threshold, and scoring weight used anywhere
in the project is defined here, ONCE. import it from here instead.
This is what makes "Required = 80%, Preferred = 20%" (and similar
numbers) configurable in one place rather than scattered across files.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    LLM_MODEL_NAME: str = "Qwen/Qwen2.5-1.5B-Instruct"
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MAX_NEW_TOKENS: int = 1024
    LLM_TEMPERATURE: float = 0.1


@dataclass(frozen=True)
class MatchingConfig:
    # Semantic similarity below this is never treated as a match.  
    # This is intentionally conservative to avoid false positives such
    # as "Spring Boot" <-> "Java" or "Docker" <-> "AWS".
    SEMANTIC_MATCH_THRESHOLD: float = 0.80


@dataclass(frozen=True)
class ScoringConfig:
    # Skill weighting (Section 13 of the spec).
    REQUIRED_SKILL_WEIGHT: float = 0.80
    PREFERRED_SKILL_WEIGHT: float = 0.20

    # Qualification sub-weighting (experience vs. education).
    EXPERIENCE_WEIGHT: float = 0.60
    EDUCATION_WEIGHT: float = 0.40

    # Final score = skills vs. qualifications.
    SKILL_SCORE_WEIGHT: float = 0.70
    QUALIFICATION_SCORE_WEIGHT: float = 0.30


MODEL_CONFIG = ModelConfig()
MATCHING_CONFIG = MatchingConfig()
SCORING_CONFIG = ScoringConfig()
