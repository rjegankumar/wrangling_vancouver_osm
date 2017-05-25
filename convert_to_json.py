import xml.etree.cElementTree as ET
import re
import codecs
import json

osm_file = 'vancouver_osm.osm'

OSM_FILE = 'small_sample.osm' # vancouver_osm.osm is the original file

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
    if re.search(caps, key):
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

xxxstreet = re.compile(r'[A-Za-z]+street')

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

postcodes_re_space = re.compile(r'^V[1-7][A-Z]\d[A-Z]\d$')
postcodes_re = re.compile(r'^V[1-7][A-Z] \d[A-Z]\d$')

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

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        node['id'] = element.attrib['id']
        node['type'] = element.tag
        node['created'] = {}
        if 'lat' in element.attrib and 'lon' in element.attrib:
            node['pos'] = [0,0]
        for attr in element.attrib:
            if attr in CREATED:
                node['created'][attr] = element.attrib[attr]
            elif attr  == 'lat':
                node['pos'][0] = float(element.attrib[attr])
            elif attr == 'lon':
                node['pos'][1] = float(element.attrib[attr])
            else:
                node[attr] = element.attrib[attr]
        for tag in element.iter('tag'):
            result = update_key(tag.attrib['k'])
            if result:
                if type(result) is list and len(result) > 2:
                    continue
                elif result[0] == 'address':
                    if 'address' not in node.keys():
                        node['address'] = {}
                    if result[1] == 'street':
                        node['address']['street'] = update_street_name(tag.attrib['v'])
                    elif result[1] == 'postcode':
                        new_postcode = update_postcode(tag.attrib['v'])
                        if new_postcode:
                            node['address']['postcode'] = update_postcode(new_postcode)
                    else:
                        node['address'][result[1]] = tag.attrib['v']
                elif type(result) is list and len(result) == 2:
                    if result[0] not in node.keys():
                        node[result[0]] = {}
                    if type(node[result[0]]) is not dict:
                        node[result[0]] = {result[0]: node[result[0]]}
                    node[result[0]][result[1]] = tag.attrib['v']
                elif result == 'phone':
                    new_phone = update_phone_num(tag.attrib['v'])
                    if new_phone:
                        node['phone'] = new_phone
                elif result == 'type':
                    continue
                else:
                    node[result] = tag.attrib['v']
        for nd in element.iter('nd'):
            if nd.attrib['ref']:
                if 'node_refs' not in node.keys():
                    node['node_refs'] = []
                node['node_refs'].append(nd.attrib['ref'])
        return node
    else:
        return None

def process_map():
    file_out = "{0}.json".format(osm_file[:-4])
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(osm_file):
            el = shape_element(element)
            if el:
                data.append(el)
                fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map()
    print len(data)

if __name__ == "__main__":
    test()