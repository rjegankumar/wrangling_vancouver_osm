# importing libraries and modules
import xml.etree.cElementTree as ET
import pprint
import re

OSM_FILE = 'small_sample.osm' # vancouver_osm.osm is the original file

# regex pattern for checking the phone number format
phones_re = re.compile(r'^\d{3}-\d{3}-\d{4}$')

# function to print all phone numbers that are not in the recommended format   
def audit_phone_number():
    phones = set()
    for _, elm in ET.iterparse(OSM_FILE):
        if elm.tag in ["node","way"]:
            for e in elm.iter("tag"):
                if e.get('k') == 'phone':
                    phone = e.get('v')
                    p = phones_re.search(phone)
                    if not p:
                        phones.add(phone)
    pprint.pprint(phones)

audit_phone_number()