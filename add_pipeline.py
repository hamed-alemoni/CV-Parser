import spacy

class Pipeline:
    def __init__(self, nlp: spacy.lang, path: str, name: str, after: str=None, before: str=None, first: bool = False, last: bool = False):
        self._nlp: spacy.lang = nlp
        self._after: str = after
        self._before: str = before
        self._path: str = path
        self._name: str = name
        self._first: str = first
        self._last: str = last

    
    def add_pipe(self) -> None:

        try:

            ruler = self._nlp.add_pipe("entity_ruler", before=self._before, after=self._after , name=self._name)

            ruler.from_disk(self._path)

        except ValueError as e:
            """The pipe already exists"""
            pass


        