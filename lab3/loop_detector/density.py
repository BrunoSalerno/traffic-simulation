import matplotlib
matplotlib.use('TkAgg')

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import collections
import sys
import numpy as np

def extractMeanFeature(data,feature, detectors):
    times = collections.OrderedDict()  # Ordered dictionary containing time periods as keys and flows in lane 0 in link 4 as values

    for detector in detectors:
        for interval in data.findall("interval"):
            if interval.get("id") == detector:
                end = float(interval.get("end"))
                if (end / 60) > 15: # warmup check
                    val = float(interval.get(feature))
                    key = int(end/60)
                    if not key in times:
                        times[key] = []
                    times[key].append(val)

    return times

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

def edge_density(data):
    detectors = ['il1','il2','il3']

    flows_dict = extractMeanFeature(data, 'flow', detectors)
    speed_dict = extractMeanFeature(data, 'harmonicMeanSpeed', detectors)
    time_intervals = np.array(list(flows_dict.keys()))

    flows = np.array(list(flows_dict.values()))
    speeds = np.array(list(speed_dict.values())) * 3.6
    densities = flows / speeds

    p_a = np.sum(densities,1)
    effective_densities = p_a#/len(detectors)
    return [effective_densities, time_intervals]

def extract_and_plot_edge_density(xs):
    xml = ET.parse(file2)
    space_mean_speed = fetch_edge_attrs(xml.getroot(), 'link4', ['density'])['density']
    plt.plot(xs, space_mean_speed, label="edgeData density", linestyle='dashed')

if __name__ == "__main__":
    file = sys.argv[1]
    tree = ET.parse(file)
    data = tree.getroot()

    ed_densities, t_intervals = edge_density(data)
    plt.plot(t_intervals, ed_densities, label="density")

    file2 = sys.argv[2]

    extract_and_plot_edge_density(t_intervals)

    plt.title('Density - Edge 4 (loop in the end)')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Density (veh/km)')
    plt.grid(True)
    plt.legend()
    plt.show()

