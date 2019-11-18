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

print ("TOTAL RUNS {}".format(number_runs))

for runs in range(number_runs):
    print ("Simulation Run Number {} has started".format(runs + 1))
    i = 1
    counter = 0

    sim_speeds = []
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

                speed = np.mean(speeds)
                var   = np.var(speeds)
                sim_speeds.append(speed)
        i += 1
    
    mean_speed = np.mean(sim_speeds)
    var_speed = np.var(sim_speeds)

    all_departed.append(departed)
    all_speeds.append(mean_speed)
    all_variances.append(var_speed)
    all_cum_variances.append(np.var(all_speeds))

    print ("Simulation Run Number {} has ended".format(runs + 1))

    traci.load(["-c", conf_file, "--random"])  # reloading simulation for the next run, with a random seed

traci.close()  # closing simulation

df = pd.DataFrame({
    'mean_speed': all_speeds,
    'variance': all_variances,
    'cum_variance': all_cum_variances,
    'departed': all_departed
    }, index=np.arange(1, number_runs + 1).tolist())

print("Final stats:")
print(df)

fig, (p1,p2,p3,p4) = plt.subplots(4,1,sharex=False, sharey=False)

df['mean_speed'].hist(ax=p1)
p1.set_title("Avg speed (m/s) - {} runs".format(number_runs))
p1.set_xlabel("Speed - m/s")
p1.set_ylabel("Frequency")

#df['variance'].plot(ax=p2, use_index=True, label="variance")
#p2.set_xlabel("Simulation")
#p2.set_ylabel("Variance - (m/s)^2")

df['cum_variance'].plot(ax=p3, use_index=True, label="cum. variance")
p3.set_xlabel("Simulation")
p3.set_ylabel("Cum variance - (m/s)^2")

df['departed'].plot(ax=p4, use_index=True)
p4.set_xlabel("Simulation")
p4.set_ylabel("Departed vehicles")
plt.show()
