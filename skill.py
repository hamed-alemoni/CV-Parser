from base import Extraction
import spacy
from add_pipeline import Pipeline
from tools import get_unique_list

class Skill(Extraction):

    def __init__(self, text: str, nlp):
        self._text: str = text
        self._nlp = nlp

        # add pipeline
        path: str = "patterns/new_skills.jsonl"
        Pipeline(self._nlp, path, 'skill', before='ner').add_pipe()
    

    def extract(self) -> list[str]:
        doc = self._nlp(self._text)

        skills = []

        for ent in doc.ents:
            if "SKILL" in ent.label_:
                skills.append(ent.text)

        return get_unique_list(skills)
    
