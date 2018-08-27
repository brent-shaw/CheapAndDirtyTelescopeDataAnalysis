#!/usr/bin/env python

"""AnalyseThatShit.py: Provides rudimentary analysis of telescope data."""

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

# import git
# cwd = os.getcwd()
# git.Git(cwd).clone("https://github.com/zeroklone/network-telescope-data.git")

#Global nonsense
dataFiles = []
sourceIP0 = {}
sourceIP1 = {}
sourceIP2 = {}
sourceIP3 = {}
sourceIPs = {}
destinationIPs = {}
countries = {}
delays = {}
logs = []

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

#OLD
#Finds all .csv files within the directory and sub-directories and adds to the dataFiles list
def FindCSVs(dir):
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            if file.endswith(".csv"):
                path = root.split(os.sep)
                file_path = "/".join(path)+"/"
                print("Found: "+file_path+file)
                dataFiles.append(file_path+file)
    print("")

#Removes all files listed in the dataFiles list
def Remove(df):
    for f in df:
        os.remove(f)
    print("All gone")

#Write out logs
def StoreAnalysisLogs(logs):
    for log in logs:
        print("Stroing "+log[0])
        with open(log[0]+".log", 'w') as outfile:
            for line in log[1]:
                outfile.write(str(line)+'\n')

#Analyses all files in the dataFiles list
#Frequency analysis of the following: Source IPs, Countries of origin, and most frequently seen IPs by network class
def RebuildData(df):
    for f in df:
        print("Rebuilding "+f.split("/")[-2]+"_"+f.split("/")[-1])

        data = {}
        sortedData = {}

        with open(f, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            filename = f.split("/")[-2]+"_"+f.split("/")[-1][:-4]

            header = "time_stamp, ip.source, ip.destination, country_iso"

            for row in reader:
                data[row['time_stamp']] = [row['ip.source'], row['ip.destination'], row['country_iso']]

        sortedData = {k: data[k] for k in sorted(data)}

        with open('sorted/sorted_'+filename+'.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='\n', quotechar='|')
            writer.writerow([header])
            for key, value in sortedData.items():
                writer.writerow([str(key)+','+str(value[0])+','+str(value[1])+','+str(value[2])])

#Lets go!
FindZipsAndExtract(dir_name)
RebuildData(dataFiles)
