import re
from lxml import etree

def extract_year(modificacao_text):
    # Use regular expression to extract the year between parentheses
    match = re.search(r'\((\d{4})\)', modificacao_text)
    if match:
        return match.group(1)
    return None

def process_xml(xml_file_path):
    # Parse the XML file
    tree = etree.parse(xml_file_path)

    # Iterate through the XML elements
    for modificacao_elem in tree.xpath(".//modificacao"):
        year = extract_year(modificacao_elem.text)
        if year is not None:
            print(f"Extracted year: {year}")

            # Create new tags with the year appended to their names
            new_tag_name = f"modificacao_{year}"
            new_open_tag = etree.Element(new_tag_name)
            new_close_tag = etree.Element("/" + new_tag_name)

            # Rename the original modificacao tags
            modificacao_elem.tag = new_tag_name

            print(f"Renamed tag: {new_tag_name}")

            # Insert the new tags into the XML tree
            modificacao_elem.addprevious(new_open_tag)
            new_open_tag.addnext(new_close_tag)

    # Write the modified XML back to file
    tree.write("modified_file.xml", encoding="UTF-8", xml_declaration=True)

# Replace 'your_file.xml' with the actual path to your XML file
xml_file_path = 'your_file.xml'
process_xml(xml_file_path)
