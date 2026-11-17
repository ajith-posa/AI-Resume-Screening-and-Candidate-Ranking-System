import re

from backend.processors.skill_extractor import (
    extract_skills_from_text,
    normalize_skill,
)

# These are not technical skills and should not appear as JD skill requirements.
NON_TECHNICAL_TERMS = {
    "problem solving",
    "communication",
    "teamwork",
    "analytical thinking",
    "attention to detail",
    "willingness to learn",
    "ownership",
    "adaptability",
    "collaboration",
}

# Exclude education and experience statements from skill extraction.
NON_SKILL_LINE_PATTERNS = [
    r"\b(bachelor|bachelors|master|masters|degree|b\.?\s*tech|b\.?\s*e\.?)\b",
    r"\b(education|qualification|qualifications|years? of experience)\b",
    r"\b(fresh graduates?|entry[- ]level candidates?)\b",
]


def _clean_skill_line(line):
    line = str(line or "").strip()
    line = re.sub(r"^[\s•*\-\u2022]+", "", line)
    # Remove category prefixes such as "Programming:" or "Frameworks:".
    if ":" in line:
        prefix, remainder = line.split(":", 1)
        if len(prefix.split()) <= 6:
            line = remainder.strip()
    return line


def split_skills(lines):
    """
    Return only recognized technical skills from JD lines.

    Unlike a simple comma splitter, this does not treat full qualification
    sentences, degree names, soft skills, or generic prose as skills.
    """
    candidates = []

    for raw_line in lines or []:
        line = _clean_skill_line(raw_line)
        if not line:
            continue

        if any(re.search(pattern, line, re.I) for pattern in NON_SKILL_LINE_PATTERNS):
            continue

        # The project-wide skill vocabulary provides canonical names and aliases.
        found = extract_skills_from_text(line)
        for skill in found:
            normalized = normalize_skill(skill)
            if not normalized or normalized in NON_TECHNICAL_TERMS:
                continue
            candidates.append(normalized)

    result = []
    seen = set()
    for skill in candidates:
        normalized = normalize_skill(skill)
        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)

    return result
