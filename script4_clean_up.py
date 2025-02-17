import re

# Define regex patterns to clean
patterns = [
    (r'^(\w{1,2}\)|§)', ''),  # Matches any word character (letter, digit, underscore) followed by ')'
    (r'^\s+', ''),  # Replaces multiple spaces with a single space
    (r'Art\. \w{1,3}', ''),  # Matches 'Art.' followed by any word character and anything before ' -'
    (r'Parágrafo único', ''),  # Removes "Parágrafo único"
    (r'\((Red.+|Inciso.+|Parágrafo incluído.+|Alínea incluída.+|Restabelecido com nova redação.+|inclui.+|alterado.+|Incluí.+|Revog.+|Vet.+)\)', ''),  # Removes annotations in parentheses
    (r'[IVXLCDM]+\s*-', ''),  # Removes Roman numerals followed by a hyphen
    #(r'[IVXLCDM]+', ''),  # Removes Roman numerals followed by a hyphen
    (r'^(\.|-|\w\))', ''),  # Matches any word character (letter, digit, underscore) followed by ')'
    (r'^\s+', ''),  # Replaces multiple spaces with a single space
    #(r'^\s+|\s+$', '')  # Removes leading and trailing spaces
    (r'^[\W_]+', ''),  # Removes punctuation and underscores at the beginning of the line
    (r'^(\d+º )', ''),
    (r'^(- )', ''),
    (r'^(\w{1})', '')

]

# Define a test file path (update this with your actual file path)
test_file_path = "/workspaces/LEX-BR-Ius_extracao_data/original_1943.txt"  # Change this before running

# Read, process, and save the test file
try:
    with open(test_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Apply regex replacements line by line
    cleaned_lines = []
    for line in lines:
        for pattern, replacement in patterns:
            line = re.sub(pattern, replacement, line)
        cleaned_lines.append(line)  # Keep the lines intact

    # Save the cleaned test file, preserving the line structure
    with open(test_file_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)  # Write the cleaned lines back

    print(f"Cleanup complete for: {test_file_path}")

except FileNotFoundError:
    print("Error: Test file not found. Please check the path.")

except Exception as e:
    print(f"An error occurred: {e}")
