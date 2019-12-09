"""
Template file for the KTH course AH2174 Traffic Simulation
Created on Monday, November 4th 2019
"""
# Importing modules/Libraries
import os, subprocess, sys, math, random

# Defining SUMO path and importing traci module
# the path can be declared manually in the operating system (https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html)
#sumo_path = '/usr/local/Cellar/sumo/1.3.1/share/sumo'
sumo_path = '/usr/local/Cellar/sumo/HEAD-93b75bf/share/sumo'
sys.path.append(os.path.join(sumo_path, 'tools'))
#os.environ["SUMO_HOME"] = sumo_path
import traci

# compose the command line to start either SUMO or SUMO-GUI
sumo_exe = "sumo"
conf_file = "sumo/config.xml"  # the configuration file
sumo_cmd = [sumo_exe, "-c", conf_file, '--random']
traci.start(sumo_cmd)

"""
Simulation example in the following section, update the written code according to the requirement of project 1
"""
# for sequential runs, see: http://sumo.dlr.de/wiki/TraCI#Shutdown

number_runs = 1  # number of simulation repetitions
last_simulation_step = 36001

print ("TOTAL RUNS {}".format(number_runs))

for runs in range(number_runs):
    print ("Simulation Run Number {} has started".format(runs + 1))
    i = 1

    while i < last_simulation_step:
        traci.simulationStep()
        i += 1
    #traci.load(["-c", conf_file, "--random"])  # reloading simulation for the next run, with a random seed

traci.close()  # closing simulation
