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
        end = float(interval.get('end'))
        if (end / 60) > 15: # warmup check
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

    # According to https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html,
    # `speed` "is an average over time and space (space-mean-speed)".
    vals = fetch_edge_attrs(xml.getroot(), edge, ['speed', 'density'])
    print(vals)

    plt.scatter(vals['density'], vals['speed'])
    b3, b2, b1, a= np.polyfit(vals['density'], vals['speed'], 3)

    # Fit
    x = np.linspace(min(vals['density']),max(vals['density']))
    y = a + b1 * x + b2 * (x ** 2) + b3 * (x ** 3)
    plt.plot(x, y, color='black')
    #

    plt.xlabel('Density (#veh/km)')
    plt.ylabel('Speed (m/s)')
    plt.title('{}: Speed vs Density (60 min)'.format(edge))
    plt.show()
