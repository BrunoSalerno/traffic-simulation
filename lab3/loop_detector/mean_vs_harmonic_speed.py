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

def density(flow, speed):
    return flow / speed

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

    for d in range(len(detectors)):
        vals = [v[d] for v in values]
        label = '{} {}'.format(feature, detectors[d])
        plt.plot(time_range, vals, label=label)

if __name__ == "__main__":
    file = sys.argv[1]

    extractAndPlot(file, 'speed')
    extractAndPlot(file, 'harmonicMeanSpeed')
    plt.title('Average vs Harmonic Speed - Edge 4 (loop in the end)')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Speed (m/s)')
    plt.grid(True)
    plt.legend()
    plt.show()
