import re

from backend.processors.jd_skill_extractor import split_skills


REQUIRED_SECTION_NAMES = [
    "REQUIRED SKILLS",
    "REQUIRED SKILL",
    "MANDATORY SKILLS",
    "REQUIRED QUALIFICATIONS & SKILLS",
    "REQUIRED QUALIFICATIONS AND SKILLS",
    "MINIMUM QUALIFICATIONS",
]

PREFERRED_SECTION_NAMES = [
    "PREFERRED SKILLS",
    "PREFERRED SKILL",
    "PREFERRED / GOOD-TO-HAVE SKILLS",
    "PREFERRED GOOD-TO-HAVE SKILLS",
    "GOOD-TO-HAVE SKILLS",
    "NICE-TO-HAVE SKILLS",
]

SECTION_HEADINGS = {
    "JOB TITLE",
    "JOB DESCRIPTION",
    "ABOUT THE ROLE",
    "KEY RESPONSIBILITIES",
    "RESPONSIBILITIES",
    "REQUIRED SKILLS",
    "REQUIRED SKILL",
    "MANDATORY SKILLS",
    "REQUIRED QUALIFICATIONS & SKILLS",
    "REQUIRED QUALIFICATIONS AND SKILLS",
    "MINIMUM QUALIFICATIONS",
    "PREFERRED SKILLS",
    "PREFERRED SKILL",
    "PREFERRED / GOOD-TO-HAVE SKILLS",
    "PREFERRED GOOD-TO-HAVE SKILLS",
    "GOOD-TO-HAVE SKILLS",
    "NICE-TO-HAVE SKILLS",
    "EDUCATION",
    "QUALIFICATION",
    "QUALIFICATIONS",
    "EXPERIENCE",
    "OTHER REQUIREMENTS",
    "WHAT WE LOOK FOR",
    "APPLICATION DETAILS",
    "JOB FUNCTION",
    "EMPLOYMENT TYPE",
    "WORK ARRANGEMENT",
    "LOCATION",
}


def _clean_heading(line):
    value = str(line or "").strip()
    value = re.sub(r"^[\s•*\-\x7f]+", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip().upper()


def _is_heading(line):
    value = str(line or "").strip()
    # Do not mistake normal sentences ending in "experience." for headings.
    if len(value) > 55 or any(mark in value for mark in ".!?;"):
        return False
    return _clean_heading(value) in SECTION_HEADINGS


def _get_lines(text):
    lines = []
    for raw_line in (text or "").replace("\r", "\n").split("\n"):
        line = raw_line.strip()
        if line:
            lines.append(line)
    return lines


def extract_section(text, section_names):
    lines = _get_lines(text)
    wanted = {_clean_heading(name) for name in section_names}

    # Use the last occurrence to skip summary-table labels when the full
    # section appears later in the document.
    start_index = None
    for index, line in enumerate(lines):
        if _is_heading(line) and _clean_heading(line) in wanted:
            start_index = index + 1

    if start_index is None:
        return []

    content = []
    for line in lines[start_index:]:
        if _is_heading(line):
            break
        content.append(line)

    return content


def extract_job_title(text):
    lines = _get_lines(text)
    for index, line in enumerate(lines):
        if _is_heading(line) and _clean_heading(line) == "JOB TITLE":
            if index + 1 < len(lines):
                return lines[index + 1].strip()

    # Fallback for simple JDs where the title is displayed without a label.
    for line in lines[:10]:
        if re.search(r"\b(software engineer|data scientist|machine learning engineer|python developer)\b", line, re.I):
            return line.strip()
    return None


def extract_job_information(text):
    required_lines = extract_section(text, REQUIRED_SECTION_NAMES)
    preferred_lines = extract_section(text, PREFERRED_SECTION_NAMES)

    education = extract_section(
        text,
        ["EDUCATION", "QUALIFICATION", "QUALIFICATIONS"],
    )

    # Degree requirements are often embedded inside "Required Qualifications
    # & Skills" instead of a separate EDUCATION heading.
    if not education:
        for line in required_lines:
            if re.search(
                r"\b(bachelor|bachelors|b\.?\s*tech|b\.?\s*e\.?|degree|computer science|computer engineering|information technology)\b",
                line,
                re.I,
            ):
                education.append(line)

    experience = extract_section(text, ["EXPERIENCE"])
    other_requirements = extract_section(
        text,
        ["OTHER REQUIREMENTS", "WHAT WE LOOK FOR"],
    )

    return {
        "job_title": extract_job_title(text),
        "required_skills": split_skills(required_lines),
        "preferred_skills": split_skills(preferred_lines),
        "education": education,
        "experience": experience,
        "other_requirements": other_requirements,
    }
