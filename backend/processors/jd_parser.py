from pathlib import Path
from backend.processors.resume_parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)


def extract_jd_text(file_path):

    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    elif extension == ".txt":
        return file_path.read_text(
            encoding="utf-8"
        )

    else:
        raise ValueError(
            "Unsupported job description format."
        )