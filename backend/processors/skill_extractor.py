import re
from typing import Iterable, List

# Canonical skills and common spellings/abbreviations. Extend this vocabulary
# when a new domain or technology appears in your resumes/JDs.
SKILL_ALIASES = {
    "python": ["python", "python3", "python 3"],
    "java": ["java", "core java"],
    "javascript": ["javascript", "java script", "js"],
    "typescript": ["typescript", "type script", "ts"],
    "c": ["c programming", "c language"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "sql": ["sql", "structured query language"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo db"],
    "sqlite": ["sqlite"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node.js", "nodejs", "node js"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "django": ["django"],
    "rest api": ["rest api", "restful api", "rest apis", "restful apis"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "natural language processing": ["natural language processing", "nlp"],
    "computer vision": ["computer vision"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "pytorch": ["pytorch", "py torch"],
    "tensorflow": ["tensorflow", "tensor flow"],
    "keras": ["keras"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "opencv": ["opencv", "open cv"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "git": ["git"],
    "github": ["github", "git hub"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "google cloud": ["google cloud", "gcp", "google cloud platform"],
    "linux": ["linux"],
    "excel": ["excel", "microsoft excel"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "r": ["r programming", "r language"],
    "statistics": ["statistics", "statistical analysis"],
    "data analysis": ["data analysis", "data analytics"],
    "data visualization": ["data visualization", "data visualisation"],
    "transformers": ["transformers", "hugging face transformers"],
    "bert": ["bert"],
    "sentence-bert": ["sentence-bert", "sentence bert", "sbert"],
    "llm": ["llm", "large language model", "large language models"],
    "rag": ["rag", "retrieval augmented generation"],
    "fastapi": ["fastapi", "fast api"],
    "streamlit": ["streamlit"],
    "tkinter": ["tkinter"],
    "android": ["android", "android development"],
    "firebase": ["firebase"],
    "java servlets": ["java servlet", "java servlets", "servlet"],
    "hibernate": ["hibernate"],
}

def normalize_skill(value: str) -> str:
    """Normalize a skill label for exact comparison."""
    value = re.sub(r"^[\s\-•*]+", "", str(value or "").strip().lower())
    value = re.sub(r"\s+", " ", value)
    value = value.strip(" .,:;|()[]{}")
    for canonical, aliases in SKILL_ALIASES.items():
        if value == canonical or value in aliases:
            return canonical
    return value

def _skill_pattern(alias: str):
    # Prevent matching short aliases inside unrelated words (e.g. C in "Cloud").
    escaped = re.escape(alias.lower())
    if alias.lower() in {"c", "r", "js", "ts", "ai", "ml", "dl", "cv"}:
        return re.compile(r"(?<![a-z0-9+#])" + escaped + r"(?![a-z0-9+#])", re.I)
    return re.compile(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])", re.I)

def extract_skills_from_section(skill_lines: Iterable[str]) -> List[str]:
    """Split skill-section lines and remove category labels such as 'Programming:'."""
    skills = []
    for line in skill_lines or []:
        line = str(line).strip()
        if not line:
            continue
        # Remove a category prefix only when it appears before a colon.
        if ":" in line:
            prefix, remainder = line.split(":", 1)
            if len(prefix.split()) <= 6:
                line = remainder
        parts = re.split(r"[,;|•]\s*|\s+/\s+", line)
        for part in parts:
            skill = re.sub(r"^[\s\-*•]+", "", part).strip(" .:")
            if skill and skill.lower() not in {"technical skills", "skills"}:
                skills.append(skill)
    return _deduplicate(skills)

def extract_skills_from_text(text: str) -> List[str]:
    """
    Find known skills across the complete resume, including project descriptions.
    This is dictionary-assisted extraction, not an assumption that every noun is a skill.
    """
    text = str(text or "")
    found = []
    for canonical, aliases in SKILL_ALIASES.items():
        for alias in set(aliases + [canonical]):
            if _skill_pattern(alias).search(text):
                found.append(canonical)
                break
    return _deduplicate(found)

def _deduplicate(skills):
    result, seen = [], set()
    for skill in skills:
        key = normalize_skill(skill)
        if key and key not in seen:
            seen.add(key)
            result.append(key)
    return result
