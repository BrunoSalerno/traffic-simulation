import math
import random

"""
Example of how to write SUMO scenario inputs in sumo-xml format using a python script for Lab2.
Can use the same method to generate other inputs as needed.
"""


def generateRandomVehicles(rate, maxtime, routeid, veh_type):
    """
    #Ex: <vehicle depart="30" id="veh0" route="r1" type="Car"/>
    """
    tdep = 0.0
    vehseq = []

    vehseq.append('<routes>')
    vehseq.append('<vType id="Car" vClass="passenger"/>')
    vehseq.append('<route id="r1" edges="link1 link2 link3 link4 link5"/>')

    #TODO: see if it makes sense to set a depart speed

    vehid = 0
    while tdep <= maxtime:
        tint = -math.log(random.random()) / rate
        tdep += tint
        vehseq.append('<vehicle depart="{}" id="veh{}" route="{}" type="{}" departLane="free"/>'.format(tdep, vehid, routeid, veh_type))
        vehid += 1

    vehseq.append('</routes>')
    return vehseq


def writeToFile(strList, filename):
    with open(filename, 'a') as filehandle:
        for str in strList:
            filehandle.write(str + '\n')


if __name__ == "__main__":
    # Example of usage
    seq = generateRandomVehicles(0.8333, 3600, "r1", "Car")  # Note: remember to change your rate to the correct time units!
    writeToFile(seq, "routes.xml")
