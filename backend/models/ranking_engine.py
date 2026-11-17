class RankingEngine:

    def rank_candidates(self, candidates):
        """
        Rank candidates based on their final score.

        Each candidate must contain:
        {
            "name": str,
            "final_score": float
        }
        """

        ranked_candidates = sorted(
            candidates,
            key=lambda candidate: candidate["final_score"],
            reverse=True
        )

        # Assign rank numbers
        for index, candidate in enumerate(
            ranked_candidates,
            start=1
        ):
            candidate["rank"] = index

        return ranked_candidates