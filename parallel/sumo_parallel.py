import multiprocessing
import traci
import numpy as np
import time
import random

def simulation(cmd,outputfile):
    traci.start(cmd)
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
    f.write("{},{}\n".format(mean_speed,var_speed))
    f.close()

if __name__ == "__main__":

    sumo_exe = "sumo"
    conf_file = "config.xml"  # the configuration file

    procs = []
    n_processors = multiprocessing.cpu_count()
    max_process = n_processors

    print("{} processors".format(n_processors))
    print("{} processes".format(max_process))

    start_time = time.time()
    outputfile = "sims_{}process_{}.csv".format(max_process,int(start_time))
    f = open(outputfile, "a+")
    f.write("mean_speed,variance\n")
    f.close()

    print("Creating {}".format(outputfile))

    for i in range(1, max_process):
        seed = int((random.random() * 100000) + time.time())
        print ("seed: {}".format(seed))
        sumo_cmd = [sumo_exe, "-c", conf_file, '--seed', str(seed)]

        proc = multiprocessing.Process(target=simulation, args=(sumo_cmd,outputfile))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()


    end_time = time.time()
    print("ELAPSED TIME: {}".format(end_time - start_time))
