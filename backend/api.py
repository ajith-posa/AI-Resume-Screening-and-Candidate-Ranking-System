
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Annotated, List
import os
import shutil
import uuid

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.services.batch_screening import BatchScreeningService


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI-Powered Resume Screening System",
    description="AI-based resume screening and candidate ranking system",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "data",
    "uploads"
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============================================================
# SERVE FRONTEND FILES
# ============================================================

app.mount(
    "/frontend",
    StaticFiles(
        directory=FRONTEND_DIR,
        html=True
    ),
    name="frontend"
)


# ============================================================
# ALLOWED FILE FORMATS
# ============================================================

ALLOWED_JD_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}

ALLOWED_RESUME_EXTENSIONS = {
    ".pdf",
    ".docx"
}


# ============================================================
# HELPER: SAVE UPLOADED FILE
# ============================================================

def save_uploaded_file(
    uploaded_file: UploadFile,
    allowed_extensions: set
) -> str:

    original_filename = os.path.basename(
        uploaded_file.filename or ""
    )

    if not original_filename:
        raise HTTPException(
            status_code=400,
            detail="An uploaded file has no filename."
        )

    extension = os.path.splitext(
        original_filename
    )[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file format: {original_filename}. "
                f"Allowed formats: "
                f"{', '.join(sorted(allowed_extensions))}"
            )
        )

    # Unique filename prevents overwriting files
    unique_filename = (
        f"{uuid.uuid4().hex}_{original_filename}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                uploaded_file.file,
                buffer
            )

        return file_path

    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)

        raise


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Resume Screening API is running",
        "frontend": "/frontend/index.html",
        "documentation": "/docs"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# ============================================================
# SCREEN CANDIDATES — NO FIXED RESUME LIMIT
# ============================================================

@app.post("/screen")
async def screen_candidates(

    # Job Description: one file
    job_description: Annotated[
        UploadFile,
        File(...)
    ],

    # Resumes: any number of uploaded files
    resumes: Annotated[
        List[UploadFile],
        File(...)
    ]

):

    saved_paths = []

    try:

        # ----------------------------------------------------
        # VALIDATE JOB DESCRIPTION
        # ----------------------------------------------------

        if not job_description.filename:
            raise HTTPException(
                status_code=400,
                detail="Job description file is required."
            )

        jd_extension = os.path.splitext(
            job_description.filename
        )[1].lower()

        if jd_extension not in ALLOWED_JD_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Job description must be PDF, DOCX, or TXT."
                )
            )

        # ----------------------------------------------------
        # VALIDATE RESUMES
        # ----------------------------------------------------

        if not resumes:
            raise HTTPException(
                status_code=400,
                detail="At least one resume is required."
            )

        for resume in resumes:

            if not resume.filename:
                raise HTTPException(
                    status_code=400,
                    detail="A resume filename is missing."
                )

            extension = os.path.splitext(
                resume.filename
            )[1].lower()

            if extension not in ALLOWED_RESUME_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Unsupported resume format: "
                        f"{resume.filename}. "
                        "Upload PDF or DOCX resumes."
                    )
                )

        # ----------------------------------------------------
        # SAVE JOB DESCRIPTION
        # ----------------------------------------------------

        jd_path = save_uploaded_file(
            job_description,
            ALLOWED_JD_EXTENSIONS
        )

        saved_paths.append(jd_path)

        # ----------------------------------------------------
        # SAVE ALL RESUMES
        # ----------------------------------------------------

        resume_paths = []

        for resume in resumes:

            resume_path = save_uploaded_file(
                resume,
                ALLOWED_RESUME_EXTENSIONS
            )

            resume_paths.append(resume_path)
            saved_paths.append(resume_path)

        # ----------------------------------------------------
        # RUN EXISTING SCREENING PIPELINE
        # ----------------------------------------------------

        batch_service = BatchScreeningService()

        result = batch_service.screen_multiple_resumes(
            jd_path,
            resume_paths
        )

        # ----------------------------------------------------
        # RETURN RANKED RESULTS
        # ----------------------------------------------------

        if isinstance(result, dict):
            result["total_resumes_submitted"] = len(
                resume_paths
            )

        return result

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Screening failed: {str(error)}"
        )

    finally:

        await job_description.close()

        for resume in resumes:
            await resume.close()


# ============================================================
# CUSTOM OPENAPI
# Makes Swagger display multiple resume uploads
# ============================================================

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = {

        "openapi": "3.0.3",

        "info": {
            "title": "AI-Powered Resume Screening System",
            "description": (
                "Upload one job description and any number "
                "of candidate resumes for AI screening "
                "and ranking."
            ),
            "version": "1.0.0"
        },

        "paths": {

            "/": {
                "get": {
                    "summary": "Home",
                    "responses": {
                        "200": {
                            "description": "API is running"
                        }
                    }
                }
            },

            "/health": {
                "get": {
                    "summary": "Health Check",
                    "responses": {
                        "200": {
                            "description": "API is healthy"
                        }
                    }
                }
            },

            "/screen": {
                "post": {
                    "summary": "Screen and Rank Candidates",

                    "description": (
                        "Upload one job description and one or "
                        "more resumes. Resumes are processed and "
                        "ranked by their final screening scores."
                    ),

                    "requestBody": {
                        "required": True,

                        "content": {
                            "multipart/form-data": {

                                "schema": {
                                    "type": "object",

                                    "properties": {

                                        "job_description": {
                                            "type": "string",
                                            "format": "binary",
                                            "description": (
                                                "Upload one Job "
                                                "Description PDF, "
                                                "DOCX, or TXT file."
                                            )
                                        },

                                        "resumes": {
                                            "type": "array",

                                            "items": {
                                                "type": "string",
                                                "format": "binary"
                                            },

                                            "description": (
                                                "Upload multiple "
                                                "candidate resumes "
                                                "in PDF or DOCX format."
                                            )
                                        }

                                    },

                                    "required": [
                                        "job_description",
                                        "resumes"
                                    ]
                                }
                            }
                        }
                    },

                    "responses": {

                        "200": {
                            "description": (
                                "Candidates screened and ranked "
                                "successfully."
                            )
                        },

                        "400": {
                            "description": "Invalid uploaded files"
                        },

                        "500": {
                            "description": "Screening failed"
                        }
                    }
                }
            }
        }
    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


# ============================================================
# CONNECT CUSTOM OPENAPI
# ============================================================

app.openapi = custom_openapi
