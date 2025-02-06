import re
from add_pipeline import Pipeline


class Education:
    def __init__(self, text: str, nlp):
        self._text: str = text.lower()  # Convert the input text to lowercase
        self._degree_keywords: list[str] = [
            "bsc", "msc", "phd", "bachelor", "master", "diploma", "bachelors", "masters"
        ]
        self._nlp = nlp

        # add pipeline
        path: str = "patterns/majors.jsonl"
        Pipeline(nlp, path, 'major', before='skill').add_pipe()

    def extract(self):
        education = []

        # Refined regex to capture degree and field only (excluding university)
        # Improved regex
        pattern = re.compile(
            r'\b(' + "|".join(map(re.escape, self._degree_keywords)) + r')\b'         # match degree keyword
            r'(?:\s+(?:in|of))?\s+'                                              # optional "in"/"of" and whitespace
            r'(.+?)'                                                             # non-greedy capture for the field
            r'(?=\s+(?:and|or)\s+(?:an\s+|a\s+)?\b(?:' + "|".join(map(re.escape, self._degree_keywords)) + r')\b|$)',
            re.IGNORECASE
        )



        # Find matches
        matches = pattern.findall(self._text)

        for degree, field in matches:

            field = self.__find_major(field) if field else "unknown field"

            if field:
                education_entry = f"{degree} in {field}".title()
                education.append(education_entry)


        # Remove duplicates
        return list(dict.fromkeys(education))
    
    def __find_major(self, text: str) -> str:
        doc = self._nlp(text)
        majors: set[str] = set()
        for ent in doc.ents:
            if ent.label_ == "Major":
                majors.add(ent.text)
            
        return ' and '.join(majors)


