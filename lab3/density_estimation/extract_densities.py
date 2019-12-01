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

def densities(vals):
    delta_x = 1 # km
    delta_t = 5.0/60 # m
    entered = np.array(vals['entered'])
    left = np.array(vals['left'])

    deltas_q = entered - left
    print('deltas_q',deltas_q)
    res = np.array([])

    for i in range(0, len(deltas_q)):
        prevdens = res[i-1] if i > 0 else 0
        delta_q = deltas_q[i]
        d = prevdens + (1/delta_x) * delta_q * delta_t
        res = np.append(res, d)

    return res


if __name__ == "__main__":
    filename = sys.argv[1]
    xml = ET.parse(filename)

    edge = 'link4'
    vals = fetch_edge_attrs(xml.getroot(), edge, ['entered','left','density'])
    print(vals)

    dens = densities(vals)
    print(dens)
