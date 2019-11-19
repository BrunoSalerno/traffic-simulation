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

number_runs = 1  # number of simulation repetitions
last_simulation_step = 36001

all_speeds = []
all_variances = []
all_n_vehicles = []
all_departed = []
all_loaded = []

print ("TOTAL RUNS {}:".format(number_runs))

for runs in range(number_runs):
    print ("Simulation Run Number {} has started".format(runs + 1))
    i = 1
    counter = 0
    departed = 0
    loaded = 0
    while i < last_simulation_step:
        traci.simulationStep()
        # Hint: filter out warm up period
        # Hint: collect output from simulation steps that correspond to a full minute
        # Hint: use IDList = traci.vehicle.getIDList() to capture all the vehicles in a specific time, read more here https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html

        departed += traci.simulation.getDepartedNumber()
        loaded += traci.simulation.getLoadedNumber()

        if i % 600 == 0:
            counter += 1
            #print ("full minute number {}".format(counter))

            # Warm-up check (15 min threshold)
            if counter > 15:
                vehicles_ids = traci.vehicle.getIDList()
                n_vehicles = len(vehicles_ids)
                all_n_vehicles.append(n_vehicles)
                speeds = []
                for vid in vehicles_ids:
                    speeds.append(traci.vehicle.getSpeed(vid))

                speed = np.mean(speeds)
                all_speeds.append(speed)
                var = np.var(all_speeds)
                all_variances.append(var)
                all_departed.append(departed)
                all_loaded.append(loaded)

                print("{} vehicles".format(n_vehicles))
                print("Avg speed {}".format(speed))
                print("Variance {}".format(var))
        i += 1

    traci.load(["-c", conf_file, "--random"])  # reloading simulation for the next run, with a random seed

traci.close()  # closing simulation

minutes = np.arange(16, 16 + len(all_speeds)).tolist()

df = pd.DataFrame({
    'mean_speed': all_speeds,
    'cum_variance': all_variances,
    'cum_departed': all_departed
    }, index=minutes)

filename = "1run-{}mins.csv".format(int(last_simulation_step / 600))
df.to_csv(filename)
