# AI-Powered Resume Screening and Candidate Ranking System

An AI-powered recruitment support system that automates resume screening, evaluates candidate profiles against job descriptions, and ranks applicants based on their relevance using Natural Language Processing (NLP) and Sentence-BERT.

## Project Overview

Recruitment teams often receive a large number of resumes for a single job opening. Manually reviewing every application can be time-consuming and may lead to inconsistent candidate evaluation.

The **AI-Powered Resume Screening and Candidate Ranking System** addresses this challenge by extracting relevant information from resumes and job descriptions, identifying matching skills, calculating candidate scores, and ranking applicants according to their suitability for a given position.

The system uses Sentence-BERT (`all-MiniLM-L6-v2`) to generate semantic embeddings and cosine similarity to evaluate contextual similarity between job requirements and candidate profiles.

## Key Features

- **Multiple Resume Upload:** Upload a job description and multiple candidate resumes.
- **Resume Parsing:** Extract candidate names, contact information, skills, education, experience, projects, and certifications.
- **Job Description Analysis:** Identify required and preferred technical skills and other job requirements.
- **Intelligent Skill Matching:** Compare candidate skills with job requirements using normalized exact matching and semantic matching.
- **Semantic Similarity:** Use Sentence-BERT embeddings and cosine similarity to measure contextual relevance.
- **Candidate Scoring:** Calculate individual scores for skill matching, semantic similarity, experience, and education.
- **Automated Ranking:** Rank candidates based on their weighted final scores.
- **Explainable Results:** Display matched requirements, missing requirements, and individual score breakdowns.
- **Certification Information:** Display certifications relevant to the job description or required skills.
- **Interactive Interface:** View candidate rankings and expand individual results to inspect detailed information.

## Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| NLP | Natural Language Processing |
| Semantic Model | Sentence-BERT |
| Pretrained Model | all-MiniLM-L6-v2 |
| Similarity Measurement | Cosine Similarity |
| Text Processing | spaCy |
| Machine Learning Libraries | PyTorch, Sentence-Transformers |
| API Documentation | FastAPI / Swagger UI |

## System Architecture

The system follows a modular architecture consisting of the following stages:

1. **Input Processing:** Accept a job description and multiple candidate resumes.
2. **Document Parsing:** Extract text from supported PDF, DOCX, and TXT documents.
3. **Information Extraction:** Identify relevant information from resumes and job descriptions.
4. **Skill Matching:** Compare extracted candidate skills with the technical requirements of the job.
5. **Semantic Analysis:** Generate Sentence-BERT embeddings and calculate cosine similarity.
6. **Candidate Evaluation:** Calculate skill, semantic, experience, and education scores.
7. **Ranking:** Calculate final weighted scores and arrange candidates in descending order.
8. **Explainable Output:** Display rankings, score breakdowns, matched and missing requirements, and relevant certifications.

## Candidate Scoring Methodology

The system calculates the final candidate score using a weighted scoring approach.

**Final Score Formula:**

Final Score = (0.40 × Skill Match) + (0.30 × Semantic Similarity) + (0.20 × Experience) + (0.10 × Education)

| Evaluation Parameter | Weight |
|---|---:|
| Skill Match | 40% |
| Semantic Similarity | 30% |
| Experience | 20% |
| Education | 10% |
| **Total** | **100%** |

Candidates are ranked according to their final scores, with higher-scoring candidates appearing first.

Certifications are displayed separately as supporting information and do not contribute additional points to the final score.

## Project Structure

```text
AI-Resume-Screening-and-Candidate-Ranking-System/
│
├── backend/
│   ├── api.py
│   ├── config.py
│   │
│   ├── models/
│   │   ├── semantic_matcher.py
│   │   └── skill_matcher.py
│   │
│   ├── processors/
│   │   ├── information_extractor.py
│   │   ├── skill_extractor.py
│   │   ├── jd_information_extractor.py
│   │   └── jd_skill_extractor.py
│   │
│   └── services/
│       ├── screening_pipeline.py
│       └── batch_screening.py
│
├── frontend/
│   └── index.html
│
├── data/
│   └── uploads/
│
├── requirements.txt
├── .gitignore
└── README.md
```

*The structure above represents the main project modules. Additional files may be present in the implementation.*

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ajithposa/AI-Resume-Screening-and-Candidate-Ranking-System.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Resume-Screening-and-Candidate-Ranking-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Download the spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### 6. Start the Backend Server

```bash
uvicorn backend.api:app --reload
```

### 7. Open the Application

Open the following URL in your browser:

```text
http://127.0.0.1:8000/frontend/index.html
```

FastAPI API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## How to Use

1. Open the application in your browser.
2. Navigate through the welcome page.
3. Upload the job description.
4. Upload multiple candidate resumes.
5. Click **Proceed with Screening**.
6. View the ranked candidate list and final scores.
7. Expand individual candidates to inspect their detailed evaluation.
8. Review skill scores, semantic similarity, experience, education, matched requirements, missing requirements, and relevant certifications.

## Expected Output

The application provides:

- Ranked candidate names.
- Final matching scores.
- Individual evaluation score breakdowns.
- Matched technical requirements.
- Missing technical requirements.
- Relevant certifications found in candidate resumes.

## Important Notes

- Candidate rankings depend on the quality and completeness of the uploaded documents.
- Semantic similarity indicates contextual relevance and does not guarantee technical proficiency.
- Certification information is extracted from resumes and is not independently verified by the system.
- The system is intended to support recruitment decisions, not replace human evaluation.

## Future Enhancements

- Integration with external recruitment platforms.
- Support for additional document formats.
- Improved extraction for complex resume layouts.
- Certification verification through credential providers.
- Advanced candidate analytics and reporting.
- Enhanced evaluation using larger and domain-specific language models.

## Authors

**Ajith Kumar Posa**
**Savanth G**
**Lokesh Gadhi**
**Thejas T J**

B.Tech – Computer Science and Engineering

Specialization: Artificial Intelligence and Machine Learning

## License

This project is developed for academic and educational purposes. A suitable open-source license can be added when the project is ready for public distribution.
