from energy_functions import *




"""
CREATE OR REPLACE FUNCTION getQueryExecutionInfo(text) RETURNS text AS $$
DECLARE
startTime text;
endTime text;
executionPlan text;
insertedId int;
BEGIN
SELECT to_char(now(), 'YYYY-MM-DD HH24:MI:SS.MS') INTO startTime;
EXECUTE  $1 INTO executionPlan;
SELECT to_char(now(), 'YYYY-MM-DD HH24:MI:SS.MS') INTO endTime;
RETURN startTime || ';' || executionPlan || ';' || endTime;
END;
$$ LANGUAGE plpgsql;
"""


def get_query_energy(query, cursor, force_order):

    # Prepare query
    join_collapse_limit = "SET join_collapse_limit ="
    join_collapse_limit += "1" if force_order else "8"
    query = join_collapse_limit + "; EXPLAIN ANALYZE " + query

    # Prepare sensor
    psensor = findPowerSensor("YWATTMK1-1F6860.power")
    stopDataRecording(psensor)
    clearPowerMeterCache(psensor)
    tm = time.time()
    datalog = psensor.get_dataLogger()
    datalog.set_timeUTC(time.time())
    startDataRecording(psensor)  # Power Meter starts recording power per second
    time.sleep(2.0)
    print("4 - is recording: ", psensor.get_dataLogger().get_recording())

    # execute query
    cursor.callproc('getQueryExecutionInfo', (query,))
    endExecTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
    endExecTimeStr = datetime.strptime(endExecTime, '%Y-%m-%d %H:%M:%S:%f')

    result = cursor.fetchone()
    result = result[0].split(";")


    print("prc begin ",result[0])
    print("prc end ",endExecTime)

    (startTime, executionPlan, endTime) = (result[0], result[1], endExecTime)

    # print("4-4 - is recording: ", psensor.get_dataLogger().get_recording())
    print("startTime: ", startTime, " - endTime: ", endTime)
    # YAPI.Sleep(2000)
    time.sleep(2.0)
    print("stop recording : ", datetime.now())
    stopDataRecording(psensor)
    print("7 - is recording: ", psensor.get_dataLogger().get_recording())

    (power, exec_time, energy) = getAveragePower(psensor, startTime, endTime)


    return (power, exec_time, energy)


def get_query_latency(query, cursor, force_order):


    join_collapse_limit = "SET join_collapse_limit ="
    join_collapse_limit += "1;" if force_order else "8;"
    cursor.execute(join_collapse_limit)

    # Prepare query

    query = " EXPLAIN  ANALYSE " + query

    cursor.execute(query)

    rows = cursor.fetchall()
    row = rows[0][0]
    latency = float(rows[0][0].split("actual time=")[1].split("..")[1].split(" ")[0])
    
    return latency

if __name__ == "__main__":

    elements = ['3b','1a','32a','8a','7a','25a','19a','22a','24a','28a','29b']
    energy_tot = []
    latency_tot = []
    for element in elements:
        print("----------------------------------------------------------")
        print(element)
        with open('/home/said/Desktop/projects/jos_learned_rtos/JOB-queries/'+ str(element) + '.sql', 'r') as file:
            query = file.read()
        conn, cursor = connect_bdd("imdbload")

        # power, exec_time, energy = get_query_energy(query, cursor, False)

        latency =  get_query_latency(query, cursor, False)

        # energy_tot.append(energy)
        latency_tot.append(latency)

        print("latency : ",latency_tot)
        # print("energy : ",energy_tot)
        print("----------------------------------------------------------")

