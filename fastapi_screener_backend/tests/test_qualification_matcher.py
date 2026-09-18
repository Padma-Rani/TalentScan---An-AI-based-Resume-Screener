"""
tests/test_qualification_matcher.py

Run with:
    python -m tests.test_qualification_matcher
"""
import json

from app.ai.model_manager import ModelManager
from app.qualification.qualification_matcher import QualificationMatcher


def main() -> int:
    manager = ModelManager.get_instance()
    qm = QualificationMatcher(manager)

    print("\n--- Experience matching ---")
    experience_result = qm.match_experience(required_months=24, candidate_months=122)
    print(json.dumps(experience_result, indent=2))

    checks = [
        ("Experience matched", experience_result["matched"] is True),
        ("Experience score is 100", experience_result["score"] == 100.0),
    ]

    print("\n--- Education matching (intelligent, not exact string) ---")
    required_education = ["Bachelor's degree in Computer Science or a related field"]
    candidate_education = [
        {"degree": "BS", "field": "Computer Science", "institution": "University of Georgia"}
    ]
    education_result = qm.match_education(required_education, candidate_education)
    print(json.dumps(education_result, indent=2))
    checks.append(("Education matched via semantic similarity", education_result["matched"] is True))

    qualification_score = qm.qualification_score(experience_result, education_result)
    print(f"\nQualification score: {qualification_score}")
    checks.append(("Qualification score computed within 0-100", 0 <= qualification_score <= 100))

    for name, ok in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")

    passed = sum(1 for _, ok in checks if ok)
    print(f"\n{passed}/{len(checks)} qualification matcher checks passed.")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
