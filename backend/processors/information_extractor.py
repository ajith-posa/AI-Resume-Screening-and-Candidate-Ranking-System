import re
from backend.processors.skill_extractor import (
    extract_skills_from_section,
    extract_skills_from_text,
)

SECTION_HEADINGS = {
    "EDUCATION", "SKILLS", "TECHNICAL SKILLS", "EXPERIENCE",
    "WORK EXPERIENCE", "PROJECTS", "PROJECT", "CERTIFICATIONS",
    "CERTIFICATION", "CERTIFICATIONS & TRAINING",
    "LICENSES & CERTIFICATIONS", "SUMMARY", "PROFESSIONAL SUMMARY",
    "OBJECTIVE", "ACHIEVEMENTS", "PUBLICATIONS", "INTERESTS",
    "PERSONAL DETAILS", "CONTACT", "CONTACT DETAILS",
}

NON_NAME_TERMS = {
    "resume", "curriculum vitae", "profile", "portfolio", "projects",
    "project", "developer", "engineer", "student", "intern", "objective",
    "summary", "artificial intelligence", "machine learning",
    "deep learning", "student performance", "url shortener",
    "link management", "ai tutor", "adaptive personalized learning",
}

def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text or "")
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r"(?:\+91[-\s]?)?[6-9]\d{9}", text or "")
    return match.group(0) if match else None

def _clean_header_line(line):
    line = re.sub(r"^[\s|•*#\-]+", "", line).strip()
    line = re.sub(r"\s*[|•]\s*.*$", "", line).strip()
    return line

def _looks_like_person_name(candidate):
    candidate = _clean_header_line(candidate)
    if not candidate or len(candidate) > 60 or any(ch.isdigit() for ch in candidate):
        return False
    lowered = candidate.lower().strip(" .,:;-")
    if lowered in NON_NAME_TERMS or lowered in {h.lower() for h in SECTION_HEADINGS}:
        return False
    if any(term in lowered for term in (
        "system", "application", "management", "prediction", "learning",
        "platform", "website", "project", "developer", "engineer",
        "technology", "database", "analysis", "shortener", "tutor"
    )):
        return False
    words = re.findall(r"[A-Za-z][A-Za-z'.-]*", candidate)
    if not 2 <= len(words) <= 4:
        return False
    # A name-like header should not be a sentence or a technical heading.
    if any(w.lower() in {"using", "with", "for", "and", "the", "system", "project"} for w in words):
        return False
    return all(w[0].isupper() for w in words)

def extract_name(text):
    lines = [_clean_header_line(line) for line in (text or "").splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return None

    # Explicit labelled name is the strongest signal.
    for i, line in enumerate(lines[:12]):
        match = re.match(r"(?i)^name\s*:\s*(.+)$", line)
        if match and _looks_like_person_name(match.group(1)):
            return match.group(1).strip()
        if line.upper().rstrip(":") == "NAME" and i + 1 < len(lines):
            if _looks_like_person_name(lines[i + 1]):
                return lines[i + 1]

    # Prefer a short, name-like line in the resume header only.
    header_lines = lines[:8]
    for line in header_lines:
        if "@" in line or re.search(r"\b(?:https?://|www\.|linkedin|github\.com)\b", line, re.I):
            continue
        if line.upper().rstrip(":") in {h for h in SECTION_HEADINGS}:
            continue
        if _looks_like_person_name(line):
            return line

    # spaCy is restricted to the header. Never search project descriptions for PERSON entities.
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("\n".join(header_lines))
        for entity in doc.ents:
            if entity.label_ == "PERSON" and _looks_like_person_name(entity.text):
                return entity.text.strip()
    except (ImportError, OSError):
        pass
    return None

def extract_section(text, section_names):
    lines = (text or "").splitlines()
    wanted = {name.upper() for name in section_names}
    collecting = False
    section_content = []
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        upper = re.sub(r"[:\s]+$", "", clean.upper())
        if upper in wanted:
            collecting = True
            continue
        if collecting and upper in SECTION_HEADINGS:
            break
        if collecting:
            section_content.append(clean)
    return section_content

def extract_resume_information(text):
    text = text or ""
    skill_section = extract_section(text, ["SKILLS", "TECHNICAL SKILLS"])
    section_skills = extract_skills_from_section(skill_section)
    # Also inspect the full resume so technologies mentioned in project descriptions
    # are not missed. The dictionary limits extraction to known skill names/aliases.
    all_text_skills = extract_skills_from_text(text)
    skills = list(dict.fromkeys(section_skills + all_text_skills))

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_section(text, ["EDUCATION"]),
        "skills": skills,
        "experience": extract_section(text, ["EXPERIENCE", "WORK EXPERIENCE"]),
        "projects": extract_section(text, ["PROJECTS", "PROJECT"]),
        # Preserve each original certification line; relevance filtering happens
        # later in ScreeningPipeline using the selected JD.
        "certifications": extract_section(
            text,
            [
                "CERTIFICATIONS",
                "CERTIFICATION",
                "CERTIFICATIONS & TRAINING",
                "LICENSES & CERTIFICATIONS",
            ],
        ),
    }
