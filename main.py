from tika import parser
from emails import Email
import spacy
from cleaning import DataCleaning
from education import Education
from expertise import Expertise
from fullname import Fullname
from phone_number import PhoneNumber
from skill import Skill
from language import Language
from experience import Experience

def read_text() -> str:
    file = r'F:/CV analyer/CV Parser/others/data/data/INFORMATION-TECHNOLOGY/12635195.pdf'
    file_data = parser.from_file(file)
    text = file_data['content']
    return text


def main() -> None:
    import pandas as pd
    cm_data = pd.read_csv('raw_computer_dataset.csv', index_col="Unnamed: 0")
    from data_extractor import DataExtraction
    nlp = spacy.load("en_core_web_md")

    indexes: int = []
    languages: list[str] = []
    educations: list[str] = []
    skills: list[str] = []
    expertise: list[str] = []
    experiences: list[str] = []
    texts: list[str] = []
    for i, text in enumerate(cm_data['Resume_test']):
        data = DataExtraction(text, nlp).extract()
    # text: str = read_text()

        indexes.append(i)
        languages.append(data.language)
        educations.append(data.education)
        skills.append(data.skill)
        expertise.append(data.expertise)
        experiences.append(data.experience)
        texts.append(text)
        print(f'{i}. {data}')

        print("-" * 100)
    
    import pandas as pd

    # Example data
    data = {
        "index": indexes,
        "language": languages,
        "experience": experiences,
        "expertise": expertise,
        "education": educations,
        "skill": skills,
        'text': texts
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    output_path = "output.csv"
    df.to_csv(output_path, index=False)

    print(f"CSV file saved successfully at {output_path}")


if __name__ == "__main__":
    main()


