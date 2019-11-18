import math
import random

"""
Example of how to write SUMO scenario inputs in sumo-xml format using a python script for Lab2.
Can use the same method to generate other inputs as needed.
"""


def generateRandomVehicles(rate, maxtime, routeid, veh_type, seq):
    """
    #Ex: <vehicle depart="30" id="veh0" route="r1" type="Car"/>
    """
    tdep = 0.0

    vehid = 0
    while tdep <= maxtime:
        tint = -math.log(random.random()) / rate
        tdep += tint
        seq.append('<vehicle depart="{}" id="veh{}" route="{}" type="{}" departLane="{}" departSpeed="{}"/>'.format(tdep, vehid, routeid, veh_type, 'free', 'desired'))
        vehid += 1

def writeToFile(strList, filename):
    with open(filename, 'a') as filehandle:
        for str in strList:
            filehandle.write(str + '\n')

if __name__ == "__main__":
    total = 3600
    acc_rate = 0.5
    CAR = 'Car'
    ACC = 'ACC'

    seq = []
    seq.append('<routes>')
    seq.append('<vType id="{}" vClass="passenger"/>'.format(CAR))
    seq.append('<vType id="{}" vClass="passenger"><carFollowing-IDM/></vType>'.format(ACC))
    seq.append('<route id="r1" edges="link1 link2 link3 link4 link5"/>')

    generateRandomVehicles(0.8333, total * (1 - acc_rate), "r1", CAR, seq)
    generateRandomVehicles(0.8333, total * acc_rate, "r1", ACC, seq)

    seq.append('</routes>')
    
    writeToFile(seq, "routes.xml")
