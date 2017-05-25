# importing libraries and modules
import xml.etree.cElementTree as ET
import pprint
import re

OSM_FILE = 'small_sample.osm' # vancouver_osm.osm is the original file

# regex pattern to check for postal code formatting
postcodes_re = re.compile(r'^V[1-7][A-Z] \d[A-Z]\d$')

# function to print all postal codes that do not conform to the std. format   
def audit_postcodes():
    postcodes = set()
    for _, elm in ET.iterparse(OSM_FILE):
        if elm.tag in ["node","way"]:
            for e in elm.iter("tag"):
                if e.get('k') == 'addr:postcode':
                    postcode = e.get('v')
                    p = postcodes_re.search(postcode)
                    if not p:
                        postcodes.add(postcode)
    pprint.pprint(postcodes)

audit_postcodes()