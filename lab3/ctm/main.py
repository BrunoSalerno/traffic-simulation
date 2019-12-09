#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from ctm import Simulation

def plot_intervals(data, var, edges=None):
    for edge_i in data:
        if not edges or (edge_i in edges):
            ys = [e[var] for e in data[edge_i]]
            print('edge {}'.format(edge_i), var,ys)
            plt.plot(ys, label='{} edge {}'.format(var, edge_i))


def plot_interval(interval, data, var):
    ys =  [data[edge][interval][var] for edge in data]
    plt.plot(ys, label='Interval {}, {}'.format(interval, var))


if __name__ == '__main__':
    edges = 5
    m = 3.0
    tau = 0.5 / 3600
    n_iters = 60
    delta_t = 10 / 3600 # 10 s
    delta_x = 0.5 # 500 m
    v0 = 50.0
    p_m = 120.0

    # Rule:
    # delta_t < delta_x / v0
    # Treiber et al 2013, p. 100


    p_as_edge1 = [49.38, 48.83, 49.47, 48.72, 48.5, 49.19, 45.82, 45.18, 45.72, 45.33, 48.11, 50.18, 49.41, 46.49, 46.59, 45.91, 37.92, 30.68, 27.99, 26.48, 32.64, 40.95, 41.75, 41.83, 42.7, 45.68, 47.86, 47.61, 47.55, 47.54, 49.58, 49.48, 48.43, 48.05, 47.35, 44.96, 43.69, 42.4, 41.72, 42.65, 48.2, 47.95, 47.7, 47.56, 44.84, 43.0, 39.94, 39.85, 39.37, 45.04, 53.0, 53.39, 53.59, 53.22, 53.01, 53.22, 53.39, 53.42, 53.51, 52.85, 53.09, 53.01, 53.33, 53.51, 53.37, 53.1, 48.66, 39.74, 37.88, 34.7, 31.85, 37.98, 40.37, 43.13, 41.65, 42.85]
    p_as_iter1 = [49.38,54.21,45.67,53.57,52.42]

    sim = Simulation(edges, m, tau, n_iters, delta_t, delta_x, v0, p_m)
    #sim.add_bottleneck(3, 40)
    output = sim.run(p_as_for_initial_edge = p_as_edge1, p_as_for_initial_iter=p_as_iter1)

    plot_intervals(output,'p_a',[1,2,3,4,5])
    #plot_intervals(output,'q_a')
    #plot_intervals(output,'s')
    #plot_intervals(output,'d')
    #for i in range(n_iters-1):
    #plot_interval(5, output, 'q_a')
    #plot_interval(5, output, 'q1')
    #plot_interval(6, output, 'q0')
    #plot_interval(6, output, 'q1')
    #plot_interval(7, output, 'q0')

    plt.ylabel('Density (#veh/km)')
    plt.xlabel('Iteration')
    plt.legend()
    plt.show()

