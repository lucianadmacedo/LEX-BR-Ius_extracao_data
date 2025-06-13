import re

def extract_modificacao_tags(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regex to match all <modificacao_YEAR> tags and their content
        pattern = r"<modificacao_\d{4}>.*?</modificacao_\d{4}>"
        
        # Find all matches
        matches = re.findall(pattern, content, flags=re.DOTALL)
        
        # Write matches to a new file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("\n".join(matches))
        
        print(f"Extracted {len(matches)} <modificacao_YEAR> tags. Saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify input and output files
input_file = 'arquivo_com_tags_revisado.xml'
output_file = 'modificacao_tags_extracted.xml'

# Run the function
extract_modificacao_tags(input_file, output_file)