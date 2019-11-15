import multiprocessing
import traci

def simulation(cmd):
    traci.start(cmd)
    i = 1
    laststep = 1800

    while i <= laststep:
        traci.simulationStep()
        IDList = traci.vehicle.getIDList()
        i += 1
        if len(IDList):
            print IDList
        
    traci.close()

if __name__ == "__main__":

    sumo_exe = "sumo"
    conf_file = "config.xml"  # the configuration file
    sumo_cmd = [sumo_exe, "-c", conf_file]

    procs = []
    max_process = multiprocessing.cpu_count()
    for i in range(1, max_process):
        proc = multiprocessing.Process(target=simulation, args=(sumo_cmd,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
