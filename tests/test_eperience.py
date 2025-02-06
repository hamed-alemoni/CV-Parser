import unittest
import os
os.chdir('..')
from experience import Experience
import unittest
import os
os.chdir('..')
from experience import Experience

class TestExperienceExtraction(unittest.TestCase):
    def setUp(self):
        # Set up sample resume texts for testing
        self.resume_with_exp_in_years = "I have over 5 years of experience in software development."
        self.resume_with_exp_in_words = "Worked as a developer for five years in total."
        self.resume_with_dates = "From January 2010 to March 2020, I worked as a software engineer."
        self.resume_with_no_exp = "I am a recent graduate with a degree in Computer Science."
        self.resume_with_spelled_out_numbers = "I have worked for twenty-three years in the field of AI."
        self.resume_with_hyphenated_numbers = "I have twenty-two years of experience."
        self.resume_with_fractions = "I worked for 1 5/6 years as a manager."
        self.resume_with_decimals = "I have 2.5 years of experience."
        self.resume_with_multiple_mentions = "5 years in development and 3 years in management." ###
        self.resume_with_months = "I worked for 24 months as a research assistant."
        self.resume_with_no_time_units = "I worked in software development."
        self.resume_with_abbreviations = "I have 10 yrs of experience as a data scientist."
        self.resume_with_single_year = "1 year of experience in marketing."
        self.resume_with_mixed_time = "I have 3 years and 6 months of work experience."
        self.resume_with_years_and_months = "Worked 2 years and 8 months in project management."
        self.resume_with_uncertain_format = "I have worked in AI for a period of two-three years."
        self.resume_with_partial_dates = "I started working in 2010 and left in 2016."
        self.resume_with_multiple_date_ranges = "I have experienced From January 2010 to March 2015 and from 2017 to 2020."
        self.resume_with_invalid_time = "I worked on a project for 6 months, no specific time mentioned."
        self.resume_with_just_numbers = "I have 30 years of experience."
        self.resume_with_mixed_units = "1 year and 6 months (approx. 18 months) of experience."
        self.resume_with_partial_words = "I worked for half a year."
        self.resume_with_approximate_duration = "Around 2 years of experience."
        self.resume_with_date_and_duration = "Worked from 2010 to 2015 for 5 years in total."
        self.resume_with_containing_experiences = "I have 15 years of AI which 5 years of it was in Apple"
        self.resume_with_dates_with_slash = "I have worked from 1/2014 to 2/2020 in Google"
        self.resume_with_dates_month_attach_year = 'job work working work working 042019 to 092020'
        self.resume_with_only_days = "I have worked for 1023 days in the past"

    def test_experience_from_years(self):
        experience = Experience(self.resume_with_exp_in_years).extract()
        self.assertEqual(experience, 5)

    def test_experience_from_words(self):
        experience = Experience(self.resume_with_exp_in_words).extract()
        self.assertEqual(experience, 5)

    def test_experience_from_dates(self):
        experience = Experience(self.resume_with_dates).extract()
        self.assertEqual(experience, 10)

    def test_no_experience(self):
        experience = Experience(self.resume_with_no_exp).extract()
        self.assertEqual(experience, 0)

    def test_experience_with_spelled_out_numbers(self):
        experience = Experience(self.resume_with_spelled_out_numbers).extract()
        self.assertEqual(experience, 23)

    def test_experience_with_hyphenated_numbers(self):
        experience = Experience(self.resume_with_hyphenated_numbers).extract()
        self.assertEqual(experience, 22)

    def test_experience_with_fractions(self):
        experience = Experience(self.resume_with_fractions).extract()
        self.assertEqual(experience, 1)  # Round to nearest integer

    def test_experience_with_decimals(self):
        experience = Experience(self.resume_with_decimals).extract()
        self.assertEqual(experience, 2)  # Round to nearest integer

    def test_multiple_experience_mentions(self):
        experience = Experience(self.resume_with_multiple_mentions).extract()
        self.assertEqual(experience, 8)

    def test_experience_with_months(self):
        experience = Experience(self.resume_with_months).extract()
        self.assertEqual(experience, 2)  # Convert months to integer years (rounding down)

    def test_experience_with_no_time_units(self):
        experience = Experience(self.resume_with_no_time_units).extract()
        self.assertEqual(experience, 0)

    def test_experience_with_abbreviations(self):
        experience = Experience(self.resume_with_abbreviations).extract()
        self.assertEqual(experience, 10)

    def test_experience_with_single_year(self):
        experience = Experience(self.resume_with_single_year).extract()
        self.assertEqual(experience, 1)

    def test_experience_with_mixed_time(self):
        experience = Experience(self.resume_with_mixed_time).extract()
        self.assertEqual(experience, 3)  # Round to nearest integer

    def test_experience_with_years_and_months(self):
        experience = Experience(self.resume_with_years_and_months).extract()
        self.assertEqual(experience, 2)  # Round to nearest integer year

    def test_experience_with_uncertain_format(self):
        experience = Experience(self.resume_with_uncertain_format).extract()
        self.assertEqual(experience, 2)  # Assuming "two-three" means 2 years (rounding)

    def test_experience_with_partial_dates(self):
        experience = Experience(self.resume_with_partial_dates).extract()
        self.assertEqual(experience, 6)

    def test_experience_with_multiple_date_ranges(self):
        experience = Experience(self.resume_with_multiple_date_ranges).extract()
        self.assertEqual(experience, 8)

    def test_experience_with_invalid_time(self):
        experience = Experience(self.resume_with_invalid_time).extract()
        self.assertEqual(experience, 0)

    def test_experience_with_just_numbers(self):
        experience = Experience(self.resume_with_just_numbers).extract()
        self.assertEqual(experience, 30)

    def test_experience_with_mixed_units(self):
        experience = Experience(self.resume_with_mixed_units).extract()
        self.assertEqual(experience, 1)  # Convert months to integer year

    def test_experience_with_partial_words(self):
        experience = Experience(self.resume_with_partial_words).extract()
        self.assertEqual(experience, 0)  # Half a year is not a full year

    def test_experience_with_approximate_duration(self):
        experience = Experience(self.resume_with_approximate_duration).extract()
        self.assertEqual(experience, 2)  # Round to nearest integer

    def test_experience_with_date_and_duration(self):
        experience = Experience(self.resume_with_date_and_duration).extract()
        self.assertEqual(experience, 5)

    def test_experience_with_containing_experiences(self):
        experience = Experience(self.resume_with_containing_experiences).extract()
        self.assertEqual(experience, 15)

    def test_experience_with_dates_with_slash(self):
        experience = Experience(self.resume_with_dates_with_slash).extract()
        self.assertEqual(experience,6)

    def test_experience_with_month_attach_to_year(self):
        experience = Experience(self.resume_with_dates_month_attach_year).extract()
        self.assertEqual(experience, 1)

    def test_experience_with_days(self):
        experience = Experience(self.resume_with_only_days).extract()
        self.assertEqual(experience, 2)

if __name__ == "__main__":
    unittest.main()


