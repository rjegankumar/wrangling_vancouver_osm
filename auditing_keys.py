# importing libraries and modules
import xml.etree.cElementTree as ET
import pprint
import re

OSM_FILE = 'small_sample.osm' # vancouver_osm.osm is the original file

# compiling re patterns to categorize keywords
caps = re.compile(r'^([A-Z]+[_A-Za-z0-9]*)$')
lower_num = re.compile(r'^([a-z0-9]+)(_[a-z0-9]+)*$')
lower_num_one_colon_caps = \
re.compile(r'^([a-z0-9]+)(_[a-z0-9]+)*:([a-z0-9]+)[A-Z]([a-z0-9]+)$')
lower_num_one_colon_all_caps = \
re.compile(r'^([a-z0-9]+)(_[a-z0-9]+)*:([A-Z]+)$')
lower_num_one_colon_multi_caps = \
re.compile(r'^(([a-z0-9]+)(_[a-z0-9]+)*:)+([A-Z]+)(_[a-z0-9]+)*$')
lower_num_colon = \
re.compile(r'^(([a-z0-9]+)(_[a-z0-9]+)*:)+([a-z0-9]+)(_[a-z0-9]+)*$')
problemchars = re.compile(r'[-=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# matching keywords to the patterns above
def key_type():
    keys = {"caps": 0, "lower_num": 0, "lower_num_one_colon_caps": 0, \
            "lower_num_one_colon_all_caps": 0, "lower_num_colon": 0, \
            "lower_num_one_colon_multi_caps": 0, "problemchars": 0, "others": 0}
    print 'tag key types with counts:\n'
    for _, element in ET.iterparse(OSM_FILE):
        if element.tag == "tag":
            if re.search(caps, element.attrib['k']):
                keys['caps'] += 1
            elif re.search(lower_num, element.attrib['k']):
                keys['lower_num'] += 1
            elif re.search(lower_num_one_colon_caps, element.attrib['k']):
                keys['lower_num_one_colon_caps'] += 1
            elif re.search(lower_num_one_colon_all_caps, element.attrib['k']):
                keys['lower_num_one_colon_all_caps'] += 1
            elif re.search(lower_num_one_colon_multi_caps, element.attrib['k']):
                keys['lower_num_one_colon_multi_caps'] += 1
            elif re.search(lower_num_colon, element.attrib['k']):
                keys['lower_num_colon'] += 1
            elif re.search(problemchars, element.attrib['k']):
                keys['problemchars'] += 1
            else:
                keys['others'] += 1
    return keys

pprint.pprint(key_type())