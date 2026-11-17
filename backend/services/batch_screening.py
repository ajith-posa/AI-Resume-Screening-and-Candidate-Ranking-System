from backend.services.screening_pipeline import ScreeningPipeline
from backend.models.ranking_engine import RankingEngine


class BatchScreeningService:

    def __init__(self):
        self.screening_pipeline = ScreeningPipeline()
        self.ranking_engine = RankingEngine()

    def screen_multiple_resumes(self, jd_path, resume_paths):

        # Process Job Description only once
        job_information = self.screening_pipeline.process_job_description(
            jd_path
        )

        candidates = []

        # Process each resume
        for resume_path in resume_paths:

            candidate_information = (
                self.screening_pipeline.process_resume(resume_path)
            )

            score_result = (
                self.screening_pipeline.calculate_candidate_score(
                    candidate_information,
                    job_information
                )
            )

            candidate_name = candidate_information.get(
                "name",
                "Unknown Candidate"
            )

            candidate = {
                "name": candidate_name,
                "resume_path": resume_path,
                "final_score": score_result["final_score"],
                "skill_score": score_result["skill_score"],
                "semantic_score": score_result["semantic_score"],
                "experience_score": score_result["experience_score"],
                "education_score": score_result["education_score"],
                "matched_requirements": (
                    score_result["explanation"]
                    ["matched_requirements"]
                ),
                "missing_requirements": (
                    score_result["explanation"]
                    ["missing_requirements"]
                ),
                # Complete original certification lines relevant to the JD.
                # Empty list is rendered as "None" by the frontend.
                "certifications": score_result.get("certifications", []),
                "explanation": score_result["explanation"]
            }

            candidates.append(candidate)

        # Rank candidates
        ranked_candidates = self.ranking_engine.rank_candidates(
            candidates
        )

        return {
            "job_information": job_information,
            "ranked_candidates": ranked_candidates
        }
