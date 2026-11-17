from processors.resume_parser import extract_resume_text
from utils.text_cleaner import clean_text
from processors.information_extractor import extract_resume_information


file_path = "data/resumes/sample_resume.pdf"

raw_text = extract_resume_text(file_path)

cleaned_text = clean_text(raw_text)

information = extract_resume_information(cleaned_text)

print("\n" + "=" * 60)
print("EXTRACTED CANDIDATE INFORMATION")
print("=" * 60)

for key, value in information.items():

    print(f"\n{key.upper()}:")

    if isinstance(value, list):

        for item in value:
            print(" -", item)

    else:
        print(" ", value)