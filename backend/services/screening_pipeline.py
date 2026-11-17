import re

from backend.processors.resume_parser import extract_resume_text
from backend.utils.text_cleaner import clean_text

from backend.processors.information_extractor import extract_resume_information
from backend.processors.jd_parser import extract_jd_text
from backend.processors.jd_information_extractor import extract_job_information

from backend.models.skill_matcher import SkillMatcher
from backend.models.scoring_engine import ScoringEngine
from backend.models.explainability_engine import ExplainabilityEngine


class ScreeningPipeline:

    def __init__(self):

        self.skill_matcher = SkillMatcher()

        self.scoring_engine = ScoringEngine()

        self.explainability_engine = ExplainabilityEngine()


    # =========================================================
    # JOB DESCRIPTION PROCESSING
    # =========================================================

    def process_job_description(self, jd_path):

        raw_text = extract_jd_text(jd_path)

        cleaned_text = clean_text(raw_text)

        job_information = extract_job_information(
            cleaned_text
        )

        return job_information


    # =========================================================
    # RESUME PROCESSING
    # =========================================================

    def process_resume(self, resume_path):

        raw_text = extract_resume_text(resume_path)

        cleaned_text = clean_text(raw_text)

        candidate_information = extract_resume_information(
            cleaned_text
        )

        # Store original resume text so that experience
        # can be detected even when the section extractor
        # does not capture a conventional "3 years" phrase.

        candidate_information["_raw_text"] = cleaned_text

        return candidate_information


    # =========================================================
    # CANDIDATE SCORE
    # =========================================================

    def calculate_candidate_score(
        self,
        candidate_information,
        job_information
    ):

        # -----------------------------------------------------
        # Skills
        # -----------------------------------------------------

        resume_skills = candidate_information.get(
            "skills",
            []
        )

        required_skills = job_information.get(
            "required_skills",
            []
        )


        match_results = self.skill_matcher.match_requirements(
            required_skills,
            resume_skills
        )


        skill_score = (
            self.scoring_engine.calculate_skill_score(
                match_results
            )
        )


        semantic_score = (
            self.scoring_engine.calculate_semantic_score(
                match_results
            )
        )


        # -----------------------------------------------------
        # Experience
        # -----------------------------------------------------

        candidate_experience_data = (
            candidate_information.get(
                "experience",
                []
            )
        )


        required_experience_data = (
            job_information.get(
                "experience",
                []
            )
        )


        # First try extracted experience section.
        candidate_years = (
            self._extract_experience_years(
                candidate_experience_data
            )
        )


        # If section extraction did not find years,
        # search the complete resume text.
        if candidate_years == 0:

            candidate_years = (
                self._extract_experience_years(
                    candidate_information.get(
                        "_raw_text",
                        ""
                    )
                )
            )


        required_years = (
            self._extract_required_years(
                required_experience_data
            )
        )


        experience_score = (
            self.scoring_engine.calculate_experience_score(
                candidate_years,
                required_years
            )
        )


        # -----------------------------------------------------
        # Education
        # -----------------------------------------------------

        education_match = self._check_education_match(

            candidate_information.get(
                "education",
                []
            ),

            job_information.get(
                "education",
                []
            )

        )


        education_score = (
            self.scoring_engine.calculate_education_score(
                education_match
            )
        )


        # -----------------------------------------------------
        # Final Score
        # -----------------------------------------------------

        final_score = (
            self.scoring_engine.calculate_final_score(

                skill_score,

                semantic_score,

                experience_score,

                education_score

            )
        )


        # -----------------------------------------------------
        # Explainability
        # -----------------------------------------------------

        explanation = (
            self.explainability_engine.generate_explanation(

                match_results,

                skill_score,

                semantic_score,

                experience_score,

                education_score,

                final_score

            )
        )


        # -----------------------------------------------------
        # Return Result
        # -----------------------------------------------------

        return {

            "match_results": match_results,

            "skill_score": skill_score,

            "semantic_score": semantic_score,

            "experience_score": experience_score,

            "education_score": education_score,

            "final_score": final_score,

            "candidate_experience_years":
                candidate_years,

            "required_experience_years":
                required_years,

            # Informational only: does not affect skill, semantic, experience,
            # education, or final scores.
            "certifications": self._filter_relevant_certifications(
                candidate_information.get("certifications", []),
                job_information
            ),

            "explanation": explanation

        }



    def _filter_relevant_certifications(
        self,
        certifications,
        job_information
    ):
        """
        Keep complete certification lines that mention a JD skill or job title.
        This is display-only and does not affect candidate scoring.
        """
        if not certifications:
            return []

        jd_skills = (
            job_information.get("required_skills", [])
            + job_information.get("preferred_skills", [])
        )

        job_title = job_information.get("job_title")
        search_terms = [str(skill).strip() for skill in jd_skills if skill]
        if job_title:
            search_terms.append(str(job_title).strip())

        # Normalize whitespace but retain the original certification wording.
        normalized_terms = []
        for term in search_terms:
            term = re.sub(r"\s+", " ", term).strip()
            if term and term.lower() not in {x.lower() for x in normalized_terms}:
                normalized_terms.append(term)

        relevant = []
        for original_line in certifications:
            line = str(original_line).strip()
            if not line:
                continue

            # Phrase-aware match: avoids matching "Java" inside "JavaScript".
            line_lower = re.sub(r"\s+", " ", line).lower()
            for term in normalized_terms:
                pattern = r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])"
                if re.search(pattern, line_lower):
                    relevant.append(line)
                    break

        # Preserve order and avoid duplicate lines.
        return list(dict.fromkeys(relevant))

    # =========================================================
    # EXPERIENCE EXTRACTION
    # =========================================================

    def _extract_experience_years(self, experience_data):

        if not experience_data:
            return 0.0


        # Convert list or string into one string.

        if isinstance(experience_data, list):

            text = " ".join(
                str(item)
                for item in experience_data
            )

        else:

            text = str(experience_data)


        text = text.lower()


        # -----------------------------------------------------
        # Pattern 1:
        #
        # 3 years
        # 3+ years
        # 2.5 years
        # 2.5+ years
        # -----------------------------------------------------

        year_matches = re.findall(

            r"(\d+(?:\.\d+)?)\s*\+?\s*years?",

            text

        )


        if year_matches:

            return max(

                float(value)

                for value in year_matches

            )


        # -----------------------------------------------------
        # Pattern 2:
        #
        # 3 yrs
        # 2+ yrs
        # -----------------------------------------------------

        yr_matches = re.findall(

            r"(\d+(?:\.\d+)?)\s*\+?\s*yrs?",

            text

        )


        if yr_matches:

            return max(

                float(value)

                for value in yr_matches

            )


        # -----------------------------------------------------
        # Pattern 3:
        #
        # 2022 - 2025
        # 2022 to 2025
        # 2022–2025
        # -----------------------------------------------------

        date_ranges = re.findall(

            r"\b(20\d{2})\s*"
            r"(?:-|–|—|to)\s*"
            r"(20\d{2})\b",

            text

        )


        if date_ranges:

            total_years = 0.0

            for start_year, end_year in date_ranges:

                start = int(start_year)

                end = int(end_year)

                if end >= start:

                    total_years += (
                        end - start
                    )


            if total_years > 0:

                return total_years


        # -----------------------------------------------------
        # Pattern 4:
        #
        # 2023 - Present
        # 2023 to Present
        # -----------------------------------------------------

        current_year = 2026

        present_ranges = re.findall(

            r"\b(20\d{2})\s*"
            r"(?:-|–|—|to)\s*"
            r"(?:present|current)\b",

            text

        )


        if present_ranges:

            total_years = 0.0

            for start_year in present_ranges:

                start = int(start_year)

                if current_year >= start:

                    total_years += (
                        current_year - start
                    )


            if total_years > 0:

                return total_years


        return 0.0


    # =========================================================
    # REQUIRED EXPERIENCE
    # =========================================================

    def _extract_required_years(
        self,
        experience_data
    ):

        return self._extract_experience_years(
            experience_data
        )


    # =========================================================
    # EDUCATION MATCH
    # =========================================================

    def _check_education_match(
        self,
        candidate_education,
        required_education
    ):
        """
        Compare degree level and field of study rather than requiring the
        exact same wording. Example: BTech in CSE (AIML) can satisfy a
        Bachelor's degree in Computer Science / a related discipline.
        """
        if not required_education:
            return True

        if not candidate_education:
            return False

        def to_text(value):
            if isinstance(value, (list, tuple, set)):
                return " ".join(str(item) for item in value)
            return str(value)

        candidate_text = re.sub(
            r"\s+", " ", to_text(candidate_education).lower()
        )
        required_text = re.sub(
            r"\s+", " ", to_text(required_education).lower()
        )

        # Normalize common Indian degree abbreviations and study fields.
        candidate_text = re.sub(r"\bb\.?\s*tech\b", " bachelor ", candidate_text)
        candidate_text = re.sub(r"\bb\.?\s*e\.?\b", " bachelor ", candidate_text)
        candidate_text = re.sub(r"\bbachelor'?s?\b", " bachelor ", candidate_text)
        candidate_text = re.sub(r"\bcse\b", " computer science ", candidate_text)
        candidate_text = re.sub(r"\bc\.s\.e\.?\b", " computer science ", candidate_text)
        candidate_text = re.sub(r"\baiml\b", " artificial intelligence machine learning ", candidate_text)
        candidate_text = re.sub(r"\bai\s*&\s*ml\b", " artificial intelligence machine learning ", candidate_text)
        candidate_text = re.sub(r"\bcs\b", " computer science ", candidate_text)
        candidate_text = re.sub(r"\bb\.?\s*sc\b", " bachelor science ", candidate_text)
        candidate_text = re.sub(r"\bm\.?\s*tech\b", " master ", candidate_text)
        candidate_text = re.sub(r"\bm\.?\s*e\.?\b", " master ", candidate_text)
        candidate_text = re.sub(r"\bmaster'?s?\b", " master ", candidate_text)

        required_text = re.sub(r"\bb\.?\s*tech\b", " bachelor ", required_text)
        required_text = re.sub(r"\bb\.?\s*e\.?\b", " bachelor ", required_text)
        required_text = re.sub(r"\bbachelor'?s?\b", " bachelor ", required_text)
        required_text = re.sub(r"\bcse\b", " computer science ", required_text)
        required_text = re.sub(r"\bc\.s\.e\.?\b", " computer science ", required_text)
        required_text = re.sub(r"\baiml\b", " artificial intelligence machine learning ", required_text)
        required_text = re.sub(r"\bai\s*&\s*ml\b", " artificial intelligence machine learning ", required_text)
        required_text = re.sub(r"\bcs\b", " computer science ", required_text)
        required_text = re.sub(r"\bm\.?\s*tech\b", " master ", required_text)
        required_text = re.sub(r"\bm\.?\s*e\.?\b", " master ", required_text)
        required_text = re.sub(r"\bmaster'?s?\b", " master ", required_text)

        # If the JD specifies a degree level, require a compatible level.
        candidate_has_bachelor = "bachelor" in candidate_text
        candidate_has_master = "master" in candidate_text
        required_has_bachelor = "bachelor" in required_text
        required_has_master = "master" in required_text

        if required_has_master and not candidate_has_master:
            return False
        if required_has_bachelor and not (candidate_has_bachelor or candidate_has_master):
            return False

        # If the JD names a discipline, require the candidate to show that
        # discipline or a recognized related discipline.
        discipline_groups = [
            {
                "computer science", "computer engineering",
                "information technology", "software engineering"
            },
            {
                "artificial intelligence", "machine learning",
                "data science"
            },
            {"electronics", "electrical engineering"},
        ]

        for group in discipline_groups:
            required_mentions = any(term in required_text for term in group)
            if required_mentions:
                candidate_mentions = any(term in candidate_text for term in group)
                # AI/ML and Data Science are related to CSE for a CSE/AIML degree.
                if not candidate_mentions:
                    if group == {"artificial intelligence", "machine learning", "data science"}:
                        candidate_mentions = (
                            "computer science" in candidate_text
                            or "computer engineering" in candidate_text
                        )
                    elif group == {
                        "computer science", "computer engineering",
                        "information technology", "software engineering"
                    }:
                        candidate_mentions = (
                            "artificial intelligence" in candidate_text
                            or "machine learning" in candidate_text
                            or "data science" in candidate_text
                        )
                if not candidate_mentions:
                    return False

        # If the JD only asks for a bachelor's/degree without naming a field,
        # a BTech is sufficient. If it gives no recognizable criteria, avoid
        # awarding a match based on unrelated words.
        if required_has_bachelor or required_has_master:
            return True

        recognized_terms = [
            "computer science", "computer engineering",
            "information technology", "software engineering",
            "artificial intelligence", "machine learning",
            "data science", "electronics", "electrical engineering",
        ]
        return any(term in required_text for term in recognized_terms) and any(
            term in candidate_text for term in recognized_terms
        )

