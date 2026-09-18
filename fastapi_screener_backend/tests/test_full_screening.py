"""
tests/test_full_screening.py

Run with:
    python -m tests.test_full_screening

Runs the entire pipeline end-to-end using in-memory resume/job text
and prints the full, explainable screening result.
"""
import json

from app.screening.screening_engine import ScreeningEngine


RESUME_TEXT = """
Jane Smith
Senior Backend Engineer

Summary:
Backend engineer with 5+ years of experience building scalable APIs.

Experience:
Backend Engineer, Acme Corp (Jan 2019 - Present)
- Built REST APIs using Python, Django, and FastAPI
- Worked with PostgreSQL and Redis
- Deployed services on Azure using Docker

Education:
BS Computer Science, University of Georgia, 2019

Certifications:
AWS Certified Developer - Associate
"""

JOB_TEXT = """
We are hiring a Backend Engineer (Python stack).

Required:
- Python
- Django
- PostgreSQL

Preferred:
- Redis
- FastAPI
- Azure

Requirements: 2 years of relevant experience.
Education: Bachelor's degree in Computer Science or related field.
"""


def main() -> int:
    engine = ScreeningEngine()
    result = engine.screen_resume_text(RESUME_TEXT, JOB_TEXT)

    print("\n=== FINAL SCREENING RESULT ===")
    print(json.dumps(result, indent=2, default=str))

    checks = [
        ("No error", result.get("error") is None),
        ("Final score present", "final_score" in result),
        ("Skill matching section present", "skill_matching" in result),
        ("Qualification section present", "qualification" in result),
        ("Has recommendation", bool(result.get("recommendation"))),
    ]
    for name, ok in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")

    passed = sum(1 for _, ok in checks if ok)
    print(f"\n{passed}/{len(checks)} end-to-end checks passed.")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
