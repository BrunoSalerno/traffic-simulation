import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import sys
import numpy as np
import sklearn.metrics

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

def greenshield(vals):
    # The fit is a linear model, following Greenshield
    # y(x) = a + b1.x
    # and
    # v(p) = vf(1 - p/pj)
    # v(p) = vf - vf/pj * p
    # so
    # a = vf
    # b1 = - vf/pj
    b1, a= np.polyfit(vals['density'], vals['speed'], 1)
    x = np.linspace(min(vals['density']),max(vals['density']))
    y = a + b1 * x

    # Equal to y, but only for the actual speeds of x
    y_predicted = a + b1 * np.array(vals['density'])

    r2 = sklearn.metrics.r2_score(vals['speed'], y_predicted)
    return x,y,r2



if __name__ == "__main__":
    filename = sys.argv[1]
    xml = ET.parse(filename)

    edge = 'link4'

    # According to https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html,
    # `speed` "is an average over time and space (space-mean-speed)".
    vals = fetch_edge_attrs(xml.getroot(), edge, ['speed', 'density'])
    print(vals)

    plt.scatter(vals['density'], vals['speed'])

    x,y,r2 = greenshield(vals)
    plt.plot(x, y, color='black', label='Greenshield R2: {}'.format(round(r2,2)))

    plt.xlabel('Density (#veh/km)')
    plt.ylabel('Speed (m/s)')
    plt.title('{}: Speed vs Density (60 min)'.format(edge))
    plt.legend()
    plt.show()
