
import json

from client import JumbleClient

def main():
    jc = JumbleClient()
    with open('testdata/uclick/0101.xml', 'r') as f:
        xml_string = f.read()
    details = jc.parse_jumble_xml(xml_string)
    print(json.dumps(details, indent=2))

main()