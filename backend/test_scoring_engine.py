from models.scoring_engine import ScoringEngine


def main():

    # Results obtained from our previous
    # semantic skill matching stage.

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

    candidate_years = 3
    required_years = 2

    education_match = True

    engine = ScoringEngine()

    skill_score = engine.calculate_skill_score(
        match_results
    )

    semantic_score = engine.calculate_semantic_score(
        match_results
    )

    experience_score = engine.calculate_experience_score(
        candidate_years,
        required_years
    )

    education_score = engine.calculate_education_score(
        education_match
    )

    final_score = engine.calculate_final_score(
        skill_score,
        semantic_score,
        experience_score,
        education_score
    )

    print("\n" + "=" * 65)
    print("AI RESUME SCREENING - CANDIDATE SCORING")
    print("=" * 65)

    print(f"\nSkill Match Score  : {skill_score:.2f}%")
    print(f"Semantic Score     : {semantic_score:.2f}%")
    print(f"Experience Score   : {experience_score:.2f}%")
    print(f"Education Score    : {education_score:.2f}%")

    print("\n" + "-" * 65)

    print(f"FINAL SCORE        : {final_score:.2f}%")

    print("=" * 65)


if __name__ == "__main__":
    main()