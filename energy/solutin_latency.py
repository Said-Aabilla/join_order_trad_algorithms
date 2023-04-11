from algos.helper_functions import get_query_latency
from energy_functions import *


if __name__ == "__main__":

    elements = ['3b','1a','32a','8a','7a','25a','19a','22a','24a','28a','29b']

    latency_tot = []
    for element in elements:
        print("----------------------------------------------------------")
        print(element)
        with open('/home/said/Desktop/projects/jos_learned_rtos/JOB-queries/'+ str(element) + '.sql', 'r') as file:
            query = file.read()
        conn, cursor = connect_bdd("imdbload")


        latency =  get_query_latency(query, False)

        latency_tot.append(latency)

        print("latency : ",latency_tot)
        print("----------------------------------------------------------")
#         latency :  [243.182, 153.767, 23.545, 299.651, 7.969, 824.902, 457.402, 559.342, 450.075, 627.022, 101.275]

