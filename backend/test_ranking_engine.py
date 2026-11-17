from models.ranking_engine import RankingEngine


def main():

    candidates = [

    {
        "name": "Candidate A",
        "final_score": 87.80,
        "matched_skills": [
            "Python",
            "FastAPI",
            "SQL",
            "Machine Learning"
        ],
        "missing_skills": [
            "Git"
        ]
    },

    {
        "name": "Candidate B",
        "final_score": 82.40,
        "matched_skills": [
            "Python",
            "SQL",
            "Machine Learning"
        ],
        "missing_skills": [
            "FastAPI",
            "Git"
        ]
    },

    {
        "name": "Candidate C",
        "final_score": 74.60,
        "matched_skills": [
            "Python",
            "SQL"
        ],
        "missing_skills": [
            "FastAPI",
            "Machine Learning",
            "Git"
        ]
    }
]

    ranking_engine = RankingEngine()

    ranked_candidates = ranking_engine.rank_candidates(
        candidates
    )

    print("\n" + "=" * 65)
    print("AI RESUME SCREENING - CANDIDATE RANKING")
    print("=" * 65)

    print(
        f"\n{'Rank':<8}"
        f"{'Candidate':<25}"
        f"{'Score':<15}"
    )

    print("-" * 65)

    for candidate in ranked_candidates:

        print(
            f"{candidate['rank']:<8}"
            f"{candidate['name']:<25}"
            f"{candidate['final_score']:.2f}%"
        )

    print("=" * 65)


if __name__ == "__main__":
    main()