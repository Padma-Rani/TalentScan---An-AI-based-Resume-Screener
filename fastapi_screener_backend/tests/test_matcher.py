"""
tests/test_matcher.py

Run with:
    python -m tests.test_matcher

Verifies exact/alias/semantic matching and, critically, false-positive
prevention (e.g. "Spring Boot" must NOT match "Java", "Docker" must
NOT match "AWS").
"""
import json

from app.ai.model_manager import ModelManager
from app.matching.matcher import DynamicAIMatcher


def main() -> int:
    print("MODEL: sentence-transformers/all-MiniLM-L6-v2 (via shared ModelManager)")
    manager = ModelManager.get_instance()
    matcher = DynamicAIMatcher(manager)

    resume_skills = ["Java", "AWS", "Git", "Node.js"]
    required_skills = ["Java", "Spring Boot", "SQL", "AWS"]

    print(f"\nINPUT resume skills: {resume_skills}")
    print(f"INPUT required skills: {required_skills}")

    results = matcher.match_skill_list(required_skills, resume_skills)
    print("\nAI OUTPUT / matching decisions:")
    print(json.dumps(results, indent=2))

    checks = []

    java_result = next(r for r in results if r["required_skill"] == "Java")
    checks.append(("Java matches exactly", java_result["matched"] and java_result["match_type"] == "exact"))

    spring_result = next(r for r in results if r["required_skill"] == "Spring Boot")
    checks.append(("Spring Boot does NOT falsely match Java", not spring_result["matched"]))

    sql_result = next(r for r in results if r["required_skill"] == "SQL")
    checks.append(("SQL does NOT falsely match Java", not sql_result["matched"]))

    aws_result = next(r for r in results if r["required_skill"] == "AWS")
    checks.append(("AWS matches exactly", aws_result["matched"] and aws_result["match_type"] == "exact"))

    docker_vs_aws = matcher.match_single_skill("Docker", ["AWS"])
    checks.append(("Docker does NOT falsely match AWS", not docker_vs_aws["matched"]))

    alias_check = matcher.match_single_skill("JavaScript", ["JS"])
    checks.append(("JavaScript matches known alias JS", alias_check["matched"]))

    score = matcher.score_skill_matches(results)
    print(f"\nRequired skill score: {score}%")
    checks.append(("Skill score computed within 0-100", 0 <= score <= 100))

    for name, ok in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")

    passed = sum(1 for _, ok in checks if ok)
    print(f"\n{passed}/{len(checks)} matcher checks passed.")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
