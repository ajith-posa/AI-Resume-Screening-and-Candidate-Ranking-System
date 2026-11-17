from models.semantic_matcher import SemanticMatcher


matcher = SemanticMatcher()


pairs = [

    (
        "Python programming",
        "Python development"
    ),

    (
        "Machine learning using Python",
        "Python based ML development"
    ),

    (
        "Database management using MySQL",
        "SQL database experience"
    ),

    (
        "Frontend development with React",
        "Deep learning using TensorFlow"
    )
]


print("=" * 60)
print("SEMANTIC SIMILARITY TEST")
print("=" * 60)


for resume_text, jd_text in pairs:

    score = matcher.calculate_similarity(
        resume_text,
        jd_text
    )

    print("\nResume :", resume_text)
    print("JD     :", jd_text)
    print("Score  :", round(score, 4))