from processors.jd_parser import extract_jd_text
from utils.text_cleaner import clean_text

from processors.jd_information_extractor import (
    extract_job_information
)


file_path = "data/job_descriptions/python_developer.txt"

raw_text = extract_jd_text(file_path)

cleaned_text = clean_text(raw_text)

job_information = extract_job_information(
    cleaned_text
)


print("\n" + "=" * 60)
print("EXTRACTED JOB INFORMATION")
print("=" * 60)


for key, value in job_information.items():

    print(f"\n{key.upper()}:")

    if isinstance(value, list):

        for item in value:
            print(" -", item)

    else:
        print(" ", value)