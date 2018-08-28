#!/usr/bin/env python

"""WeWillRebuild.py: Reordering data from network telescope repo."""

"""
Obtain the data by cloning: https://github.com/zeroklone/network-telescope-data.git
Run this script in the base folder of the data.
"""

__author__ = "Brent Shaw"
__copyright__ = "Copyright 2018"
__credits__ = ["Brent Shaw", "Sean Devonport", "Motse Lehata"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Brent Shaw"
__email__ = "shaw@live.co.za"
__status__ = "Development"

import csv
import time
from collections import Counter
import os, zipfile
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

#Global nonsense
dataFiles = []

#Set current working directory
dir_name = os.getcwd()
os.chdir(dir_name)

#Prints the first n items of a list
def firstN(l, n, debug=False):
    count = 0
    while count < n:
        if debug:
            print(l[count])
        yield l[count]
        count = count + 1

#Finds all .zip files within the directory and sub-directories and extracts these
#If extracted already, the CSV files are added to the dataFiles list
def FindZipsAndExtract(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".zip"):
                path = root.split(os.sep)
                file_path = "/".join(path)+"/"
                if not os.path.isfile(file_path+file[:-4]):
                    zip_ref = zipfile.ZipFile(file_path+file)
                    print("Extracting: "+file_path+file)
                    zip_ref.extractall(file_path)
                    zip_ref.close()
                    #os.remove(file_name)
                else:
                    print("Found: "+file_path+file[:-4])
                    dataFiles.append(file_path+file[:-4])

    print("")

#Rebuild all files in the dataFiles list
#Load data
#Store usefull data in dict
#Sort dict by timestamp
#Store new csv
def RebuildData(df):
    for f in df:
        print("Rebuilding "+f.split("/")[-2]+"_"+f.split("/")[-1])

        data = {}
        sortedData = {}

        with open(f, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            filename = f.split("/")[-2]+"_"+f.split("/")[-1][:-4]

            header = "time_stamp,ip.length,ip.identification,ip.offset,ip.ttl,ip.checksum,ip.source,ip.destination,tcp.sequence,tcp.acknowledge,tcp.offset,tcp.flags_x,tcp.checksum,tcp.urgent_point,tcp_flags_binary_string_x,traffic_status_x,threat_type,time_index,seconds_in_day,sin_time,cos_time,well_known_src_port,well_known_dst_port,registered_src_port,registered_dst_port,ephemeral_src_port,ephemeral_dst_port,tcp.flags_y,tcp_flags_binary_string_y,traffic_status_y,country,country_iso,alpha_2_code,same_source,same_destination_portion,diff_port_portion,same_port_portion,same_dest_same_port_portion,same_dest_diff_port_portion,diff_dest_same_port_portion"

            for row in reader:
                data[row['time_stamp']] = [row["ip.length"],row["ip.identification"],row["ip.offset"],row["ip.ttl"],row["ip.checksum"],row["ip.source"],row["ip.destination"],row["tcp.sequence"],row["tcp.acknowledge"],row["tcp.offset"],row["tcp.flags_x"],row["tcp.checksum"],row["tcp.urgent_point"],row["tcp_flags_binary_string_x"],row["traffic_status_x"],row["threat_type"],row["time_index"],row["seconds_in_day"],row["sin_time"],row["cos_time"],row["well_known_src_port"],row["well_known_dst_port"],row["registered_src_port"],row["registered_dst_port"],row["ephemeral_src_port"],row["ephemeral_dst_port"],row["tcp.flags_y"],row["tcp_flags_binary_string_y"],row["traffic_status_y"],row["country"],row["country_iso"],row["alpha_2_code"],row["same_source"],row["same_destination_portion"],row["diff_port_portion"],row["same_port_portion"],row["same_dest_same_port_portion"],row["same_dest_diff_port_portion"],row["diff_dest_same_port_portion"]]

        sortedData = {k: data[k] for k in sorted(data)}

        with open('sorted/sorted_'+filename+'.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
            writer.writerow([header])
            for key, value in sortedData.items():
                writer.writerow([str(key)+','.join(value)])

#Lets go!
FindZipsAndExtract(dir_name)
RebuildData(dataFiles)
