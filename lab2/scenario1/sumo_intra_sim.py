"""
Template file for the KTH course AH2174 Traffic Simulation
Created on Monday, November 4th 2019
"""
# Importing modules/Libraries
import os, subprocess, sys, math, random
import numpy as np

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import pandas as pd

# Defining SUMO path and importing traci module
# the path can be declared manually in the operating system (https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html)
#sumo_path = '/usr/local/Cellar/sumo/1.3.1/share/sumo'
sumo_path = '/usr/local/Cellar/sumo/HEAD-93b75bf/share/sumo'
sys.path.append(os.path.join(sumo_path, 'tools'))
#os.environ["SUMO_HOME"] = sumo_path
import traci

# compose the command line to start either SUMO or SUMO-GUI
sumo_exe = "sumo"
conf_file = "config.xml"  # the configuration file
sumo_cmd = [sumo_exe, "-c", conf_file]
traci.start(sumo_cmd)

"""
Simulation example in the following section, update the written code according to the requirement of project 1
"""
# for sequential runs, see: http://sumo.dlr.de/wiki/TraCI#Shutdown

number_runs = 20  # number of simulation repetitions
last_simulation_step = 36001

all_speeds = {}
all_departed = {}

print ("TOTAL RUNS {}:".format(number_runs))

for runs in range(number_runs):
    print ("Simulation Run Number {} has started".format(runs + 1))
    i = 1
    counter = 0
    departed = 0

    while i < last_simulation_step:
        traci.simulationStep()

        departed += traci.simulation.getDepartedNumber()

        if i % 600 == 0:
            counter += 1

            # Warm-up check (15 min threshold)
            if counter > 15:
                vehicles_ids = traci.vehicle.getIDList()
                speeds = []
                for vid in vehicles_ids:
                    speeds.append(traci.vehicle.getSpeed(vid))

                key = 'sim' + str(runs + 1)
                if not key in all_speeds:
                    all_speeds[key] = []
                if not key in all_departed:
                    all_departed[key] = []

                all_speeds[key].append(np.mean(speeds))
                all_departed[key].append(departed)

        i += 1

    traci.load(["-c", conf_file, "--random"])  # reloading simulation for the next run, with a random seed

traci.close()  # closing simulation

df_speeds = pd.DataFrame.from_dict(all_speeds, orient='index').transpose()
df_departed = pd.DataFrame.from_dict(all_departed, orient='index').transpose()

df = pd.DataFrame({
    'mean_speed': df_speeds.mean(axis=1),
    'mean_departed': df_departed.mean(axis=1)
    })
df.set_index(df.index + 16, inplace=True)

variances = []
for i in range(1, len(df.index) + 1):
    sample = df['mean_speed'].iloc[:i]
    variances.append(np.var(sample))

df['cum_variance'] = variances

filename = "{}runs-{}mins.csv".format(number_runs, int(last_simulation_step / 600))
df.to_csv(filename)
