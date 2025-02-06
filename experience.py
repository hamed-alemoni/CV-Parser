import spacy
from spacy.matcher import Matcher
from base import Extraction
import re
from typing import Any
from datetime import datetime
class Experience(Extraction):
    def __init__(self, text: str):
        self._text: str = text


    def extract(self) -> int:

        experiences: list[int] = ExperienceFinder(self._text).find_experience()
        experiences = max(experiences) if experiences else 0

        experience: int = ExperienceCalculationWithRegex(self._text).calculate_years_of_experience()

        if experiences or experience:
            return max(experiences, experience)

        if experience:
            return experience
        
        experience = ExperienceCalculationWithoutRegex(self._text).calculated_experience_during() 

        return experience


class ExperienceFinder:

    def __init__(self, resume_text: str):
        self._resume_text: str = resume_text

    def __word_to_num(self, word: str) -> float | None:
        # Adding a more extensive mapping for numbers written out in words
        word_map = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
            "eight": 8, "nine": 9, "ten": 10,  "twenty": 20,  "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
            "eighty": 80,  "ninety": 90,  "one hundred": 100
        }

        # Normalize the input by replacing hyphens with spaces and making it lowercase
        normalized_word = word.replace("-", " ").lower()

        # try to find integer part if it is exist
        value: int | str = self.__extract_integer_value(normalized_word)
        
        # If no space found, treat it as a simple word that is directly mapped
        # return word_map.get(normalized_word, None) if isinstance(value, str) else value
        return self.__calculate_total_experience(normalized_word.split(), word_map) if isinstance(value, str) else value

    @staticmethod
    def __calculate_total_experience(words: list[str], word_map: dict[str, int]) -> int:
                # if two unit appear in a row return the first one
        result: list[int] = []
        unit_counter: int = 0
        for i, word in enumerate(words):
            number: int = word_map.get(word.strip(), None)
            
            if not number:
                continue

            if number // 10 == 0:
                unit_counter += 1
            
            if unit_counter == 2:
                return word_map.get(words[i - 1].strip(), None)
            
            result.append(number)
        
        return sum(result)

        
    @staticmethod
    def __extract_integer_value(word: str) -> int | str:
        if " " in word:

            parts = word.split(" ")

            # Handle the first part (the integer part)
            integer_part = parts[0]

            if "/" in parts[1]:

                if integer_part.isdigit():
                    integer_value = int(integer_part)

                    return integer_value
            
        elif '.' in word:
            return int(float(word))
        
        return word



    def find_experience(self) -> list[int]:

        matches: list[str] = self.__find_matches()

        return self.__filter_experiences(matches)
    
    def __filter_experiences(self, matches: list[str]):
        related_work_experience: RelatedWorkExperience = RelatedWorkExperience(self._resume_text)
        years_of_experience = []
        check: bool = True



        for match in matches:
            match_parts = match.split()

            condition_value: bool = related_work_experience.is_work_experience(match, 40) or \
                        related_work_experience.is_work_experience(match, 50) or \
                        related_work_experience.is_work_experience(match, 60)
            
            if condition_value:  # Check if the context is related to work experience
                result, check = self.__find_experience_each_match(match, match_parts, check)
                years_of_experience.extend(result)

        if check and years_of_experience:
            years_of_experience = [sum(years_of_experience)]
        # Return the years of experience found
        return years_of_experience
    

    def __find_experience_each_match(self, match: str, match_parts: str, check: bool) -> tuple[list[int], bool]:

        years_of_experience: list[int] = []
        

        if len(match_parts) == 2:  # e.g., "10 years" or "5 yrs"
            num, check = self.__extract_number(match, match_parts, check)
            if num is not None:
                years_of_experience.append(num)
            return years_of_experience, check
        
        
        if len(match_parts) > 2:  # Spelled out numbers like "twenty one years"
            # Check if the combined phrase like "twenty two" is valid
            num = self.__word_to_num(" ".join(match_parts[:2]))  # Join first two words to form a full number
            if num is not None:
                years_of_experience.append(num)

            return years_of_experience, check
    
    def __extract_number(self, match: str, match_parts: str, check: bool) -> tuple[int, bool]:
        num = None
        if match_parts[1][0].lower() == "y":
            if not self.__is_containing_in(match):
                check = False
            num = int(match_parts[0]) if match_parts[0].isdigit() else self.__word_to_num(match_parts[0])
        elif match_parts[1][0].lower() == "m":
            num = int(match_parts[0]) // 12 if match_parts[0].isdigit() else self.__word_to_num(match_parts[0])
        elif match_parts[1][0].lower() == "d":
            num = int(match_parts[0]) // 365 if match_parts[0].isdigit() else self.__word_to_num(match_parts[0])

        return num, check

    def __find_matches(self) -> list[str]:

        # Updated regex pattern to handle compound numbers like "twenty two"
        experience_patterns = [
            # Match compound numbers like "one 1/2 years", "two 3/4 years", etc.
            r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)(?:[-\s](?:one|two|three|four|five|six|seven|eight|nine))?\s*(?:\d{1,2}/\d{1,2})?\s*(?:years?|yr|yrs?|months?|mo|mos?)\b",  # Matches both "twenty 2/3 years" and "10 1/2 years"
            r"\b\d{1,2}\s*\d{0,2}/\d{1,2}\s*(?:years?|yr|yrs?|months?|mo|mos?)\b",  # Matches "1 1/2 years", "2 3/4 months"
            r"\b\d{1,2}(?:\.\d+)?\s*(?:years?|yr|yrs?|months?|mo|mos?)\b",  # Matches decimal years like "2.5 years", "3.4 months"
            r"\b\d{1,2}\s*(?:years?|yr|yrs?|months?|mo|mos?)\b",  # Numerical years or months (like 10 years or 24 months),
            r"\b\d{1,9}\s*days?\b",
            r"\b\d{1,9}\s*(?:years?|yrs?|yr|months?|mos?|mo)",

        ]
        
        for pattern in experience_patterns:
        
            # Find matches for potential work experience terms in the resume text
            matches = re.findall(pattern, self._resume_text, flags=re.IGNORECASE)
            if matches:
                return matches

    
    def __is_containing_in(self, word: str) -> bool:

        index: int = self._resume_text.find(word) + len(word)

        text: str = self._resume_text[index:].strip()

        return text[0:2].lower() == "in"


