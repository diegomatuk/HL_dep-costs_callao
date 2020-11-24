import numpy as np
import pandas as pd
import requests
import json
from tqdm import tqdm
import math

zones = pd.read_csv('data.csv',engine = 'python')[['Longitud','Latitud']].values.tolist()
#DOSENT MATTER BEACUSE THEY ARE FREE KEYS (WITH A LIMIT )

keys = ["5b3ce3597851110001cf62484b5a677deef84813a41b445795184fd2",
        "5b3ce3597851110001cf6248d06de8ed9179499ea2f83309128acbfc",
        "5b3ce3597851110001cf6248528ad3c1233e44d3ae2e1774bfbba309"]


def deprivation_cost(time):
    return math.exp(1.5031 + 0.1172*time) + math.exp(1.5031)


##################CREATE THE JSONS FIRST##############################
#Sources : rows
#Destinations : columns
def osr(key, array, sources, destinations):
    body = {
        "locations": array,
        "destinations": destinations,
        "id": "matrix_request",
        "metrics": ["duration"],
        "resolve_locations": "false",
        "sources": sources,
    }

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml,img/png; charset=utf-8',
        'Authorization': key
    }
    response = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car',
                             json=body, headers=headers).json()

    return response

a = 0
for ix in (range(0, len(zones), 50)):
    for jx in (range(0, len(zones), 50)):
        c_keys = keys[a % 3]
        sources = [str(i) for i in range(ix, ix+50)]
        destinations = [str(j) for j in range(jx, jx+50)]
        try:
            query = osr(c_keys, zones, sources, destinations)
            with open(f"experimentation/osr/osr_matrix_{a}.json", "w") as f:
                json.dump(query, f)
        except:
            print("Error en ", a)
            pass
        a += 1


#FOR REMAINING GOOD values. SOURCES = ROW, DESTINATIONS = COLUMNS
a = 10
for ix in (range(0, len(zones), 50)):
    c_keys = keys[a % 3]
    sources = [str(i) for i in range(ix, ix+50)]
    destinations = [str(j) for j in range(500,518)]
    query = osr(c_keys, zones, sources, destinations)
    with open(f"experimentation/osr/osr_matrix_{a}.json", "w") as f:
        json.dump(query, f)
    a += 11

#LOWER PART OF THE BLOCK
a = 110
for ix in (range(0, len(zones), 50)):
    c_keys = keys[a % 3]
    sources = [str(i) for i in range(500, 518)]
    destinations = [str(j) for j in range(ix,ix+50)]
    query = osr(c_keys, zones, sources, destinations)
    with open(f"experimentation/osr/osr_matrix_{a}.json", "w") as f:
        json.dump(query, f)
    a += 1

# FOR THE FINAL MINI-BLOCK
sources = [str(i) for i in range(500, 518)]
destinations = [str(i) for i in range(500, 518)]


query = osr(c_keys, zones, sources, destinations)
with open(f"experimentation/osr/osr_matrix_120.json", "w") as f:
    json.dump(query, f)



#APPEND ALL THE MINI-BLOCKS TO A BIGGER ONE AND THEN COMPUTE THE DEPRIVATIONS COSTS
blocks = []

for i in range(0, 121):
    with open("experimentation/osr/osr_matrix_{}.json".format(i), 'r') as f:
        data = json.load(f)
    try:
        duratione = data["durations"]
        array = np.array(duratione)
        blocks.append(array)
    except:
        print("Error en: ".format(i))

#the number is always the amount of miniblocks (NxN) --> N being the amount of miniblocks
matrix = np.vstack([np.hstack(blocks[i:i+11]) for i in range(0, len(blocks), 11)])

#DATA IS IN SECONDS
np.savetxt("experimentation/time_matrix_day1.csv", matrix, delimiter=",")
matrix = matrix/3600

deprivation_cost = np.exp(1.5031 + 0.1172*matrix) + np.exp(1.5031)



np.savetxt('experimentation/dep_costs/dep_cost_day1.csv',deprivation_cost,delimiter = ',')
