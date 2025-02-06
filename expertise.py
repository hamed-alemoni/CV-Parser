from base import Extraction
import spacy
from tools import get_unique_list
from add_pipeline import Pipeline

class Expertise(Extraction):

    def __init__(self, text: str, nlp):
        self._text: str = text
        self._nlp = nlp

        # add pipeline
        path: str = "patterns/expertises.jsonl"
        Pipeline(nlp=self._nlp, path=path, name='expertise', before='skill').add_pipe()

    
    def extract(self) -> str:

        doc = self._nlp(self._text)
        
        expertises: set[str] = set()

        for ent in doc.ents:
            if "Expertise" in ent.label_:
                expertises.add(ent.text.strip())

        return expertises