class ExperienceCalculationWithRegex:
    def __init__(self, resume_text: str):
        self._resume_text: str = resume_text.replace("/", " ")

    def calculate_years_of_experience(self) -> int:
        dates: set[str] = self.__extract_years()
        durations: int = 0
        related_work_experience: RelatedWorkExperience = RelatedWorkExperience(self._resume_text)

        # Store the valid date ranges found
        valid_date_ranges: list[str] = []

        for date in dates:
            condition_value: bool = related_work_experience.is_work_experience(date, 43) or \
                                    related_work_experience.is_work_experience(date, 50) or \
                                    related_work_experience.is_work_experience(date, 67)

            if condition_value:
                date = self.__remove_bad_matches(date)
                valid_date_ranges.append(date)

        

        # Check for overlaps in the valid date ranges
        if len(valid_date_ranges) > 0:
            valid_date_ranges = {date.replace('from', '').strip() for date in valid_date_ranges}


            # Apply the get_bigger_date logic to find the later date range
            valid_date_ranges = list(reversed(self.sort_date_ranges(valid_date_ranges)))
            while valid_date_ranges:
                date_range1 = valid_date_ranges.pop()
                for date_range2 in valid_date_ranges:
                    # Only proceed if the ranges don't overlap
                    if self.check_overlap(date_range1, date_range2) and date_range1 != date_range2 and date_range1 not in date_range2 and date_range2 not in date_range1:
                        small_date_range: str = ''
                        if self.get_bigger_date(date_range1, date_range2) ==  date_range1:
                            small_date_range = date_range2[::]
                        else:
                            small_date_range = date_range1[::]
                            date_range1 = date_range2
                        try:
                            valid_date_ranges.remove(small_date_range)
                        except ValueError:
                            pass

                # Calculate the final duration using the "bigger" date range
                duration: int = self.__calculate_duration(date_range1)
                if duration:
                    durations += duration

        years_of_experience: int = 0 if durations == 0 else durations // 12

        return years_of_experience

    def check_overlap(self, date_range1: str, date_range2: str) -> bool:
        start1, end1 = self.__parse_date_range(date_range1)
        start2, end2 = self.__parse_date_range(date_range2)

        if not start1 or not end1 or not start2 or not end2:
            return False  # If dates are invalid, return False
        
        if (end1 == start2) or (end2 == start1) or (start1.year == end2.year) or (start2.year == end1.year):
            return False

        # Check if the ranges overlap
        return not (end1 < start2 or end2 < start1)

    def sort_date_ranges(self, date_ranges: list[str]) -> list[str]:
        sorted_ranges = []
        
        for date_range in date_ranges:
            if not sorted_ranges:
                sorted_ranges.append(date_range)
            else:
                inserted = False
                for i in range(len(sorted_ranges)):
                    if self.get_bigger_date(date_range, sorted_ranges[i]) == date_range:
                        sorted_ranges.insert(i, date_range)
                        inserted = True
                        break
                if not inserted:
                    sorted_ranges.append(date_range)
        
        return sorted_ranges

    def get_bigger_date(self, date_range1: str, date_range2: str):
        start1, end1 = self.__parse_date_range(date_range1)
        start2, end2 = self.__parse_date_range(date_range2)

        # If any date range couldn't be parsed, return the valid one
        if not start1 or not end1:
            return date_range2
        if not start2 or not end2:
            return date_range1
        
        if start1 < start2:
            return date_range1
        elif start2 < start1:
            return date_range2
        # Compare the end dates to return the later one
        elif end1 > end2:
            return date_range1
        elif end2 > end1:
            return date_range2
        else:
            # If both end dates are equal, return the later of the start dates
            return date_range1 if start1 > start2 else date_range2

    def __parse_date_range(self, date_range: str):
        if not date_range:
            return None, None  # Return None if the date range is invalid

        # Extract start and end dates from a date range string
        parts = re.split(r' to |-', date_range.lower())
        if len(parts) < 2:
            return None, None  # Return None if the date range doesn't contain both start and end dates

        start_date = self.__parse_date(parts[0])
        end_date = self.__parse_date(parts[1]) if len(parts) > 1 else None

        return start_date, end_date

    def __extract_years(self):
        import re

        matches = []

        date_patterns = [
            r"(?i)(\b(?:[A-Za-z]+|\d{2}|\d{2}/\d{4})\s?\d{4}\s*(?:to|to\s(?:Current|present))\s*(?:[A-Za-z]+|\d{2}|\d{2}/\d{4})?\s?\d{4}|\d{2}\s\d{4}\s*to\s(?:Current|present)|\d{2}/\d{4}\s*to\s*\d{2}/\d{4}|\b\d{2}\s\d{4}\s*to\s\d{2}\s\d{4})",
            r"(?i)(\b(?:[A-Za-z]{3,9}|\d{1,2})\s\d{3}\s*to\s(?:[A-Za-z]{3,9}|\d{1,2})?\s?\d{4}|\b\d{4}\s*to\s\d{4}|\d{1,2}/\d{4}\s*to\s*\d{1,2}/\d{4})",
            # r"(?i)\b(?:[A-Za-z]{3,9}\s?\d{4}|\d{2}\s?\d{4})\s*(?:to\s*(?:[A-Za-z]{3,9}\s?\d{4}|\d{2}\s?\d{4}|present|Current))?\b",
            r'(?i)\d{4} to (?:present|current)',
        ]
        
        result: list[str] = []
        for pattern in date_patterns:
            matches = re.findall(pattern, self._resume_text)
            if matches:
                result.extend(matches)

        result = list(set(result))
            
        return result

    @staticmethod
    def __remove_bad_matches(match: str) -> str:
        words: list[str] = match.split()

        for i, word in enumerate(words):
            if len(word) == 2 and word.isdigit():
                if int(word) > 12 or int(word) < 1:
                    words.remove(word)

            elif len(word) == 6 and word.isdigit():
                words.remove(word)

                if int(word[2:]) > 0:
                    words.insert(i, word[2:])

                if int(word[:2]) < 12 and int(word[:2]) > 1:
                    words.insert(i, word[:2])

        return " ".join(words)

    def __calculate_duration(self, date_range: str) -> int:
        date_range = re.sub(r'from', '', date_range.lower()).strip()

        # Split and parse the dates
        parts = re.split(r' to |-', date_range.lower())
        start_date = self.__parse_date(parts[0])
        end_date = self.__parse_date(parts[1]) if len(parts) > 1 else 0

        # Calculate duration in months
        if start_date and end_date:
            duration_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            return max(0, duration_months)  # Ensure no negative durations

        return None

    # Helper function to parse a date string
    def __parse_date(self, date_str):
        month_names = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }

        if date_str.lower() in ['current', 'present']:
            return datetime.now()

        match = re.match(r'(\d{2})/(\d{4})', date_str)
        if match:
            month, year = match.groups()
            return datetime(int(year), int(month), 1)

        match = re.match(r'(\w+)[ -]?(\d{4})', date_str)
        if match:

            month, year = match.groups()

            if int(year) != 0:
                if month.isdigit():
                    return datetime(int(year), int(month), 1)
                elif month.capitalize()[:3] in month_names:
                    return datetime(int(year), month_names[month.capitalize()[:3]], 1)

        match = re.match(r'(\d{4})', date_str)
        if match:
            return datetime(int(match.group()), 1, 1)

        return None


