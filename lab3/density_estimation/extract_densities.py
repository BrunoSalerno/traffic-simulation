import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import sys
import numpy as np
import pandas as pd

def fetch_edge_attrs(data, edge_id, attrs):
    values = {}
    intervals = data.findall('interval')
    for interval in intervals:
        end = float(interval.get('end'))
        if (end / 60) >= 15: # warmup check
            for edge in interval:
                if edge.get('id') == edge_id:
                    for attr in attrs:
                        if not attr in values:
                            values[attr] = []
                        if edge.get(attr) is not None:
                            values[attr].append(float(edge.get(attr)))
    return values

def fetch_interval_attrs(data, int_ids, attrs):
    values = {}
    intervals = data.findall('interval')
    for interval in intervals:
        end = float(interval.get('end'))
        if (end / 60) >= 15: # warmup check
            int_id = interval.get('id')
            if int_id in int_ids:
                if not int_id in values:
                    values[int_id] = {}
                for attr in attrs:
                    if not attr in values[int_id]:
                        values[int_id][attr] = []
                    val = interval.get(attr)
                    if val is not None:
                        values[int_id][attr].append(float(val))
    return values

def densities(density_0,deltas_q):
    delta_x = 1 # km
    delta_t = 5.0/60 # h

    res = np.array([density_0])

    for i in range(1, len(deltas_q)):
        prevdens = res[-1]
        delta_q = deltas_q[i]
        d = prevdens + (1/delta_x) * delta_q * delta_t
        res = np.append(res, d)

    return res

def traci_densities():
    links_d = pd.read_csv("output/links_1runs.csv")
    dens = links_d['link4']
    print(dens)
    return [dens.index+16, dens]

if __name__ == "__main__":
    filename = sys.argv[1]
    xml = ET.parse(filename)

    edgefilename = sys.argv[2]
    xml2 = ET.parse(edgefilename)

    traci_xs, traci_densities = traci_densities()

    sumo_densities = fetch_edge_attrs(xml2.getroot(), 'link4', ['entered','left','density'])['density']

    links = ['il1_start', 'il2_start', 'il3_start','il1_end','il2_end','il3_end']
    vals = fetch_interval_attrs(xml.getroot(), links, ['flow','nVehContrib'])

    entered = np.array(vals['il1_start']['flow'])+np.array(vals['il2_start']['flow']) +np.array(vals['il3_start']['flow'])
    left = np.array(vals['il1_end']['flow'])+np.array(vals['il2_end']['flow']) +np.array(vals['il3_end']['flow'])
    deltas_q = entered - left

    dens = densities(sumo_densities[0], deltas_q)

    minutes = np.array(range(len(dens))) * 5 + 15
    plt.plot(minutes,dens, label='Density conservation law')
    plt.plot(minutes,sumo_densities, label='SUMO edge density')
    plt.plot(traci_xs,traci_densities, label='SUMO tracy density')

    plt.ylabel('Density (#veh/km)')
    plt.xlabel('Minutes')
    plt.title('Density - Edge 4')
    plt.legend()
    plt.show()
