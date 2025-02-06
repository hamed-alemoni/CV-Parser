from base import Extraction
import spacy
from tools import get_unique_list

class Language(Extraction):

    def __init__(self, text: str, nlp: spacy.lang.en.English):
        self._text: str = text
        self._nlp: spacy.lang.en.English = nlp


    
    def extract(self) -> list[str]:

        doc = self._nlp(self._text)
        
        languages = ["english"]

        for ent in doc.ents:
            if "Language" in ent.label_:
                languages.append(ent.text)

        return get_unique_list(languages)