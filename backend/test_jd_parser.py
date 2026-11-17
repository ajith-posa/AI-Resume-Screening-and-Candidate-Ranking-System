from processors.jd_parser import extract_jd_text
from utils.text_cleaner import clean_text


file_path = "data/job_descriptions/python_developer.txt"

raw_text = extract_jd_text(file_path)

cleaned_text = clean_text(raw_text)

print("=" * 60)
print("JOB DESCRIPTION")
print("=" * 60)

print(cleaned_text)