import multiprocessing
import traci
import numpy as np

def simulation(cmd):
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
    print("Mean speed: {}".format(mean_speed))
    print("Variance: {}".format(var_speed))
    print("Departed: {}".format(departed))

if __name__ == "__main__":

    sumo_exe = "sumo"
    conf_file = "config.xml"  # the configuration file
    sumo_cmd = [sumo_exe, "-c", conf_file, '--random']

    procs = []
    n_processors = multiprocessing.cpu_count()
    max_process = n_processors

    print("{} processors".format(n_processors))
    print("{} processes".format(max_process))

    for i in range(1, max_process):
        proc = multiprocessing.Process(target=simulation, args=(sumo_cmd,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
