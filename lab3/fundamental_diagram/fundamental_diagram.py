import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import sys
import numpy as np
import sklearn.metrics
import scipy.optimize

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
    # The fit is a linear model, following Greenshields
    # y(x) = a + b1.x
    # and
    # v(p) = vf(1 - p/pj)
    # v(p) = vf - vf/pj * p
    # so
    # a = vf
    # b1 = - vf/pj
    b1, a= np.polyfit(vals['density'], vals['speed'], 1)
    x = np.linspace(0,-a/b1)
    y = a + b1 * x

    print('Greenshield: a: {} b1: {}'.format(a, b1))

    # Equal to y, but only for the actual speeds of x
    y_predicted = a + b1 * np.array(vals['density'])

    r2 = sklearn.metrics.r2_score(vals['speed'], y_predicted)
    return x,y,r2

def _greenberg_func(p, pj, v0):
    return v0 * np.log(pj/p)

def greenberg(vals):
    # Initial guess: v0 = 70km, and kj = 200 veh/km
    popt, pconv = scipy.optimize.curve_fit(_greenberg_func, vals['density'], vals['speed'], p0 =[200,70])
    pj, v0 = popt
    x = np.linspace(10,350)
    y = _greenberg_func(x, pj, v0)

    print('Greenberg: pj: {}, v0: {}'.format(pj, v0))

    # Equal to y, but only for the actual speeds of x
    y_predicted = _greenberg_func(np.array(vals['density']), pj, v0)
    r2 = sklearn.metrics.r2_score(vals['speed'], y_predicted)

    return x, y, r2

if __name__ == "__main__":
    filename = sys.argv[1]
    xml = ET.parse(filename)

    edge = 'link4'

    # According to https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html,
    # `speed` "is an average over time and space (space-mean-speed)".
    vals = fetch_edge_attrs(xml.getroot(), edge, ['speed', 'density'])
    # We convert speeds to km/h:
    vals['speed'] = np.array(vals['speed']) * 3.6

    print(vals)

    plt.scatter(vals['density'], vals['speed'], color='gray')

    x,y,r2 = greenshield(vals)
    plt.plot(x, y, label='Greenshields R2: {}'.format(round(r2,2)))

    x,y,r2 = greenberg(vals)
    plt.plot(x, y, label='Greenberg R2: {}'.format(round(r2,2)))

    plt.axis(xmin=0,ymin=0)
    plt.xlabel('Density (#veh/km)')
    plt.ylabel('Speed (km/h)')
    plt.title('{}: Speed vs Density (60 min)'.format(edge))
    plt.legend()
    plt.show()
