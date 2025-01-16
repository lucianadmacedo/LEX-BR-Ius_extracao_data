### use this script with caution ###

import re

def remove_extra_closing_tags(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regular expression to find redundant closing </modificacao> tags
    # Matches </modificacao> tags that follow another </modificacao> without opening a new tag
    pattern = r"(</modificacao_\d{4}>\n\s.\w.*\n)(</modificacao>)"

    # Remove only the extra closing tags
    cleaned_content = re.sub(pattern, r"\1", content)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

    print(f"Extra </modificacao> tags removed. Cleaned file saved as {output_file}")

def remove_specific_tags(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define the tags to be removed
    tags_to_remove = [r"</artigo>", r"</tachado>", r"<tachado>", r"<artigo>"]

    # Iterate through the list and remove each tag
    for tag in tags_to_remove:
        content = re.sub(tag, "", content)
    
    # Define the tags to remove completely (including their content)
    tags_to_remove_with_content = [r"<(modificacao|titulo|capitulo|texto|ementa|norma|abertura|promulgacao|assinatura|publicacao|q)>.*? </(modificacao|titulo|capitulo|texto|ementa|norma|abertura|promulgacao|assinatura|publicacao|q)>"]

    # Remove tags with their content
    for tag in tags_to_remove_with_content:
        content = re.sub(tag, "", content, flags=re.DOTALL)

    # Write the cleaned content to a new file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Specified tags removed. Cleaned file saved as {output_file}")

# Specify input and output files
input_file = 'tags_com_ano.xml'
output_file = 'tags_com_ano.xml'


# Run the functions
remove_extra_closing_tags(input_file, output_file)
remove_specific_tags(input_file, output_file)
