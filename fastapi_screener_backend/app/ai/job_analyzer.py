"""
app/ai/job_analyzer.py

Uses the LLM to dynamically extract structured requirements from
a job description: required skills, preferred skills, experience
(converted to months), education requirements, and responsibilities.

"""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from app.ai.model_manager import ModelManager
from app.core.json_utils import extract_json_object


JOB_SYSTEM_PROMPT = (
    "You are a precise job-description-parsing assistant. You extract "
    "ONLY information explicitly present in the job description. You "
    "always respond with a single valid JSON object and nothing else."
)


JOB_PROMPT_TEMPLATE = """Read the job description below and extract structured requirements.

Return ONLY a JSON object with exactly this shape:
{{
  "required_skills": [],
  "preferred_skills": [],
  "experience_years": 0,
  "education": [],
  "responsibilities": []
}}

Rules:
- "required_skills" and "preferred_skills" must contain ONLY individual technical technology names (e.g. "Java", "Spring Boot", "AWS") - never full sentences, job titles, education requirements, or experience statements.
- "required_skills" = technologies explicitly stated as required / must-have.
- "preferred_skills" = technologies explicitly stated as nice-to-have / preferred / a plus / bonus.
- If the description does not clearly separate required vs preferred, put clearly mandatory technologies in "required_skills" and anything explicitly marked optional in "preferred_skills".
- "experience_years" is a NUMBER of years of experience required (decimals allowed, e.g. 1.5 for 18 months). If no experience requirement is stated, use 0.
- "education" is a list of education requirement strings taken from the text (e.g. "Bachelor's degree in Computer Science or related field").
- "responsibilities" is a list of job responsibility strings.
- Respond with the JSON object only - no extra commentary.

JOB DESCRIPTION:
\"\"\"
{job_text}
\"\"\"
"""


def _empty_job_result() -> Dict[str, Any]:
    return {
        "required_skills": [],
        "preferred_skills": [],
        "experience_months": 0,
        "education": [],
        "responsibilities": [],
    }


class JobDescriptionAnalyzer:
    """Turns raw job description text into structured, validated JSON."""

    def __init__(self, model_manager: Optional[ModelManager] = None) -> None:
        self.model_manager = model_manager or ModelManager.get_instance()

    def analyze(self, job_text: str) -> Dict[str, Any]:
        if not job_text or not job_text.strip():
            print("[WARN] JobDescriptionAnalyzer received empty job description text.")
            return _empty_job_result()

        prompt = JOB_PROMPT_TEMPLATE.format(job_text=job_text.strip())
        raw_output = self.model_manager.generate(prompt, system_prompt=JOB_SYSTEM_PROMPT)

        parsed = extract_json_object(raw_output)
        if parsed is None:
            print(
                "[WARN] JobDescriptionAnalyzer: model output was not valid JSON. "
                "Falling back to an empty structured result.\n"
                f"Raw model output (truncated):\n{raw_output[:500]}"
            )
            return _empty_job_result()

        return self._validate_and_clean(parsed)

    def _validate_and_clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = _empty_job_result()

        for key in ("required_skills", "preferred_skills", "responsibilities"):
            value = data.get(key)
            if isinstance(value, list):
                result[key] = [str(item).strip() for item in value if str(item).strip()]

        education = data.get("education")
        if isinstance(education, list):
            result["education"] = [str(item).strip() for item in education if str(item).strip()]
        elif isinstance(education, str) and education.strip():
            result["education"] = [education.strip()]

        result["experience_months"] = self._years_to_months(data.get("experience_years", 0))

        # Safety net (not a skill database): strip anything that is
        # clearly a sentence, not a technology name, out of the skill
        # lists in case the model slips one in.
        result["required_skills"] = self._filter_sentence_like(result["required_skills"])
        result["preferred_skills"] = self._filter_sentence_like(result["preferred_skills"])

        return result

    @staticmethod
    def _years_to_months(value: Any) -> int:
        try:
            years = float(value)
        except (TypeError, ValueError):
            return 0
        return max(0, round(years * 12))

    @staticmethod
    def _filter_sentence_like(skills: List[str]) -> List[str]:
        """
        Removes obviously non-skill entries (long phrases, sentences
        mentioning experience/degree/etc.) that a model might mistakenly
        place in a skill list. This is a light safety net, not a skill
        dictionary - it never adds or renames technologies.
        """
        blocked_markers = ("experience", "degree", "years", "responsible for")
        cleaned = []
        for skill in skills:
            if len(skill.split()) > 5:
                continue
            if any(marker in skill.lower() for marker in blocked_markers):
                continue
            cleaned.append(skill)
        return cleaned


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    manager = ModelManager.get_instance()
    analyzer = JobDescriptionAnalyzer(manager)
    sample = "Required: Python, Django, PostgreSQL. 2 years experience. Bachelor's in CS."
    print(json.dumps(analyzer.analyze(sample), indent=2))
