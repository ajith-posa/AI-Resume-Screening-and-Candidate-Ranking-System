from fastapi import FastAPI

app = FastAPI(
    title="AI-Powered Resume Screening and Candidate Ranking System",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Screening System API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }