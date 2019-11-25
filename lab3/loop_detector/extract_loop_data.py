"""
Example on how to use Element Tree to extract data from the detector loop output file:
"""

import matplotlib
matplotlib.use('TkAgg')

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import collections
import sys

""" 
Extracting flow from lane 0 in link 4:
"""


def flow(loopId,xml,feature):
    tree = ET.parse(xml)
    root = tree.getroot()
    time_flow = collections.OrderedDict()  # Ordered dictionary containing time periods as keys and flows in lane 0 in link 4 as values
    for information in root.findall("interval"):
        if information.get("id") == loopId:
            end = float(information.get("end"))
            flow = float(information.get(feature))
            time_flow[int(end / 60)] = int(flow)
    return time_flow

def extract_and_plot(xml, feature):
    loops = ['il1', 'il2', 'il3']

    for loopId in loops:
        data = flow(loopId, xml, feature)
        time_range = list(data.keys())
        values = list(data.values())
        plt.plot(time_range, values, label=feature + ' ' + loopId)
        plt.xlabel('Duration (minutes)')

if __name__ == "__main__":
    file = sys.argv[1]
    extract_and_plot(file, 'speed')

    extract_and_plot(file, 'harmonicMeanSpeed')

    plt.grid(True)
    plt.legend()
    plt.show()
