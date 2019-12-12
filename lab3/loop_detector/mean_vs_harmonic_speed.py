"""
Example on how to use Element Tree to extract data from the detector loop output file:
"""

import matplotlib
matplotlib.use('TkAgg')

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import collections
import sys
import numpy as np

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

def extractMeanFeature(xml,feature, detectors):
    tree = ET.parse(xml)
    root = tree.getroot()
    times = collections.OrderedDict()  # Ordered dictionary containing time periods as keys and flows in lane 0 in link 4 as values

    for detector in detectors:
        for interval in root.findall("interval"):
            if interval.get("id") == detector:
                end = float(interval.get("end"))
                if (end / 60) > 15: # warmup check
                    val = float(interval.get(feature))
                    key = int(end/60)
                    if not key in times:
                        times[key] = []
                    times[key].append(val)

    return times

def extractAndPlot(xml, feature):
    detectors = ['il1', 'il2', 'il3']
    data = extractMeanFeature(xml, feature, detectors)

    time_range = list(data.keys())
    values = list(data.values())

    flows = extractMeanFeature(xml, 'flow', detectors).values()
    densities = np.array(list(values)) / np.array(list(flows))

    mean = np.average(values, weights=densities, axis=1)

    # for d in range(len(detectors)):
    #     vals = [v[d] for v in values]
    #label = '{} {}'.format(feature, detectors[d])

    plt.plot(time_range, mean, label='detector ' + feature)
    return time_range

def extractAndPlotMeanSpaceSpeed(xml, xs):
    xml = ET.parse(file2)
    space_mean_speed = fetch_edge_attrs(xml.getroot(), 'link4', ['speed'])['speed']
    plt.plot(xs, space_mean_speed, label="edgeData speed", linestyle='dashed')

if __name__ == "__main__":
    file = sys.argv[1]

    extractAndPlot(file, 'speed')
    time_range = extractAndPlot(file, 'harmonicMeanSpeed')

    file2 = sys.argv[2]
    extractAndPlotMeanSpaceSpeed(file2, time_range)

    plt.title('Average vs Harmonic Speed - Edge 4 (loop in the middle)')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Speed (m/s)')
    plt.grid(True)
    plt.legend()
    plt.show()
