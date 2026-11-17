from services.batch_screening import BatchScreeningService


jd_path = "data/job_descriptions/python_developer.txt"

resume_paths = [
    "data/resumes/candidate_1.pdf",
    "data/resumes/candidate_2.pdf",
    "data/resumes/candidate_3.pdf",
    "data/resumes/candidate_4.pdf"
]


batch_service = BatchScreeningService()

result = batch_service.screen_multiple_resumes(
    jd_path,
    resume_paths
)


print("\n==============================")
print("JOB INFORMATION")
print("==============================")

print("Job Title:")
print(result["job_information"]["job_title"])

print("\nRequired Skills:")
print(result["job_information"]["required_skills"])


print("\n==============================")
print("CANDIDATE RANKING")
print("==============================")


for candidate in result["ranked_candidates"]:

    print("\n------------------------------")

    print("Rank:", candidate["rank"])
    print("Candidate:", candidate["name"])
    print("Final Score:", candidate["final_score"])

    print("Skill Score:", candidate["skill_score"])
    print("Semantic Score:", candidate["semantic_score"])
    print("Experience Score:", candidate["experience_score"])
    print("Education Score:", candidate["education_score"])

    print("\nMatched Requirements:")

    for item in candidate["matched_requirements"]:
        print(
            f"  {item['requirement']} "
            f"-> {item['matched_skill']} "
            f"({item['similarity']})"
        )

    print("\nMissing Requirements:")

    for item in candidate["missing_requirements"]:
        print(
            f"  {item['requirement']}"
        )