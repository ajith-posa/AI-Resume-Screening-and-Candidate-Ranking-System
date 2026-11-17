from backend.scoring_config import (
    SKILL_WEIGHT,
    SEMANTIC_WEIGHT,
    EXPERIENCE_WEIGHT,
    EDUCATION_WEIGHT
)


class ScoringEngine:

    # =========================================================
    # SKILL SCORE
    # =========================================================

    def calculate_skill_score(self, match_results):

        if not match_results:
            return 0.0

        matched = sum(
            1
            for result in match_results
            if result["status"] == "MATCHED"
        )

        total = len(match_results)

        return round(
            (matched / total) * 100,
            2
        )


    # =========================================================
    # SEMANTIC SCORE
    # =========================================================

    def calculate_semantic_score(self, match_results):

        if not match_results:
            return 0.0

        # Only similarity scores of requirements that
        # actually passed the matching threshold are used.

        matched_results = [
            result
            for result in match_results
            if result["status"] == "MATCHED"
        ]

        # No requirements matched
        if not matched_results:
            return 0.0

        total_similarity = sum(
            result["similarity"]
            for result in matched_results
        )

        average_similarity = (
            total_similarity / len(matched_results)
        )

        return round(
            average_similarity * 100,
            2
        )


    # =========================================================
    # EXPERIENCE SCORE
    # =========================================================

    def calculate_experience_score(
        self,
        candidate_years,
        required_years
    ):

        if required_years <= 0:
            return 100.0

        if candidate_years >= required_years:
            return 100.0

        return round(
            (candidate_years / required_years) * 100,
            2
        )


    # =========================================================
    # EDUCATION SCORE
    # =========================================================

    def calculate_education_score(
        self,
        education_match
    ):

        return 100.0 if education_match else 0.0


    # =========================================================
    # FINAL SCORE
    # =========================================================

    def calculate_final_score(
        self,
        skill_score,
        semantic_score,
        experience_score,
        education_score
    ):

        final_score = (

            skill_score * SKILL_WEIGHT

            + semantic_score * SEMANTIC_WEIGHT

            + experience_score * EXPERIENCE_WEIGHT

            + education_score * EDUCATION_WEIGHT

        )

        return round(
            final_score,
            2
        )