"""
record() logs sensor and valve data to a .csv file. Typically instantiated as a multiprocessing.processimport time
"""
import datetime
import time
import csv
import os

def record(poke1, poke2, lines, starttime, endtime, anID):
    print("recording started")
    now = datetime.datetime.now()
    d = now.strftime("%m%d%y_%Hh%Mm")
    localpath = os.getcwd()
    filepath = localpath + "/" + anID + "_" + d + ".csv"
    with open(filepath, mode='w') as record_file:
        fieldnames = ['Time', 'Poke1', 'Poke2', 'Line1', 'Line2', 'Line3', 'Line4']
        record_writer = csv.writer(record_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        record_writer.writerow(fieldnames)
        while time.time() < endtime:
            t = round(time.time() - starttime, 2)
            data = [str(t), str(poke1.is_crossed()), str(poke2.is_crossed())]
            for item in lines:
                if item.is_open:
                    valvestate = item.taste
                else:
                    valvestate = "None"
                data.append(str(valvestate))
            record_writer.writerow(data)
            time.sleep(0.005)
    print("recording ended")
    record_file.close()