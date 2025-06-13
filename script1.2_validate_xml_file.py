from lxml import etree

def validate_xml_lxml(file_path):
    try:
        with open(file_path, 'r') as file:
            etree.parse(file)
        print("XML is well-formed.")
        return True
    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error:\n{e}")
        return False

# Example usage
validate_xml_lxml("arquivo_com_tags_revisado.xml")
