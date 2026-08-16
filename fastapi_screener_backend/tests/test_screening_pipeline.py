import os
import tempfile
import pytest
from app.pipeline.screening_pipeline import ScreeningPipeline
from app.models.schemas import DecisionType, RequirementStatus


def test_critical_semantic_eligibility_recovery():
    """Rule #30: Test candidate with ReactJS, Python ML, MySQL, HTTP API services vs Python, React.js, SQL, REST APIs."""
    jd_text = "Looking for a Software Developer with 2+ years of experience in Python, React.js, SQL and REST APIs."

    resume_text = (
        "PROFESSIONAL SUMMARY:\n"
        "Experienced Software Developer with 3 years of software engineering background.\n\n"
        "TECHNICAL SKILLS:\n"
        "Python, ReactJS, MySQL, HTTP API services\n\n"
        "WORK EXPERIENCE:\n"
        "Software Engineer | Tech Corp (2021 - Present)\n"
        "• Developed component-based frontend applications using ReactJS for responsive web apps.\n"
        "• Created Python ML applications for data analytics and predictive modeling.\n"
        "• Worked with MySQL databases to design relational schemas and optimize query performance.\n"
        "• Developed HTTP API services to expose backend functionality to mobile applications.\n"
    )

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write(resume_text)
        tmp_path = tmp.name

    try:
        response = ScreeningPipeline.screen_resume(tmp_path, jd_text)

        # Assertions
        assert response.decision in [DecisionType.SHORTLIST, DecisionType.MANUAL_REVIEW]
        assert response.overall_score >= 75.0
        assert response.confidence >= 0.75

        req_map = {r.requirement.lower(): r for r in response.requirements}

        assert "python" in req_map
        assert req_map["python"].status == RequirementStatus.MATCHED
        assert "sql" in req_map
        assert req_map["sql"].status in [RequirementStatus.MATCHED, RequirementStatus.POTENTIAL_MATCH]

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_missing_mandatory_requirement_rejection():
    """Test candidate missing mandatory requirement (Python & SQL absent)."""
    jd_text = "Must have 2+ years of experience in Python and SQL."
    resume_text = (
        "PROFESSIONAL SUMMARY:\n"
        "Graphic Designer with experience in Photoshop, Illustrator, and Figma.\n"
    )

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write(resume_text)
        tmp_path = tmp.name

    try:
        response = ScreeningPipeline.screen_resume(tmp_path, jd_text)
        assert response.decision == DecisionType.REJECT
        assert response.overall_score < 60.0
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
