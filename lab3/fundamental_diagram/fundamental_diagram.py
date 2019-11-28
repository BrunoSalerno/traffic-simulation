import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import sys

def fetch_edge_attrs(data, edge_id, attrs):
    values = {}
    intervals = data.findall('interval')
    for interval in intervals:
        for edge in interval:
            if edge.get('id') == edge_id:
                for attr in attrs:
                    if not attr in values:
                        values[attr] = []
                    values[attr].append(edge.get(attr))
    return values

if __name__ == "__main__":
    filename = sys.argv[1]
    xml = ET.parse(filename)

    edge = 'link4'
    vals = fetch_edge_attrs(xml.getroot(), edge, ['speed', 'density'])
    print(vals)

    plt.scatter(vals['density'], vals['speed'])
    plt.xlabel('Density (#veh/km)')
    plt.ylabel('Speed (m/s)')
    plt.title('{}: Speed vs Density (60 min)'.format(edge))
    plt.show()
