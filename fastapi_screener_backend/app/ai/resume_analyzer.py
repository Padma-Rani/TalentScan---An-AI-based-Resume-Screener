"""
app/ai/resume_analyzer.py

Uses the LLM to dynamically extract structured information from
resume text. The model reads the resume and reports the technologies, experience, education,
projects, certifications, and summary it actually finds.
"""
from __future__ import annotations

import copy
import json
from typing import Any, Dict, List, Optional

from app.ai.model_manager import ModelManager
from app.core.json_utils import extract_json_object


RESUME_SYSTEM_PROMPT = (
    "You are a precise resume-parsing assistant. You extract ONLY "
    "information that is explicitly present in the resume text. You "
    "never invent, guess, or add information that is not stated. You "
    "always respond with a single valid JSON object and nothing else - "
    "no markdown fences, no explanation, no extra text."
)


RESUME_PROMPT_TEMPLATE = """Read the resume text below and extract structured information.

Return ONLY a JSON object with exactly this shape:
{{
  "skills": {{
    "programming_languages": [],
    "frameworks_libraries": [],
    "databases": [],
    "apis": [],
    "cloud_technologies": [],
    "devops_tools": [],
    "development_tools": [],
    "other_technologies": []
  }},
  "experience": [
    {{
      "job_title": "",
      "company": "",
      "start_date": "",
      "end_date": "",
      "description": ""
    }}
  ],
  "education": [
    {{
      "degree": "",
      "field": "",
      "institution": "",
      "graduation_date": ""
    }}
  ],
  "projects": [
    {{
      "name": "",
      "description": "",
      "technologies": []
    }}
  ],
  "certifications": [],
  "summary": ""
}}

Rules:
- Put ONLY concrete technical technologies (languages, frameworks, tools, databases, APIs, cloud/devops platforms) into the skills lists - never job titles, soft skills, or full sentences.
- Every skill you list must be an exact technology name that appears in the resume text.
- If a section has no information, return an empty list or empty string for it.
- Do not fabricate dates, companies, or degrees that are not present in the text.
- end_date should be the literal text from the resume (e.g. "Present", "March 2023").
- Respond with the JSON object only - no extra commentary.

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"
"""


def _empty_resume_result() -> Dict[str, Any]:
    return {
        "skills": {
            "programming_languages": [],
            "frameworks_libraries": [],
            "databases": [],
            "apis": [],
            "cloud_technologies": [],
            "devops_tools": [],
            "development_tools": [],
            "other_technologies": [],
        },
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": [],
        "summary": "",
    }


class ResumeAnalyzer:
    """Turns raw resume text into structured, validated JSON via the shared LLM."""

    def __init__(self, model_manager: Optional[ModelManager] = None) -> None:
        self.model_manager = model_manager or ModelManager.get_instance()

    def analyze(self, resume_text: str) -> Dict[str, Any]:
        if not resume_text or not resume_text.strip():
            print("[WARN] ResumeAnalyzer received empty resume text.")
            return _empty_resume_result()

        prompt = RESUME_PROMPT_TEMPLATE.format(resume_text=resume_text.strip())
        raw_output = self.model_manager.generate(prompt, system_prompt=RESUME_SYSTEM_PROMPT)

        parsed = extract_json_object(raw_output)
        if parsed is None:
            print(
                "[WARN] ResumeAnalyzer: model output was not valid JSON. "
                "Falling back to an empty structured result.\n"
                f"Raw model output (truncated):\n{raw_output[:500]}"
            )
            return _empty_resume_result()

        return self._validate_and_clean(parsed)

    def _validate_and_clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = _empty_resume_result()

        skills = data.get("skills")
        if isinstance(skills, dict):
            for category in result["skills"]:
                value = skills.get(category)
                if isinstance(value, list):
                    result["skills"][category] = [
                        str(item).strip() for item in value if str(item).strip()
                    ]
        elif isinstance(skills, list):
            # If the model collapsed all categories into one flat list,
            # keep the data usable rather than discarding it.
            result["skills"]["other_technologies"] = [
                str(item).strip() for item in skills if str(item).strip()
            ]

        for key in ("experience", "education", "projects"):
            value = data.get(key)
            if isinstance(value, list):
                result[key] = [item for item in value if isinstance(item, dict)]

        certifications = data.get("certifications")
        if isinstance(certifications, list):
            result["certifications"] = [
                str(item).strip() for item in certifications if str(item).strip()
            ]
        elif isinstance(certifications, str) and certifications.strip():
            result["certifications"] = [certifications.strip()]

        summary = data.get("summary")
        if isinstance(summary, str):
            result["summary"] = summary.strip()

        return result

    def flat_skills(self, structured_resume: Dict[str, Any]) -> List[str]:
        """Every extracted skill across all categories, de-duplicated."""
        skills = structured_resume.get("skills", {})
        flat: List[str] = []
        for value in skills.values():
            if isinstance(value, list):
                flat.extend(value)

        seen = set()
        unique: List[str] = []
        for skill in flat:
            key = skill.lower().strip()
            if key and key not in seen:
                seen.add(key)
                unique.append(skill)
        return unique


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    manager = ModelManager.get_instance()
    analyzer = ResumeAnalyzer(manager)
    sample = "John Doe\nSoftware Engineer\nSkills: Java, Spring Boot, AWS"
    print(json.dumps(analyzer.analyze(sample), indent=2))
