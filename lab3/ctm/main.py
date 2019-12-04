import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from ctm import Simulation

def plot_intervals(data, var, edges=None):
    for edge_i in data:
        if not edges or (edge_i in edges):
            ys = [e[var] for e in data[edge_i]][0:]
            print('edge {}'.format(edge_i), var,ys)
            plt.plot(ys, label='{} edge {}'.format(var, edge_i))
        

def plot_interval(interval, data, var):
    ys =  [data[edge][interval][var] for edge in data]
    plt.plot(ys, label='Interval {}, {}'.format(interval, var))


if __name__ == '__main__':
    edges = 5
    m = 3.0
    tau = 0.001
    #n_iters = 30
    n_iters = 15

    sim = Simulation(edges, m, tau, n_iters)
    output = sim.run()

    print(output)

    #plot_intervals(output,'q0')
    plot_intervals(output,'q_a',[2])
    #plot_intervals(output,'p_a')
    #plot_intervals(output,'q_a')
    #plot_intervals(output,'s')
    #plot_intervals(output,'d')
    #for i in range(n_iters-1):
    #plot_interval(5, output, 'q0')
    #plot_interval(6, output, 'q0') 
    #plot_interval(7, output, 'q0') 
    plt.legend()
    plt.show()
