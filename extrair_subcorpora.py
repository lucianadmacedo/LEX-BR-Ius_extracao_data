import xml.etree.ElementTree as ET
import re
from pathlib import Path

def extract_texts_by_year(xml_file):
    # Load the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create a dictionary to hold the extracted texts by year
    texts_by_year = {}

    # Loop through all elements in the XML file
    for elem in root.iter():
        # Check if the tag matches the pattern 'modificacao_YYYY'
        match = re.match(r'modificacao_(\d{4})', elem.tag)
        if match:
            year = match.group(1)
            # Get the text inside the tag
            text = elem.text.strip() if elem.text else ''
            # Add the text to the dictionary
            if year not in texts_by_year:
                texts_by_year[year] = []
            texts_by_year[year].append(text)

    # Save the extracted texts to separate files
    for year, texts in texts_by_year.items():
        file_path = Path(f'modificacao_{year}.txt')
        with file_path.open('w', encoding='utf-8') as f:
            for text in texts:
                f.write(text + '\n')

    print(f"Extracted texts have been saved into separate files by year.")

# Example usage
extract_texts_by_year('annotated_tags.xml')
