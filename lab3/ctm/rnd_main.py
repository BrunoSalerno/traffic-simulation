#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import random

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
    edges = 6
    m = 3.0
    tau = 1.4 / 3600
    n_iters = 60
    delta_t = 10 / 3600 # 10 s
    delta_x = 0.5 # 500 m
    v0 = 15.0
    p_m = 360.0

    # Rule:
    # delta_t < delta_x / v0
    # Treiber et al 2013, p. 100

    p_as_edge1 = np.repeat(40 + random.randint(-2,2),60)
    p_as_iter1 = np.repeat(40 + random.randint(-2,2),6)

    q_as_edge1 = np.repeat(600 + random.randint(-2,2),60)
    q_as_iter1 = np.repeat(600 + random.randint(-2,2),6)

    sim = Simulation(edges, m, tau, n_iters, delta_t, delta_x, v0, p_m)

    sim.add_bottleneck(edge=2, capacity=300, interval=20)

    output = sim.run(p_as_for_initial_edge = p_as_edge1, p_as_for_initial_iter=p_as_iter1, q_as_for_initial_edge = q_as_edge1, q_as_for_initial_iter = q_as_iter1)

    #plot_intervals(output,'q_a',[1,2,3,4,5])
    #plt.ylabel('Flow (#veh/h)')

    plot_intervals(output,'p_a')
    plt.ylabel('Density (#veh/km)')
    plt.xlabel('Iteration')
    plt.title('Density - CTM with rnd values. Bottleneck at 2nd edge in int 20')
    plt.legend()
    plt.show()

    plot_intervals(output,'q_a')
    plt.ylabel('Flow (#veh/h)')
    plt.title('Flow - CTM with rnd values. Bottleneck at 2nd edge in int 20')
    plt.xlabel('Iteration')
    plt.legend()
    plt.show()
