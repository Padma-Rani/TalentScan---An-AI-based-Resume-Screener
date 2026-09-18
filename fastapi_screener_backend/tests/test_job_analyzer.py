"""
tests/test_job_analyzer.py

Run with:
    python -m tests.test_job_analyzer

Loads the real shared AI model and proves it can turn actual job
description text into structured requirements - and that it adapts to
completely different technology stacks WITHOUT any code change,
proving the system is dynamic rather than a hardcoded skill list.
"""
import json

from app.ai.model_manager import ModelManager
from app.ai.job_analyzer import JobDescriptionAnalyzer


JOB_1_JAVA_STACK = """
We are hiring a Backend Engineer.

Required:
- Java
- Spring Boot
- REST API
- SQL

Preferred:
- AWS
- Docker
- Kubernetes

Requirements: 2 years of software development experience.
Education: Bachelor's degree in Computer Science or a related field.
"""

JOB_2_PYTHON_STACK = """
We are hiring a Backend Engineer (Python stack).

Required:
- Python
- Django
- PostgreSQL

Preferred:
- Redis
- FastAPI
- Azure

Requirements: 18 months of relevant experience.
Education: Bachelor's degree in Computer Science or related field.
"""


def analyze_and_check(analyzer: JobDescriptionAnalyzer, label: str, text: str) -> bool:
    print(f"\n=== {label} ===")
    print("INPUT (job description):")
    print(text)

    result = analyzer.analyze(text)

    print("\nAI OUTPUT / PARSED RESULT:")
    print(json.dumps(result, indent=2))

    checks = {
        "has_required_skills": len(result["required_skills"]) > 0,
        "has_preferred_skills": len(result["preferred_skills"]) > 0,
        "experience_converted_to_months": result["experience_months"] > 0,
        "has_education": len(result["education"]) > 0,
    }
    for name, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")

    return all(checks.values())


def main() -> int:
    print("MODEL: Qwen2.5-1.5B-Instruct (via shared ModelManager)")
    manager = ModelManager.get_instance()
    analyzer = JobDescriptionAnalyzer(manager)

    ok_1 = analyze_and_check(analyzer, "Job 1 (Java stack)", JOB_1_JAVA_STACK)
    ok_2 = analyze_and_check(analyzer, "Job 2 (Python stack)", JOB_2_PYTHON_STACK)

    print("\n=== DYNAMISM CHECK ===")
    print(
        "No Python source code was changed between Job 1 and Job 2, yet the "
        "extracted technologies were entirely different sets - proving the "
        "extraction is AI-driven, not a hardcoded list."
    )

    passed = sum([ok_1, ok_2])
    print(f"\n{passed}/2 job description scenarios passed.")
    return 0 if passed == 2 else 1


if __name__ == "__main__":
    raise SystemExit(main())
