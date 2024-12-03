import re
from lxml import etree
import os

def extract_year(modificacao_text):
    # Use regular expression to extract the year between parentheses
    match = re.search(r'\((Red.+|Inciso.+|Parágrafo incluído.+|Alínea incluída.+|Restabelecido com nova redação.+|inclui.+|alterado.+|Incluí.+)', modificacao_text)
    if match is None:
        return None
    match = re.search(r'[0-9]{4}', match.group(0))  # Extract the year
    if match:
        return match.group(0)
    return None

def rename_modificacao_tags(xml_file_path):
    # Parse the XML file
    tree = etree.parse(xml_file_path)
    root = tree.getroot()

    # Iterate through the XML elements
    for modificacao_elem in root.xpath(".//modificacao"):
        year = extract_year(modificacao_elem.text)
        if year is not None:
            # Rename the original modificacao tags to include the year
            new_tag_name = f"modificacao_{year}"
            modificacao_elem.tag = new_tag_name
            print(f"Renamed tag: {new_tag_name}")

    # Create a new output file name by appending "_modified" to the original filename
    file_name, file_extension = os.path.splitext(xml_file_path)
    output_file_path = f"{file_name}_modified{file_extension}"

    # Write the modified XML back to a new file
    tree.write(output_file_path, encoding="UTF-8", xml_declaration=True)
    print(f"Modified XML saved to: {output_file_path}")

# Replace 'your_file.xml' with the actual path to your XML file
xml_file_path = 'your_file.xml'
rename_modificacao_tags(xml_file_path)