# importing libraries and modules
import xml.etree.cElementTree as ET
import pprint
import random

OSM_FILE = 'small_sample.osm' # vancouver_osm.osm is the original file

# identifying and counting all tags in the osm file
def count_tags(osm_file):
    tags_dict = {}
    for _, elm in ET.iterparse(osm_file):
        if elm.tag in tags_dict:
            tags_dict[elm.tag] += 1
        else:
            tags_dict[elm.tag] = 1
    return tags_dict

# uncomment below lines to see the output:

#print '\nAll tags:\n'
#pprint.pprint(count_tags(OSM_FILE))
#print ''

# displaying examples of all osm elements
def tags_example(osm_file, t_keys):
    print '\nExamples of all osm elements:\n'
    for tag in t_keys:
        for _, elm in ET.iterparse(osm_file):
            if elm.tag == tag:
                print ET.tostring(elm)
                break

# uncomment below lines to see the output:

#tags = count_tags(OSM_FILE)
#tag_keys = tags.keys() 
#tag_keys.remove('osm')
#tags_example(OSM_FILE, tag_keys)

# identifying and displaying attributes and tags of node and way elements
def count_elm_tags_attribs(osm_file, ts = ['node','way']):
    elm_attr = {'node_attr':{},'way_attr':{}}
    elm_tag = {'node_tag':{},'way_tag':{}}
    for _, elm in ET.iterparse(osm_file):
        if elm.tag in ts:
            for attr in elm.attrib:
                if attr in elm_attr['{}_attr'.format(elm.tag)]:
                    elm_attr['{}_attr'.format(elm.tag)][attr] += 1
                else:
                    elm_attr['{}_attr'.format(elm.tag)][attr] = 1
            for e in elm.iter():
                if e.tag not in ts:
                    if e.tag in elm_tag['{}_tag'.format(elm.tag)]:
                        elm_tag['{}_tag'.format(elm.tag)][e.tag] += 1
                    else:
                        elm_tag['{}_tag'.format(elm.tag)][e.tag] = 1
    print 'Attributes and tags of node and way elements:\n'
    pprint.pprint(elm_attr)
    print ''
    pprint.pprint(elm_tag)
    print ''

# uncomment below lines to see the output:

#count_elm_tags_attribs(OSM_FILE)

# displaying the top 'tag' keys 
def tag_keys(osm_file):
    t_k = {}
    for _, elm in ET.iterparse(osm_file):
        if elm.tag == 'tag':
            if elm.attrib['k'] in t_k:
                t_k[elm.attrib['k']] += 1
            else:
                t_k[elm.attrib['k']] = 1
    return sorted(t_k, key=t_k.get, reverse=True)[:10]

# uncomment below lines to see the output:

#pprint.pprint(tag_keys(OSM_FILE)) #node tag - name:en might need cleanup

# displaying random 'tag' values of top 'tag' keys
def tag_values(osm_file):
    for k in tag_k:
        print "\n'{0}' values in element:\n".format(k)
        values = []
        for _,elm in ET.iterparse(osm_file):
            if elm.tag == 'tag' and elm.get('k') == k:
                values.append(elm.get('v'))
        pprint.pprint(random.sample(values,5))
    print ''

# uncomment below lines to see the output:

#tag_k = tag_keys(OSM_FILE)
#tag_values(OSM_FILE) 