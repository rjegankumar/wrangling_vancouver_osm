import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict

OSM_FILE = 'small_sample.osm' # vancouver_osm.osm is the original file

# re pattern for street names that have a string like "denmanstreet"

xxxstreet = re.compile(r'[A-Za-z]+street')

# dictionary that will be used to map the correct street type

street_name_mapping = {
        re.compile(r'\bAve\b') : 'Avenue',
        re.compile(r'\bBlvd\b') : 'Boulevard',
        re.compile(r'\bDr\b') : 'Drive',
        re.compile(r'\bHwy\b') : 'Highway',
        re.compile(r'\bRd\b') : 'Road',
        re.compile(r'\bSt\b') : 'Street',
        re.compile(r'\bSteet\b') : 'Street',
        re.compile(r'\bst\b') : 'Street',
        re.compile(r'\bstreet\b') : 'Street',
        re.compile(r'\bW\b') : 'West',
        re.compile(r'\bE\b') : 'East',
        re.compile(r'\bS\b') : 'South',
        re.compile(r'\bN\b') : 'North'
        }

# function to correct the street types

def update_street_name(name):
    name = name.replace('.','')
    if '#' in name:
        name = name.split(' #')[0]
    if 'Vancouver' in name:
        name = name.split(' Vancouver')[0]
    if re.search(xxxstreet, name):
        street = re.compile(r'street')
        s1 = re.search(xxxstreet, name)
        s2 = re.search(street, name[s1.start():s1.end()])
        name = name[:s2.start()]+' '+name[s2.start()].upper()\
        +name[(s2.start()+1):]
    for st_abbr, st_full in street_name_mapping.iteritems():
        if re.search(st_abbr, name):
            s = re.search(st_abbr, name)
            name = name[:s.start()]+st_full+name[s.end():]
    return name

# creating a list of all of the updated street names
   
updated_street_names = []

for _, elm in ET.iterparse(OSM_FILE):
    if elm.tag in ["node","way"]:
        for e in elm.iter("tag"):
            if e.get('k') == 'addr:street':
                street_name = e.get('v')
                result = update_street_name(street_name)
                updated_street_names.append(result)

print len(updated_street_names)

# a list of expected street names
expected_street_names = ["Street", "Avenue", "Boulevard", "Drive", "Court", 
                         "Place", "Square", "Lane", "Road", "Trail", "Parkway", 
                         "Commons", "Broadway", "Mall", "Way", "Venue", "Walk",
                         "Highway", "Crossing", "Alley", "Crescent", "Esplanade",
                         "Kingsway", "Terminal","Connector","Mews","Seawall"]

# regex pattern to find street types used in addr:street
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# function to audit street types
def audit_street_type():
    street_types = defaultdict(set)
    for street_name in updated_street_names:
        m = street_type_re.search(street_name)
        if m:
            street_type = m.group()
            if street_type not in expected_street_names:
                street_types[street_type].add(street_name)
    pprint.pprint(dict(street_types))

audit_street_type()
