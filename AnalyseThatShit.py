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

#Set current working directory
dir_name = os.getcwd()
os.chdir(dir_name)

#Prints the first n items of a list
def firstN(l, n):
    count = 0
    while count < n:
        print(l[count])
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

#Analyses all files in the dataFiles list
#Frequency analysis of the following: Source IPs, Countries of origin, and most frequently seen IPs by network class
def AnalyseFiles(df):
    for f in df:
        print("Analysis of: "+f.split("/")[-1])
        with open(f, 'r') as csvfile:

            reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
            for row in reader:
                if "time_stamp" in row:
                    pass
                else:
                    parts = row[0].split(',')
                    octets = parts[6].split('.')

                    #This builds the frequency analysis dictionaries
                    #Long and slow :)
                    try:
                        if parts[0] in sourceIPs:
                            sourceIPs[parts[6]] += 1
                        else:
                            sourceIPs[parts[6]] = 1

                        if octets[0] in sourceIP0:
                            sourceIP0[octets[0]] += 1
                        else:
                            sourceIP0[octets[0]] = 1

                        if octets[1] in sourceIP1:
                            sourceIP1[octets[1]] += 1
                        else:
                            sourceIP1[octets[1]] = 1

                        if octets[2] in sourceIP2:
                            sourceIP2[octets[2]] += 1
                        else:
                            sourceIP2[octets[2]] = 1

                        if octets[3] in sourceIP3:
                            sourceIP3[octets[3]] += 1
                        else:
                            sourceIP3[octets[3]] = 1

                        if parts[31] in countries:
                            countries[parts[31]] += 1
                        else:
                            countries[parts[31]] = 1
                    except:
                        pass

        #Print Source IPs
        s = [(p, sourceIPs[p]) for p in sorted(sourceIPs, key=sourceIPs.get, reverse=True)]
        print("Source IPs")
        firstN(s,30)
        print("")

        #Print Countries
        s = [(p, countries[p]) for p in sorted(countries, key=countries.get, reverse=True)]
        print("Country of Origin")
        firstN(s,30)
        print("")

        #Print Class A Octect results
        s = [(p, sourceIP0[p]) for p in sorted(sourceIP0, key=sourceIP0.get, reverse=True)]
        print("Class A range")
        firstN(s,30)
        print("")

        #Print Class B Octect results
        s = [(p, sourceIP1[p]) for p in sorted(sourceIP1, key=sourceIP1.get, reverse=True)]
        print("Class B range")
        firstN(s,30)
        print("")

        #Print Class C Octect results
        s = [(p, sourceIP2[p]) for p in sorted(sourceIP2, key=sourceIP2.get, reverse=True)]
        print("Class C range")
        firstN(s,30)
        print("")

        #Print Class D Octect results
        s = [(p, sourceIP3[p]) for p in sorted(sourceIP3, key=sourceIP3.get, reverse=True)]
        print("Class D range")
        firstN(s,30)
        print("")

        print(" ---")

#Lets go!
FindZipsAndExtract(dir_name)
AnalyseFiles(dataFiles)
