import re
from pathlib import Path

def extract_non_modificacao_texts(xml_file, output_file):
    # Read the file content as plain text
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File {xml_file} not found.")
        return

    # Remove all <modificacao_*> tags and their content
    content_without_modificacao = re.sub(r"<modificacao_\d{4}>.*?</modificacao_\d{4}>", "", content, flags=re.DOTALL)

    # Extract all remaining text outside any tags
    non_tagged_texts = re.findall(r">([^<]+)<", content_without_modificacao)

    # Create the new XML structure
    new_root = "<root>\n"
    for text in non_tagged_texts:
        cleaned_text = text.strip()  # Remove extra spaces
        if cleaned_text:  # Skip empty lines
            new_root += f"  <text>{cleaned_text}</text>\n"
    new_root += "</root>"

    # Save the output to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(new_root)

    print(f"Extracted texts have been saved to {output_file}.")

# Example usage
xml_file = 'tags_com_ano.xml'
output_file = 'original_1943.txt'
extract_non_modificacao_texts(xml_file, output_file)