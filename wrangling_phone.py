import xml.etree.cElementTree as ET
import re
import pprint

OSM_FILE = 'small_sample.osm' # vancouver_osm.osm is the original file

# function to clean up the phone number formatting

def update_phone_num(num):
    try:
        digits = filter(str.isdigit, num)
        if len(digits) == 11 and digits[0] == '1':
            return digits[1:4]+'-'+ digits[4:7] + '-' + digits[7:11]
        elif len(digits) == 10:
            return digits[0:3]+'-'+ digits[3:6] + '-' + digits[6:10]
        else:
            return None
    except TypeError:
        return None

# Creating a list of updated phone numbers

updated_phone_nums = []

for _, elm in ET.iterparse(OSM_FILE):
    if elm.tag in ["node","way"]:
        for e in elm.iter("tag"):
            if e.get('k') == 'phone':
                phone = e.get('v')
                updated_phone_nums.append(update_phone_num(phone))

print len(updated_phone_nums)

# regex pattern for checking the phone number format
phones_re = re.compile(r'^\d{3}-\d{3}-\d{4}$')

# function to print all phone numbers that are not in the recommended format   
def audit_phone_number():
    phones = set()
    for phone in updated_phone_nums:
        if phone:
            p = phones_re.search(phone)
            if not p:
                phones.add(phone)
    pprint.pprint(phones)

audit_phone_number()
