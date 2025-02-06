
from base import Extraction
from tika import parser
from cleaning import DataCleaning
from education import Education
from expertise import Expertise
from skill import Skill
from language import Language
from experience import Experience
from dataclasses import dataclass

class DataExtraction(Extraction):
    def __init__(self, text: str, nlp):
        self._text: str = text
        self._nlp = nlp

    def extract(self) -> list[str]:
        separator: str = '/'
        cleaner: DataCleaning = DataCleaning(self._nlp)
        cleaned_text: str = cleaner.clean_data(self._text)

        languages: list[str] = Language(cleaned_text, self._nlp).extract()
        language: str = f"{separator}".join(languages)

        experience = Experience(self._text).extract()

        skills: list[str] = Skill(cleaned_text, self._nlp).extract()
        skill: str = f"{separator}".join(skills)

        educations: list[str] = Education(self._text, self._nlp).extract()
        education: str = f"{separator}".join(educations)

        expertises: list[str] = Expertise(cleaned_text, self._nlp).extract()
        expertise: str = f"{separator}".join(expertises)

        data: Data = Data(language, experience, skill, education, expertise)

        return data




@dataclass
class Data:
    language: str
    experience: int
    skill: str
    education: str
    expertise: str

