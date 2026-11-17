from models.explainability_engine import ExplainabilityEngine


def main():

    match_results = [

        {
            "requirement": "Python",
            "matched_skill": "Python",
            "similarity": 1.0,
            "status": "MATCHED"
        },

        {
            "requirement": "FastAPI",
            "matched_skill": "FastAPI",
            "similarity": 1.0,
            "status": "MATCHED"
        },

        {
            "requirement": "SQL",
            "matched_skill": "SQL",
            "similarity": 1.0,
            "status": "MATCHED"
        },

        {
            "requirement": "Machine Learning",
            "matched_skill": "Machine Learning",
            "similarity": 1.0,
            "status": "MATCHED"
        },

        {
            "requirement": "Git",
            "matched_skill": "Python",
            "similarity": 0.35,
            "status": "MISSING"
        }
    ]

    skill_score = 80.0
    semantic_score = 86.0
    experience_score = 100.0
    education_score = 100.0
    final_score = 87.80

    engine = ExplainabilityEngine()

    explanation = engine.generate_explanation(
        match_results,
        skill_score,
        semantic_score,
        experience_score,
        education_score,
        final_score
    )

    print("\n" + "=" * 70)
    print("AI RESUME SCREENING - EXPLAINABILITY")
    print("=" * 70)

    print("\nMATCHED REQUIREMENTS")
    print("-" * 70)

    for item in explanation["matched_requirements"]:

        print(
            f"✓ {item['requirement']} "
            f"→ {item['matched_skill']} "
            f"(Similarity: {item['similarity']})"
        )

    print("\nMISSING REQUIREMENTS")
    print("-" * 70)

    for item in explanation["missing_requirements"]:

        print(
            f"✗ {item['requirement']} "
            f"(Best available similarity: "
            f"{item['similarity']})"
        )

    print("\nSCORE BREAKDOWN")
    print("-" * 70)

    scores = explanation["score_breakdown"]

    print(
        f"Skill Match Score : "
        f"{scores['skill_match_score']:.2f}%"
    )

    print(
        f"Semantic Score    : "
        f"{scores['semantic_score']:.2f}%"
    )

    print(
        f"Experience Score  : "
        f"{scores['experience_score']:.2f}%"
    )

    print(
        f"Education Score   : "
        f"{scores['education_score']:.2f}%"
    )

    print(
        f"Final Score       : "
        f"{scores['final_score']:.2f}%"
    )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()