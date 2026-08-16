from app.matching.skill_normalizer import SkillNormalizer
from app.models.schemas import MatchType


def test_canonical_normalization():
    assert SkillNormalizer.normalize("React.js") == "react"
    assert SkillNormalizer.normalize("ReactJS") == "react"
    assert SkillNormalizer.normalize("JS") == "javascript"
    assert SkillNormalizer.normalize("ML") == "machine_learning"


def test_relationship_comparison():
    rel_type, conf = SkillNormalizer.compare_skills("React.js", "ReactJS")
    assert rel_type == MatchType.ALIAS

    rel_type, conf = SkillNormalizer.compare_skills("SQL", "MySQL")
    assert rel_type == MatchType.RELATED

    rel_type, conf = SkillNormalizer.compare_skills("Python", "Django")
    assert rel_type == MatchType.RELATED
