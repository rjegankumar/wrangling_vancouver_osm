import xml.etree.cElementTree as ET
import re
import pprint

OSM_FILE = 'small_sample.osm' # vancouver_osm.osm is the original file

# regex pattern to help correct the postal codes
postcodes_re_space = re.compile(r'^V[1-7][A-Z]\d[A-Z]\d$')
postcodes_re = re.compile(r'^V[1-7][A-Z] \d[A-Z]\d$')

# function to clean up the postal codes to conform to the standard format
def update_postcode(pc):
    pc = pc.upper()
    if ';' in pc:
        pc = pc.split(';')[1]
    if pc[:3] == 'BC ':
        pc = pc.strip('BC ')
    if pc[-1] == ',':
        pc = pc.strip(',')
    if postcodes_re_space.search(pc):
        pc = pc[:3]+' '+pc[3:]
    if postcodes_re.search(pc):
        return pc
    else:
        return None

# Creating a list of updated postal codes

updated_postcodes = []

for _, elm in ET.iterparse(OSM_FILE):
    if elm.tag in ["node","way"]:
        for e in elm.iter("tag"):
            if e.get('k') == 'addr:postcode':
                postcode = e.get('v')
                updated_postcodes.append(update_postcode(postcode))

print len(updated_postcodes)

# function to print all postal codes that do not conform to the std. format
def audit_postcodes():
    postcodes = set()
    none = 0
    for p in updated_postcodes:
        if p:
            if not postcodes_re.search(p):
                postcodes.add(p)
        else:
            none += 1
    print none
    pprint.pprint(postcodes)

audit_postcodes()