class ExperienceCalculationWithoutRegex:

    def __init__(self, text: str):
        self._text: str = text
        self._work_related_years: list[dict[str, Any]] = self.__detect_related_years(self.__extract_years())


    def __extract_years(self) -> list[int]:
        """
        Extract all valid years from the text using regex.
        A valid year is between 1900 and 2099.
        """
        year_pattern = r"\b(19[0-9]{2}|20[0-9]{2})\b"
        return [match.group() for match in re.finditer(year_pattern, self._text)]

    def __detect_related_years(self, extracted_years: list[int]) -> dict[str, Any]:
        """
        Detect if extracted years are related to work experience by analyzing their surrounding words.
        """

        related_work_experience: RelatedWorkExperience = RelatedWorkExperience(self._text)

        results: set = {year for year in extracted_years if related_work_experience.is_work_experience(year)}
        
        return results

    def calculated_experience_during(self) -> int:

        if not self._work_related_years:
            return 0

        related_years = [int(year) for year in self._work_related_years]

        min_year = min(related_years)

        max_year = max(related_years)

        return max_year - min_year


class RelatedWorkExperience:
    def __init__(self, text: str):
        self._text: str = text

    def is_work_experience(self, date: str, window_size=50):
        # List of common job-related keywords to check around the dates
        work_keywords = [
            # General work-related terms
            "work", "worked", "working", "employment", "employed", "job", "career", 
            "position", "role", "experience", "task", "tasks", "responsibility", 
            "responsibilities", "achievement", "achievements", "accomplishment", 
            "accomplishments", "skills", "expertise", "projects", "project", 'configure',
        
            # Management and leadership
            "manager", "management", "director", "supervisor", "lead", "leader", 
            "leadership", "coordinator", "head", "executive", "chief", "officer", 
            "admin", "administrator", "program manager", "team", "team leader",
        
            # Internships and training
            "intern", "internship", "trainee", "training", "apprentice", "apprenticeship",
        
            # Action verbs for work tasks
            "developed", "designed", "implemented", "planned", "executed", "organized", 
            "coordinated", "supervised", "managed", "initiated", "analyzed", "created", 
            "built", "optimized", "led", "solved", "improved", "achieved", "reduced", 
            "increased", "maintained", "supported", "deployed", "configured", 'filesrecord',
            "integrated", "tested", "launched", "delivered", "oversaw", "presented", 
            "taught", "mentored", "monitored", "evaluated", "streamlined", "innovated", 
            "designed", "collaborated", "reported", "proposed", "recommended", "researched",
        
            # Industry-specific terms
            "engineer", "engineering", "developer", "development", "software", 
            "hardware", "technology", "IT", "information technology", "data", "analytics", 
            "consultant", "consulting", "business", "marketing", "sales", "finance", 
            "accounting", "operations", "supply chain", "product", "customer", 
            "service", "support", "quality assurance", "QA", "HR", "human resources",
        
            # Keywords for certifications or achievements
            "certified", "certification", "license", "licensed", "accredited", 
            "awarded", "award", "honor", "honored", "recognition", "recognized",
        
            # Keywords for reports and documentation
            "report", "reports", "document", "documentation", "proposal", 
            "presentation", "presentations", "analysis", "analyses", "strategy", 
            "strategies", "plan", "plans", "policy", "policies",
        
            # Collaboration and communication
            "collaborated", "collaboration", "communicated", "communication", 
            "negotiated", "negotiation", "partnered", "stakeholder", "client", 
            "customer", "vendor", "supplier",
        
            # Miscellaneous
            "contract", "contractor", "freelance", "freelancer", "temporary", 
            "full-time", "part-time", "consulting", "outsourced", "self-employed",'technic'
        ]
        
        # List of common education-related keywords to exclude
        education_keywords = [
            "master", "bachelor", "diploma", "degree", "academic", "studies", "student", "course", "graduate",
            "graduated", "graduation", "thesis", "dissertation", 'certifi', 'certified'
        ]

        degree_keywords: list[str] = [
            "bsc", "msc", "phd", "bachelor", "master", "diploma", "bachelors", "masters",
        ]

        # Search for keywords near the date in the resume text
        start_index = self._text.find(date)
        # If the date is found, check the context around it
        if start_index != -1:
            # Look a few words before and after the date range to find any work-related keywords
            snippet = self._text[max(0, start_index - window_size):start_index + len(date) + window_size]
            
            # First, check if education-related keywords are found in the snippet. If yes, ignore it.
            if any(education_keyword.lower() in snippet.lower() for education_keyword in education_keywords):
                return False
            
            if any(degree_keyword.lower() in snippet.lower() for degree_keyword in degree_keywords):
                return False
            
            # Then, look for work-related keywords
            for keyword in work_keywords:
                if keyword.lower() in snippet.lower():  # Case-insensitive check for the keyword
                    return True
                    
        return False


