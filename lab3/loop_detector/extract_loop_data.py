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

def extractMeanFeature(xml,feature):
    tree = ET.parse(xml)
    root = tree.getroot()
    time_flow = collections.OrderedDict()  # Ordered dictionary containing time periods as keys and flows in lane 0 in link 4 as values

    detectors = ['il1', 'il2', 'il3']
    for detector in detectors:
        for information in root.findall("interval"):
            if information.get("id") == detector:
                end = float(information.get("end"))
                if (end / 60) > 15: # warmup check
                    val = float(information.get(feature))
                    time_flow[int(end / 60)] = val

    for t in time_flow:
        time_flow[t] = np.mean(time_flow[t])

    return time_flow

def extractAndPlot(xml, feature):
    data = extractMeanFeature(xml, feature)
    time_range = list(data.keys())
    values = list(data.values())
    print(values)
    plt.plot(time_range, values, label=feature)
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Speed (m/s)')

if __name__ == "__main__":
    file = sys.argv[1]

    extractAndPlot(file, 'speed')
    extractAndPlot(file, 'harmonicMeanSpeed')

    plt.grid(True)
    plt.legend()
    plt.show()
