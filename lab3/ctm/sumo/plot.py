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

    densities = fetch_edge_attr(xml.getroot(), 'density')
    df = pd.DataFrame(densities)
    print(df)

    df.plot()
    plt.ylabel('Density (#veh/km)')
    plt.xlabel('Iteration')
    plt.show()
