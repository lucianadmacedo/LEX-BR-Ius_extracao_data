import re
from lxml import etree

def extract_year(modificacao_text):
    # Use regular expression to extract the year between parentheses
    match = re.search(r'\((Red.+|Inciso.+|Parágrafo incluído.+|Alínea incluída.+|Restabelecido com nova redação.+|inclui.+|alterado.+|Incluí.+)', modificacao_text)
    if match is None:
        return None
#    print(match)
#    input('')
    match = re.search('[0-9]{4,4}', match.group(0))
#    print(match.group(0))
#    input('')
    if match:
        return match.group(0)
    return None

def process_xml(xml_file_path):
    # Parse the XML file
    tree = etree.parse(xml_file_path)
    all_texts = [ ]
    # Iterate through the XML elements
    for modificacao_elem in tree.xpath(".//modificacao"): # Probably it will be necessary to check cases
        year = extract_year(modificacao_elem.text)
        print(year)
        if year is not None:
            # Create new tags with the year appended to their names
            new_tag_name = f"modificacao_{year}"
            # Rename the original modificacao tags
            modificacao_elem.tag = new_tag_name
            print(f"Renamed tag: {new_tag_name}")
            parent = modificacao_elem.getparent()
            all_text = ''.join(etree.tostring(child, encoding='unicode', method='text') for child in parent.iter())
            all_text = all_text.split(modificacao_elem.text)[0].strip().split(r'\n')[-1]
            modificacao_elem.text = all_text + modificacao_elem.text
            all_texts.append(all_text)
#            print(modificacao_elem.text)
            # Insert the new tags into the XML tree
    # Write the modified XML back to file
    txt = etree.tostring(tree, encoding = 'unicode')
    for i in all_texts:
        print(i)
        txt = txt.replace(i, '', 1)
#    print(txt)
#    print(etree.tostring(tree))
    with open('modified_file.xml','w') as f:
        f.write(txt)
#    tree.write("modified_file.xml", encoding="UTF-8", xml_declaration=True)

def get_year(bpart):
    yearpart = bpart.split('</modificacao>')[0]
    return (extract_year(yearpart.strip()), yearpart)


def get_previous_text(text):
    return text.split('>')[-1]

def get_text(xml_file_path):
    f2 = open(xml_file_path + 'nu', 'w')
    with open(xml_file_path, 'r') as f:
        text = f.read()
    modtext = text.split('<modificacao>')
    for i in range(len(modtext) - 1):
        write_text(f2, modtext[i], get_year(modtext[i+1]))


def write_text(f2, pretext, year):
    if year[0] is None:
        f2.write(pretext + '<modificacao>' + year[1] + '</modificacao>')
        return 0
    prepretext = get_previous_text(pretext)
    pretext = pretext.split(prepretext)[0]
    pretext = pretext.split('</modificacao>')[-1]
    f2.write(pretext + '\n<modificacao_' + year[0] + '>' + prepretext + year[1] +  '</modificacao_' + year[0] + '>\n')

# Replace 'your_file.xml' with the actual path to your XML file
xml_file_path = 'arquivo_original.xml'
#process_xml(xml_file_path)

get_text(xml_file_path)