import xml.etree.cElementTree as ET
import re
import pprint

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

# creating a function to update or correct the keywords prior to creating db

def update_key(key):
    if key.split(':')[0] == 'addr':
        key = key[:4]+'ess'+key[4:]
    elif re.search(caps, key):
        return key.lower()
    elif re.search(lower_num, key):
        return key
    elif re.search(lower_num_one_colon_caps, key):
        key_list = key.split(':')
        cap_index = re.search(r'[A-Z]', key_list[1]).start()
        key_list[1] = key_list[1][:cap_index] + '_' + \
        key_list[1][cap_index].lower() + key_list[1][(cap_index+1):]
        return key_list
    elif re.search(lower_num_one_colon_all_caps, key):
         key_list = key.split(':')
         key_list[1] = key_list[1].lower()
         return key_list
    elif re.search(lower_num_one_colon_multi_caps, key):
        key_list = key.split(':')
        under_index = re.search(r'_', key_list[1]).start()
        key_list[1] = key_list[1][:under_index].lower() + '_' + key_list[1][(under_index+1):]
        return key_list
    elif re.search(lower_num_colon, key):
        return key.split(':')
    elif re.search(problemchars, key):
        return None

# creating a list of all of the updated keywords
   
updated_keys = []

for _, element in ET.iterparse(OSM_FILE):
    if element.tag == "tag":
        result = update_key(element.attrib['k'])
        if type(result) is list:
            for i in result:
                updated_keys.append(i)
        else:
            updated_keys.append(result)

print len(updated_keys)

# checking whether the update key function worked correctly

def key_type():
    keys = {"None": 0, "caps": 0, "lower_num": 0, "lower_num_one_colon_caps": 0, \
            "lower_num_one_colon_all_caps": 0, "lower_num_colon": 0, \
            "lower_num_one_colon_multi_caps": 0, "problemchars": 0, "others": 0}
    print 'tag key types with counts:\n'
    for e in updated_keys:
        if e == None:
            keys['lower_num'] += 1
        elif re.search(caps, e):
            keys['caps'] += 1
        elif re.search(lower_num, e):
            keys['lower_num'] += 1
        elif re.search(lower_num_one_colon_caps, e):
            keys['lower_num_one_colon_caps'] += 1
        elif re.search(lower_num_one_colon_all_caps, e):
            keys['lower_num_one_colon_all_caps'] += 1
        elif re.search(lower_num_one_colon_multi_caps, e):
            keys['lower_num_one_colon_multi_caps'] += 1
        elif re.search(lower_num_colon, e):
            keys['lower_num_colon'] += 1
        elif re.search(problemchars, e):
            keys['problemchars'] += 1
        else:
            keys['others'] += 1
    return keys

pprint.pprint(key_type())
