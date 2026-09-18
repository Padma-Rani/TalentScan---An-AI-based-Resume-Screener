"""
tests/test_resume_analyzer.py

Run with:
    python -m tests.test_resume_analyzer

Loads the real shared AI model and proves it can turn actual resume
text into structured JSON - not just that the model downloaded.
"""
import json

from app.ai.model_manager import ModelManager
from app.ai.resume_analyzer import ResumeAnalyzer


SAMPLE_RESUME = """
Jane Smith
Senior Backend Engineer

Summary:
Backend engineer with 5 years of experience building scalable APIs.

Experience:
Backend Engineer, Acme Corp (Jan 2021 - Present)
- Built REST APIs using Python, Django, and FastAPI
- Worked with PostgreSQL and Redis
- Deployed services on Azure using Docker

Education:
BS Computer Science, University of Georgia, 2019

Certifications:
AWS Certified Developer - Associate

Projects:
Order Processing Service - built with Python, FastAPI, PostgreSQL
"""


def main() -> int:
    print("MODEL: Qwen2.5-1.5B-Instruct (via shared ModelManager)")
    manager = ModelManager.get_instance()
    analyzer = ResumeAnalyzer(manager)

    print("\nINPUT (resume text):")
    print(SAMPLE_RESUME)

    result = analyzer.analyze(SAMPLE_RESUME)

    print("\nAI OUTPUT / PARSED RESULT:")
    print(json.dumps(result, indent=2))

    flat_skills = analyzer.flat_skills(result)
    print(f"\nFlat skill list: {flat_skills}")

    checks = {
        "has_skills": len(flat_skills) > 0,
        "has_experience": len(result["experience"]) > 0,
        "has_education": len(result["education"]) > 0,
        "has_summary": bool(result["summary"]),
    }
    for name, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")

    passed = sum(checks.values())
    print(f"\n{passed}/{len(checks)} resume analyzer checks passed.")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
