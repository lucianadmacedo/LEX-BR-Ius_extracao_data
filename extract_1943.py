import xml.etree.ElementTree as ET

# Load and parse the original XML file
tree = ET.parse('your_file.xml')
root = tree.getroot()

# Function to extract texts not followed by <modificacao> and save to a new XML
def extract_and_save_texts(root, output_file):
    # Create a new root for the new XML
    new_root = ET.Element("root")  # Or choose a different name for the root element
    
    # Initialize a list to hold the previous element
    prev_element = None

    for element in root.iter():
        # Check if the element has text and if it's not immediately followed by <modificacao>
        if element.text and (prev_element is None or prev_element.tag != 'modificacao'):
            # Create a new element for each valid text
            new_element = ET.SubElement(new_root, "text")
            new_element.text = element.text.strip()
        
        # Set the current element as the previous one for the next iteration
        prev_element = element

    # Write the new tree to a file
    new_tree = ET.ElementTree(new_root)
    new_tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Call the function and save the new XML
output_file = 'output.xml'
extract_and_save_texts(root, output_file)
