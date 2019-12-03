import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from ctm import Simulation

if __name__ == '__main__':
    edges = 5
    m = 3
    tau = 1
    n_iters = 30

    sim = Simulation(edges, m, tau, n_iters)
    output = sim.run()

    print(output)

    for edge_i in output:
        ys = [e['q0'] for e in output[edge_i]]
        ys = ys[3:]
        plt.plot(ys, label='q0 edge {}'.format(edge_i))

    plt.legend()
    plt.show()
