import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import sys
import numpy as np

def fetch_edge_attrs(data, edge_id, attrs):
    values = {}
    intervals = data.findall('interval')
    for interval in intervals:
        for edge in interval:
            if edge.get('id') == edge_id:
                for attr in attrs:
                    if not attr in values:
                        values[attr] = []
                    if edge.get(attr) is not None:
                        values[attr].append(float(edge.get(attr)))
    return values

if __name__ == "__main__":
    filename = sys.argv[1]
    xml = ET.parse(filename)

    edge = 'link4'
    vals = fetch_edge_attrs(xml.getroot(), edge, ['density'])
    print(vals)

