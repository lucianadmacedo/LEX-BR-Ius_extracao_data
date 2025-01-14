from lxml import etree

def fix_mismatched_tags(input_file, output_file):
    try:
        # Parse the XML file
        parser = etree.XMLParser(recover=True, remove_blank_text=True)
        tree = etree.parse(input_file, parser)

        # Write the corrected XML to the output file
        with open(output_file, 'wb') as f:
            tree.write(f, pretty_print=True, encoding='UTF-8', xml_declaration=True)

        print(f"Corrected XML written to {output_file}")
    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")

# Specify input and output files
input_file = 'annotated_tags.xml'
output_file = 'annotated_tags.xml'

# Run the script
fix_mismatched_tags(input_file, output_file)
