import time

from algos.helper_functions import get_query_latency
from energy_functions import *


if __name__ == "__main__":

    elements = ['3b','1a','32a','8a','7a','25a','19a','22a','24a','28a','29b']

    latency_tot = []
    energy_tot = []

    for element in elements:
        print("----------------------------------------------------------")
        print(element)
        # with open('/home/said/Desktop/projects/RTOS (copy)/new-solutions/'+ str(element) + '.sql', 'r') as file:
        with open('/home/said/Desktop/projects/RTOS (copy)/JOB-queries/'+ str(element) + '.sql', 'r') as file:
            query = file.read()
        conn, cursor = connect_bdd("imdbload")

        start = time.time()
        latency =  get_query_latency(query, False)
        end = time.time()
        # Calculate time difference in milliseconds
        time_diff_ms = (end - start) * 1000

        # Print result in milliseconds
        print("Time taken: {:.2f} ms".format(time_diff_ms))
        # (power, exec_time, energy) =  get_query_exec_energy(query, True)
        #
        # latency_tot.append(latency)
        # energy_tot.append(energy)

        print("latency : ",latency_tot)
        # print("energy : ",energy_tot)
        print("----------------------------------------------------------")
#         latency :  [243.182, 153.767, 23.545, 299.651, 7.969, 824.902, 457.402, 559.342, 450.075, 627.022, 101.275]

