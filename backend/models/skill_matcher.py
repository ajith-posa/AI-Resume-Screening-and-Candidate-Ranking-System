from backend.models.semantic_matcher import SemanticMatcher
from backend.config import SEMANTIC_MATCH_THRESHOLD
from backend.processors.skill_extractor import normalize_skill


# Directional compatibility: a candidate's concrete technology can demonstrate
# knowledge of the broader language/standard. Do not treat the reverse as true.
RELATED_SKILLS = {
    "sql": {"mysql", "postgresql", "sqlite", "microsoft sql server"},
}

class SkillMatcher:
    def __init__(self):
        self.semantic_matcher = SemanticMatcher()

    def find_best_match(self, requirement, resume_skills):
        requirement_norm = normalize_skill(requirement)
        normalized_resume_skills = [
            (skill, normalize_skill(skill))
            for skill in (resume_skills or [])
        ]

        # 1. Exact normalized match.
        for original_skill, normalized_skill in normalized_resume_skills:
            if normalized_skill == requirement_norm:
                return {
                    "requirement": requirement,
                    "matched_skill": original_skill,
                    "similarity": 1.0,
                    "status": "MATCHED",
                    "match_type": "exact",
                }

        # 2. Safe directional technology-to-standard compatibility.
        accepted_related = RELATED_SKILLS.get(requirement_norm, set())
        for original_skill, normalized_skill in normalized_resume_skills:
            if normalized_skill in accepted_related:
                return {
                    "requirement": requirement,
                    "matched_skill": original_skill,
                    "similarity": 0.95,
                    "status": "MATCHED",
                    "match_type": "related",
                }

        # 3. Semantic fallback. Keep the configured threshold.
        best_skill = None
        best_score = -1.0
        for skill in (resume_skills or []):
            score = self.semantic_matcher.calculate_similarity(
                str(requirement), str(skill)
            )
            if score > best_score:
                best_score = score
                best_skill = skill

        matched = best_score >= SEMANTIC_MATCH_THRESHOLD
        return {
            "requirement": requirement,
            "matched_skill": best_skill if matched else None,
            "similarity": round(max(best_score, 0.0), 4),
            "status": "MATCHED" if matched else "MISSING",
            "match_type": "semantic" if matched else "none",
        }

    def match_requirements(self, required_skills, resume_skills):
        return [
            self.find_best_match(requirement, resume_skills)
            for requirement in (required_skills or [])
        ]
