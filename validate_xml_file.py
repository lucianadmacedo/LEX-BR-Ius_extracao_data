from lxml import etree

def clean_xml(input_file, output_file):
    # Parse the XML file
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(input_file, parser)
        root = tree.getroot()

        # Write the cleaned XML to the output file
        with open(output_file, 'wb') as f:
            tree.write(f, pretty_print=True, encoding='UTF-8', xml_declaration=True)

        print(f"Cleaned XML written to {output_file}")
    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")

# Specify input and output files
input_file = 'annotated_tags.xml'
output_file = 'annotated_tags.xml'

# Run the cleaning function
clean_xml(input_file, output_file)
