import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from ctm import Simulation

if __name__ == '__main__':
    sim = Simulation()
    output = sim.run()
    print(output)
    for edge_i in output:
        ys = [e['q0'] for e in output[edge_i]]
        plt.plot(ys, label='edege {}'.format(edge_i))
    plt.legend()
    plt.show()
