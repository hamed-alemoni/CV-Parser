import unittest
import spacy
from education import Education  # Replace 'your_module' with the actual module name
from add_pipeline import Pipeline
class TestEducation(unittest.TestCase):
    def setUp(self):
        self.nlp = spacy.load("en_core_web_md")
        # add pipeline
        path: str = "patterns/majors.jsonl"
        Pipeline(self.nlp, path, 'Major', before='tok2vec').add_pipe()
        self.education = Education("I have a BSc in Computer Science and an MSc in Data Science.", self.nlp)

    def test_extract_single_degree(self):
        edu = Education("BSc in Computer Science", self.nlp)
        self.assertEqual(edu.extract(), ["Bsc In Computer Science"])
    
    def test_extract_multiple_degrees(self):
        edu = Education("I have a BSc in Computer Science and an MSc in Data Science.", self.nlp)
        self.assertEqual(edu.extract(), ["Bsc In Computer Science", "Msc In Data Science"])
    
    def test_extract_no_degree(self):
        edu = Education("I studied something unrelated.", self.nlp)
        self.assertEqual(edu.extract(), [])
    
    def test_extract_with_unknown_field(self):
        edu = Education("I have a Bachelors.", self.nlp)
        self.assertEqual(edu.extract(), [])
    
    def test_extract_with_and_or(self):
        edu = Education("MSc in Computer Science and Artificial Intelligence", self.nlp)
        expected_results = [
            ["Msc In Artificial Intelligence And Computer Science"],
            ["Msc In Computer Science And Artificial Intelligence"]
        ]
        self.assertIn(edu.extract(), expected_results)

if __name__ == "__main__":
    unittest.main()
