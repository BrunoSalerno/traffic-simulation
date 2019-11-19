import multiprocessing
import traci
import numpy as np
import time
import random
import sys

def simulation_handler(cmd,outputfile,times):
    for i in range(times):
        simulation(cmd, outputfile)

def simulation(cmd,outputfile):
    seed = int((random.random() * 100000) + time.time())
    print ("seed: {}".format(seed))

    traci.start(cmd + ['--seed', str(seed)])
    i = 1
    laststep = 36001
    minutes = 0

    sim_speeds = []
    departed = 0

    while i <= laststep:
        traci.simulationStep()

        departed += traci.simulation.getDepartedNumber()

        if i % 600 == 0:
            minutes += 1

            # Warm-up check (15 min threshold)
            if minutes > 15:
                vehicles_ids = traci.vehicle.getIDList()
                speeds = []
                for vid in vehicles_ids:
                    speeds.append(traci.vehicle.getSpeed(vid))

                speed = np.mean(speeds)
                var   = np.var(speeds)
                sim_speeds.append(speed)
        
        i += 1
 
    traci.close()

    mean_speed = np.mean(sim_speeds)
    var_speed = np.var(sim_speeds)

    f = open(outputfile, "a+")
    f.write("{},{},{}\n".format(mean_speed,var_speed,departed))
    f.close()

if __name__ == "__main__":

    sumo_exe = "sumo"
    conf_file = "config.xml"  # the configuration file
    sumo_cmd = [sumo_exe, "-c", conf_file]

    procs = []
    n_processors = multiprocessing.cpu_count()
    max_process = int(sys.argv[1]) if len(sys.argv) >= 2 else n_processors
    n_runs = int(sys.argv[2]) if len(sys.argv) >= 3 else max_process
    runs_per_process = n_runs / max_process

    start_time = time.time()
    outputfile = "sims_{}process_{}runs_{}.csv".format(max_process,n_runs,int(start_time))

    interactive = True
    if len(sys.argv) >=4 and sys.argv[3] == '--no-interactive':
        interactive = False

    print("Info about the simulation:")
    print("{} processors".format(n_processors))
    print("{} processes".format(max_process))
    print("{} total runs".format(n_runs))
    print("{} runs per process".format(runs_per_process))
    print("Output file: {}".format(outputfile))
    if interactive:
        continue_or_not = raw_input("Press N to cancel...")
        if continue_or_not == 'N':
            sys.exit()

    f = open(outputfile, "a+")
    f.write("mean_speed,variance,departed\n")
    f.close()

    for i in range(1, max_process):
        proc = multiprocessing.Process(target=simulation_handler, args=(sumo_cmd,outputfile,runs_per_process))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    end_time = time.time()
    print("ELAPSED TIME: {}".format(end_time - start_time))
