import re
from pathlib import Path

def extract_texts_by_year(xml_file):
    # Read the file content as a string
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File {xml_file} not found.")
        return

    # Use regex to match all <modificacao_YEAR> tags and their content
    pattern = r"<modificacao_(\d{4})>(.*?)</modificacao_\1>"
    matches = re.findall(pattern, content, flags=re.DOTALL)

    # Create a dictionary to hold the extracted texts by year
    texts_by_year = {}

    # Organize matches into the dictionary
    for year, text in matches:
        text = text.strip()  # Remove leading and trailing whitespace
        if year not in texts_by_year:
            texts_by_year[year] = []
        texts_by_year[year].append(text)

    # Save the extracted texts to separate files by year
    for year, texts in texts_by_year.items():
        file_path = Path(f'modificacao_{year}.txt')
        with file_path.open('w', encoding='utf-8') as f:
            for text in texts:
                f.write(text + '\n')

    print(f"Extracted texts have been saved into separate files by year.")

# Example usage
extract_texts_by_year('modificacao_tags_extracted.xml')