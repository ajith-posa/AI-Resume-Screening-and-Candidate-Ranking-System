from services.screening_pipeline import ScreeningPipeline


def main():

    jd_path = (
        "data/job_descriptions/"
        "python_developer.txt"
    )

    resume_path = (
        "data/resumes/"
        "sample_resume.pdf"
    )

    pipeline = ScreeningPipeline()

    print("\n" + "=" * 70)
    print("AI RESUME SCREENING SYSTEM")
    print("=" * 70)

    # --------------------------------------------------
    # PROCESS JOB DESCRIPTION
    # --------------------------------------------------

    print("\n[1] Processing Job Description...")

    job_information = (
        pipeline.process_job_description(
            jd_path
        )
    )

    print("Job Title:")
    print(
        job_information["job_title"]
    )

    print("\nRequired Skills:")
    for skill in job_information["required_skills"]:
        print(" -", skill)

    # --------------------------------------------------
    # PROCESS RESUME
    # --------------------------------------------------

    print("\n[2] Processing Resume...")

    candidate_information = (
        pipeline.process_resume(
            resume_path
        )
    )

    print("Candidate:")
    print(
        candidate_information["name"]
    )

    print("\nResume Skills:")
    for skill in candidate_information["skills"]:
        print(" -", skill)

    # --------------------------------------------------
    # CALCULATE SCORE
    # --------------------------------------------------

    print("\n[3] Running AI Screening...")

    result = pipeline.calculate_candidate_score(
        candidate_information,
        job_information
    )

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("SCREENING RESULT")
    print("=" * 70)

    print(
        f"\nCandidate: "
        f"{candidate_information['name']}"
    )

    print(
        f"Final Score: "
        f"{result['final_score']:.2f}%"
    )

    print("\nSCORE BREAKDOWN")
    print("-" * 70)

    print(
        f"Skill Match : "
        f"{result['skill_score']:.2f}%"
    )

    print(
        f"Semantic    : "
        f"{result['semantic_score']:.2f}%"
    )

    print(
        f"Experience  : "
        f"{result['experience_score']:.2f}%"
    )

    print(
        f"Education   : "
        f"{result['education_score']:.2f}%"
    )

    print("\nMATCHED REQUIREMENTS")
    print("-" * 70)

    for item in result[
        "explanation"
    ]["matched_requirements"]:

        print(
            f"✓ {item['requirement']}"
            f" → {item['matched_skill']}"
            f" ({item['similarity']})"
        )

    print("\nMISSING REQUIREMENTS")
    print("-" * 70)

    for item in result[
        "explanation"
    ]["missing_requirements"]:

        print(
            f"✗ {item['requirement']}"
        )

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()