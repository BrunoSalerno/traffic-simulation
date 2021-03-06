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

all_speeds = []
all_variances = []
all_cum_variances = []
all_departed = []
all_accels = []

print ("TOTAL RUNS {}".format(number_runs))

for runs in range(number_runs):
    print ("Simulation Run Number {} has started".format(runs + 1))
    i = 1
    counter = 0

    sim_speeds = []
    sim_accels = []
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
                accels = []
                for vid in vehicles_ids:
                    speeds.append(traci.vehicle.getSpeed(vid))
                    accels.append(traci.vehicle.getAcceleration(vid))

                speed = np.mean(speeds)
                sim_speeds.append(speed)
                accel = np.mean(accels)
                sim_accels.append(accel)
        i += 1
    
    mean_speed = np.mean(sim_speeds)
    mean_accel = np.mean(sim_accels)
    var_speed = np.var(sim_speeds)

    all_departed.append(departed)
    all_speeds.append(mean_speed)
    all_accels.append(mean_accel)
    all_variances.append(var_speed)
    all_cum_variances.append(np.var(all_speeds))

    print ("Simulation Run Number {} has ended".format(runs + 1))

    traci.load(["-c", conf_file, "--random"])  # reloading simulation for the next run, with a random seed

traci.close()  # closing simulation

df = pd.DataFrame({
    'mean_speed': all_speeds,
    'mean_accel': all_accels,
    'variance': all_variances,
    'cum_variance': all_cum_variances,
    'departed': all_departed,
    }, index=np.arange(1, number_runs + 1).tolist())

filename = "{}runs.csv".format(number_runs)
df.to_csv(filename)
