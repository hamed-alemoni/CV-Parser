import unittest
import spacy
from spacy.tokens import Span, Doc

# Import the class to test. Adjust the module name as needed.
from expertise import Expertise  # Replace 'your_module' with the correct module name
from add_pipeline import Pipeline

class TestExpertiseExtraction(unittest.TestCase):

    def setUp(self):
        # Use a blank English model for testing.
        self.nlp = spacy.load("en_core_web_md")

        # add pipeline
        path: str = "patterns/expertises.jsonl"
        Pipeline(nlp=self.nlp, path=path, name='expertise', before='ner').add_pipe()

    def create_doc_with_entities(self, text: str, ents: list) -> Doc:
        """
        Creates a Doc from the given text and assigns the provided list of Span objects as entities.
        """
        doc = self.nlp(text)
        doc.ents = ents
        return doc

    def test_extract_with_expertise(self):
        # Prepare the text.
        text = "I have expertise Machine Learning"
        # Create a Doc from the text.
        doc = self.nlp(text)
        # Assume tokens: ["I", "have", "expertise", "Machine", "Learning"]
        # We want the Expertise entity to cover "Machine Learning".
        expertise_span = Span(doc, 3, 5, label="Expertise")
        doc.ents = [expertise_span]

        # Create an Expertise instance.
        expertise_instance = Expertise(text, self.nlp)
        # Monkey-patch _nlp so that extract() returns our pre-built doc.
        expertise_instance._nlp = lambda txt: doc

        # Call extract() and verify that it returns the expected expertise text.
        self.assertEqual(expertise_instance.extract(), {"Machine Learning"})

    def test_extract_without_expertise(self):
        # Text with no Expertise entity.
        text = "I have no relevant skills."
        doc = self.nlp(text)
        # No entities assigned.
        doc.ents = []

        expertise_instance = Expertise(text, self.nlp)
        expertise_instance._nlp = lambda txt: doc

        self.assertEqual(expertise_instance.extract(), set())

    def test_extract_first_expertise_only(self):
        # In case there are multiple Expertise entities, the method should return the first one.
        text = "I have expertise in AI and also expertise in ML."
        doc = self.nlp(text)
        # For simplicity, we manually create two Expertise spans.
        # Adjust token indices based on how the text is tokenized.
        # Let's assume tokens are: ["I", "have", "expertise", "in", "AI", "and", "also", "expertise", "in", "ML", "."]
        span1 = Span(doc, 2, 5, label="Expertise")  # covers "expertise in AI"
        span2 = Span(doc, 7, 10, label="Expertise")  # covers "expertise in ML"
        doc.ents = [span1, span2]

        expertise_instance = Expertise(text, self.nlp)
        expertise_instance._nlp = lambda txt: doc

        # The extract method returns the text of the first Expertise entity.
        self.assertEqual(expertise_instance.extract(), {span1.text.strip(), span2.text.strip()})


if __name__ == '__main__':
    unittest.main()
