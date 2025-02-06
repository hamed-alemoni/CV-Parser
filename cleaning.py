from spacy.lang.en.stop_words import STOP_WORDS
import spacy
from typing import Iterator


class DataCleaning:
    def __init__(self, nlp: spacy):
        self._nlp: spacy = nlp

    def clean_data(self, text: str) -> str:
        doc = self._nlp(text)
        clean_tokens = []

        for token in doc:
            if token.text not in STOP_WORDS and token.pos_ != "PUNKT" and token.pos_ != "SYM" and token.pos_ != "SPACE":
                clean_tokens.append(token.lemma_.strip().lower())

        return " ".join(clean_tokens)
    
    # Function to remove verbs
    def remove_verbs(self, words: Iterator[str]) -> set[str]:
        non_verbs = {word for word in words if self._nlp(word)[0].pos_ != 'VERB'}
        return non_verbs
    
    
    # Function to lemmatize words
    def lemmatize_words(self, words: Iterator[str]) -> set[str]:
        lemmatized_words = {self._nlp(word)[0].lemma_ for word in words}
        return lemmatized_words
    
