from models.skill_matcher import SkillMatcher


def main():

    # Skills extracted from the candidate's resume
    resume_skills = [
        "Python",
        "Machine Learning",
        "FastAPI",
        "SQL",
        "TensorFlow",
        "Pandas",
        "NumPy"
    ]

    # Required skills extracted from the Job Description
    required_skills = [
        "Python",
        "FastAPI",
        "SQL",
        "Machine Learning",
        "Git"
    ]

    # Create matcher
    matcher = SkillMatcher()

    # Perform semantic matching
    results = matcher.match_requirements(
        required_skills,
        resume_skills
    )

    print("\n" + "=" * 70)
    print("AI RESUME SCREENING - SKILL MATCHING RESULTS")
    print("=" * 70)

    print(
        f"\nSemantic Match Threshold: "
        f"{__import__('config').SEMANTIC_MATCH_THRESHOLD}"
    )

    print("\nResume Skills:")
    print(", ".join(resume_skills))

    print("\nJob Required Skills:")
    print(", ".join(required_skills))

    print("\n" + "-" * 70)

    # Display individual results
    for result in results:

        print(f"\nRequirement : {result['requirement']}")
        print(f"Best Match  : {result['matched_skill']}")
        print(f"Similarity  : {result['similarity']}")
        print(f"Status      : {result['status']}")

    print("\n" + "-" * 70)

    # Summary
    matched = [
        result
        for result in results
        if result["status"] == "MATCHED"
    ]

    missing = [
        result
        for result in results
        if result["status"] == "MISSING"
    ]

    print("\nSUMMARY")
    print("-" * 70)

    print(f"Total Requirements : {len(results)}")
    print(f"Matched            : {len(matched)}")
    print(f"Missing            : {len(missing)}")

    print("\nMatched Requirements:")

    if matched:
        for result in matched:
            print(
                f"  ✓ {result['requirement']} "
                f"→ {result['matched_skill']} "
                f"({result['similarity']})"
            )
    else:
        print("  None")

    print("\nMissing Requirements:")

    if missing:
        for result in missing:
            print(
                f"  ✗ {result['requirement']} "
                f"→ Best available: {result['matched_skill']} "
                f"({result['similarity']})"
            )
    else:
        print("  None")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()