# importing libraries and modules
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

OSM_FILE = 'small_sample.osm' # vancouver_osm.osm is the original file

# a list of expected street names
expected_street_names = ["Street", "Avenue", "Boulevard", "Drive", "Court", 
                         "Place", "Square", "Lane", "Road", "Trail", "Parkway", 
                         "Commons", "Broadway", "Mall", "Way", "Venue", "Walk",
                         "Highway", "Crossing", "Alley", "Crescent", "Esplanade",
                         "Kingsway", "Terminal","Connector","Mews","Seawall"]

# regex pattern to find street types used in addr:street
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# function to print all addr:street values that are unexpected
def audit_street_type():
    street_types = defaultdict(set)
    for _, elm in ET.iterparse(OSM_FILE):
        if elm.tag in ["node","way"]:
            for e in elm.iter("tag"):
                if e.get('k') == 'addr:street':
                    street_name = e.get('v')
                    m = street_type_re.search(street_name)
                    if m:
                        street_type = m.group()
                        if street_type not in expected_street_names:
                            street_types[street_type].add(street_name)
    pprint.pprint(dict(street_types))

audit_street_type()