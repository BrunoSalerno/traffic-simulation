import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import sys
import numpy as np
import pandas as pd

def fetch_edge_attr(data, attr):
    values = {}
    intervals = data.findall('interval')
    for interval in intervals:
        end = float(interval.get('end'))
        if (end / 60) >= 15: # warmup check
            for edge in interval:
                edge_id = edge.get('id')
                if not edge_id in values:
                    values[edge_id] = []
                if edge.get(attr) is not None:
                    values[edge_id].append(float(edge.get(attr)))
    return values

if __name__ == '__main__':
    filename = sys.argv[1]
    xml = ET.parse(filename)

    densities = pd.DataFrame(fetch_edge_attr(xml.getroot(), 'density'))
    del densities['link5']

    print("densities")
    print(densities)
    print(list(densities['link1']))

    speeds = pd.DataFrame(fetch_edge_attr(xml.getroot(), 'speed'))
    del speeds['link5']

    # flow = density * speed
    flows = np.multiply(speeds.values, densities.values)

    print("flows")
    print(list(flows[:,0]))
    print(flows[0])

    densities[0:60].plot()
    #plt.plot(flows[0:60])
    plt.ylabel('Density (#veh/km)')
    plt.xlabel('Iteration')
    plt.show()
