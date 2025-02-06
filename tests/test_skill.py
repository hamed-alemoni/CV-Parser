import unittest
import spacy
from spacy.tokens import Span, Doc

# Mock dependencies
from unittest.mock import patch

# Import the Skill class
from skill import Skill  # Replace 'your_module' with the correct module name


class TestSkillExtraction(unittest.TestCase):

    def setUp(self):
        """Set up a blank spaCy English model for testing."""
        self.nlp = spacy.load("en_core_web_md")

    def create_doc_with_entities(self, text: str, ents: list) -> Doc:
        """
        Creates a spaCy Doc from text and assigns given entities.
        """
        doc = self.nlp(text)
        doc.ents = ents
        return doc

    @patch("skill.find_text", return_value="Python, Java, and C++ are my skills.")
    @patch("skill.get_unique_list", side_effect=lambda x: list(dict.fromkeys(x)))
    def test_extract_skills(self, mock_find_text, mock_get_unique_list):
        """
        Test that skills are correctly extracted from text.
        """
        text = "Python, Java, and C++ are my skills."
        doc = self.nlp(text)
        
        # Simulate recognized skills
        skills_spans = [
            Span(doc, 0, 1, label="SKILL"),  # "Python"
            Span(doc, 2, 3, label="SKILL"),  # "Java"
            Span(doc, 5, 6, label="SKILL")   # "C++"
        ]
        doc.ents = skills_spans

        # Instantiate Skill class with mock NLP
        skill_instance = Skill(text, self.nlp)
        skill_instance._nlp = lambda txt: doc  # Override NLP processing

        extracted_skills = skill_instance.extract()
        expected_skills = ["Python", "Java", "C++"]

        self.assertEqual(extracted_skills, expected_skills)

    @patch("skill.find_text", return_value="No skills mentioned.")
    @patch("skill.get_unique_list", side_effect=lambda x: list(dict.fromkeys(x)))
    def test_extract_no_skills(self, mock_find_text, mock_get_unique_list):
        """
        Test that an empty list is returned when no skills are present.
        """
        text = "No skills mentioned."
        doc = self.nlp(text)
        doc.ents = []  # No skill entities

        skill_instance = Skill(text, self.nlp)
        skill_instance._nlp = lambda txt: doc  # Override NLP processing

        extracted_skills = skill_instance.extract()
        self.assertEqual(extracted_skills, [])

    @patch("skill.find_text", return_value="Python, Java, Python, and C++ are my skills.")
    @patch("skill.get_unique_list", side_effect=lambda x: list(dict.fromkeys(x)))
    def test_extract_duplicate_skills(self, mock_find_text, mock_get_unique_list):
        """
        Test that duplicate skills are removed.
        """
        text = "Python, Java, Python, and C++ are my skills."
        doc = self.nlp(text)
        
        # Simulate recognized skills (with duplicates)
        skills_spans = [
            Span(doc, 0, 1, label="SKILL"),  # "Python"
            Span(doc, 2, 3, label="SKILL"),  # "Java"
            Span(doc, 4, 5, label="SKILL"),  # "Python" (duplicate)
            Span(doc, 7, 8, label="SKILL")   # "C++"
        ]
        doc.ents = skills_spans

        skill_instance = Skill(text, self.nlp)
        skill_instance._nlp = lambda txt: doc  # Override NLP processing

        extracted_skills = skill_instance.extract()
        expected_skills = ["Python", "Java", "C++"]  # Duplicates removed

        self.assertEqual(extracted_skills, expected_skills)


if __name__ == '__main__':
    unittest.main()
