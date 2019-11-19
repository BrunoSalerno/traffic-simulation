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
    vehid = 0

    while tdep <= maxtime:
        tint = -math.log(random.random()) / rate
        tdep += tint
        vehseq.append({
            'depart': tdep,
            'id':"{}_{}".format(veh_type, vehid),
            'route': routeid,
            'type': veh_type,
            'departLane': 'free',
            'departSpeed': 'desired'
        })

        vehid += 1
    return vehseq

def writeToFile(strList, filename):
    with open(filename, 'a') as filehandle:
        for str in strList:
            filehandle.write(str + '\n')

if __name__ == "__main__":
    total = 3600
    veh = 3000.0
    acc_proportion = 1
    filename = 'routes-1ACC'

    car_rate = veh * (1 - acc_proportion) / total
    acc_rate = veh * acc_proportion / total
   
    CAR = 'Car'
    ACC = 'ACC'

    seq = []
    seq.append('<routes>')
    seq.append('<vType id="{}" vClass="passenger"/>'.format(CAR))
    seq.append('<vType id="{}" vClass="passenger" carFollowModel="IDM" color="green"/>'.format(ACC))
    seq.append('<route id="r1" edges="link1 link2 link3 link4 link5"/>')

    all_vehicles =[]

    if car_rate > 0:
        all_vehicles += generateRandomVehicles(car_rate, total, "r1", CAR)

    if acc_rate > 0:
        all_vehicles += generateRandomVehicles(acc_rate, total, "r1", ACC)

    all_vehicles.sort(key = lambda i: i['depart'])
    for veh in all_vehicles:
        xml_str = "<vehicle"
        for key in veh:
            xml_str += ' {}="{}"'.format(key, veh[key])
        xml_str += ' />'
        seq.append(xml_str)

    seq.append('</routes>')

    writeToFile(seq, "{}.xml".format(filename))
