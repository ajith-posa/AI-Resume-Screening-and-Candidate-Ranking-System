class ExplainabilityEngine:

    def generate_skill_explanation(self, match_results):

        matched = []
        missing = []

        for result in match_results:

            requirement = result["requirement"]
            matched_skill = result.get("matched_skill")
            similarity = result["similarity"]
            status = result["status"]

            if status == "MATCHED":

                matched.append({
                    "requirement": requirement,
                    "matched_skill": matched_skill,
                    "similarity": similarity
                })

            else:

                missing.append({
                    "requirement": requirement,
                    "similarity": similarity
                })

        return {
            "matched_requirements": matched,
            "missing_requirements": missing
        }


    def generate_score_breakdown(
        self,
        skill_score,
        semantic_score,
        experience_score,
        education_score,
        final_score
    ):

        return {
            "skill_match_score": skill_score,
            "semantic_score": semantic_score,
            "experience_score": experience_score,
            "education_score": education_score,
            "final_score": final_score
        }


    def generate_explanation(
        self,
        match_results,
        skill_score,
        semantic_score,
        experience_score,
        education_score,
        final_score
    ):

        skill_explanation = self.generate_skill_explanation(
            match_results
        )

        score_breakdown = self.generate_score_breakdown(
            skill_score,
            semantic_score,
            experience_score,
            education_score,
            final_score
        )

        return {
            "matched_requirements":
                skill_explanation["matched_requirements"],

            "missing_requirements":
                skill_explanation["missing_requirements"],

            "score_breakdown":
                score_breakdown
        }