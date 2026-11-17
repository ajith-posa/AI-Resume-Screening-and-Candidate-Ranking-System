from processors.resume_parser import extract_resume_text
from utils.text_cleaner import clean_text


file_path = "data/resumes/sample_resume.pdf"

raw_text = extract_resume_text(file_path)

cleaned_text = clean_text(raw_text)

print("=" * 60)
print("CLEANED RESUME TEXT")
print("=" * 60)

print(cleaned_text)