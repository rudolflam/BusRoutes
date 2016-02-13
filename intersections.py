import argparse


def find_intersections(file):
    import xml
    from xml.dom.minidom import parse

    data = {}
    keys = []

    ways = {}
    wkeys = []

    relations = {}
    rkeys = []

    dom = xml.dom.minidom.parse(file)
    #  parse out osm nodes
    #
    for n in dom.getElementsByTagName("node"):
        nid = int(n.getAttribute("id"))
        data[nid] = {}
        data[nid]["lat"] = float(n.getAttribute("lat"))
        data[nid]["lon"] = float(n.getAttribute("lon"))
        for tag in n.getElementsByTagName("tag"):
            if(tag.hasAttribute("k")):
                k = tag.getAttribute("k")
                if(k not in keys):
                    keys.append(k)
                if(tag.hasAttribute("v")):
                    data[nid][k] = tag.getAttribute("v")
    # parse out osm ways/polygons
    #
    wids = []
    for n in dom.getElementsByTagName("way"):
        wid = int(n.getAttribute("id"))
        wids.append(wid)
        ways[wid] = {}
        ways[wid]['ref'] = []
        ways[wid]['geomType'] = ""
        ways[wid]['tags'] = {}
        for nd in n.getElementsByTagName('nd'):
            if nd.hasAttribute('ref'):
                ref = nd.getAttribute('ref')
                ways[wid]['ref'].append(int(ref))
        for tag in n.getElementsByTagName("tag"):
            if tag.hasAttribute("k") and tag.hasAttribute('v'):
                k = tag.getAttribute("k")
                if k not in wkeys:
                    wkeys.append(k)
                ways[wid]['tags'][k] = tag.getAttribute('v')
        first = ways[wid]['ref'][0]
        last = ways[wid]['ref'][len(ways[wid]['ref'])-1]
        if first == last:
            ways[wid]['geomType'] = "polygon"
        else:
            ways[wid]['geomType'] = "polyline"
    intersections = []
    wids2 = [x for x in wids]
    print ('finding intersections')
    for x in wids:
        for y in wids:
            if x < y:
                ref1 = ways[x]['ref']
                ref2 = ways[y]['ref']
                l = [e for e in ref1 if e in ref2]
                if l and len(l) == 1:
                    intersections += l
                    
    print ("There are "+ str(len(intersections))+ ' intersections')
    intersections = { intersection: ( data[intersection]['lat'], data[intersection]['lon']) for intersection in intersections }

    return intersections

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Extract intersections from OSM')
    parser.add_argument('file', help='The OSM file')
    args = parser.parse_args()
    print('Processing ...'+args.file)
    intersections = find_intersections(args.file)
    for i in intersections:
        print ( str(i) + ' : '+ str(intersections[i]) )