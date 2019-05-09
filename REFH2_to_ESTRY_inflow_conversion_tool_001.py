# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:58:41 2019

@author: simon.desmet
"""

#REFH2  to ESTRY inflow conversion tool

import pandas as pd
import os
import glob


REFH2datafolder = raw_input("file path for REFH2 output files please:")
outPutPath = raw_input("file path for output files please:")

os.chdir(REFH2datafolder)#sets the path for working folder to current directory

os.getcwd()#prints current directory to see if the above has worked.


REFH2resultsList = []#empty list for REFH csv files
nodeNames = []#empty list for the names of each node in REFH2 outputs
stormDurations = []# empty list for each stormDuration in REFH2 outputs

for filename in glob.glob('*hrs.csv'): #defines new variable 'filename'loops through workingfolder and adds each 'filename' with hrs.csv in it to a list
    print filename
    REFH2resultsList.append(filename)
    # we now have a list of csv files with REFH2 results in them.
    filenameBits = filename[:-4].split(' ')
    nodeNames.append(filenameBits[0])
    stormDurations.append(filenameBits[1])
    # for each CSV we seperate the file name by the spaces and take the first string and add it to the nodeNames list and second string (having dropped .csv and add it to the durations list)
    
nodeNames = set(nodeNames) # drop all duplicates in list using set function
print nodeNames

stormDurations = set(stormDurations) # drop all duplicates in list using set function
print stormDurations

# get list of returns out of one file by opening a file, taking the headers as a list, stripping them down to just the 'total flow' headers and then stripping to the retun periods

lastfileHeaders = pd.read_csv(filename, header=0) # reads the last filename into python pandas from csv
csvheaderList = list(lastfileHeaders) # takes the headers in the pandas dataframe and puts them into a list
totalFlowHeaders = []# blank list for holding the headers with total flows in them
returnPeriods = []# blank list for holding

for header in csvheaderList: # get list of all headers with 'total flow' in them
    if 'Total flow' in header:
        totalFlowHeaders.append(header)
        
        
for flowHeader in totalFlowHeaders:
    flowHeaderBits = flowHeader.split(' ')
    unformatedReturn = flowHeaderBits[-4]
    formatedReturn = unformatedReturn[1:]
    returnPeriods.append(formatedReturn)
print returnPeriods

# loop through returns create a results file for each return period and each duration

#loop through returns
for returnPeriod in returnPeriods:
    #loop through durations
    for duration in stormDurations:
        #create new dataframe
        outputname = returnPeriod+'_'+duration
        print outputname
        # get a results file of correct duration and copy it for base dataframe to copy results too
        for csv in REFH2resultsList:
            if duration in csv:
               duration_DF = pd.read_csv(csv, header=0) 
               working_DF = duration_DF['Time']# gets dataframe with just time column.
               working_DF = working_DF.to_frame()#error was occuring at .join as working_DF was not a dataframe for some reason
               break
            else:
               continue
           
           
        # copy in relevant data
        for csv in REFH2resultsList:
            if duration in csv:
                openCsv_DF = pd.read_csv(csv, header=0)
                csvHeadersList = list(openCsv_DF)
                columntoCopy = []
                for head in csvHeadersList:
                    if 'Total flow m3/s ('+returnPeriod+' year)- urbanised model' in head:
                        #working_DF = working_DF+openCsv_DF[head]
                        head_DF = openCsv_DF[head]
                        head_DF = head_DF.to_frame()
                        #rename column header to node
                        csvBits = csv.split(' ')
                        nodeforHeader = csvBits[0]
                        print nodeforHeader
                        head_DF.columns = [nodeforHeader]
                        holding_DF = working_DF.join(head_DF, how='left')
                        working_DF = holding_DF
                    else:
                        continue
            
        outputString = outPutPath+'\\REFH2'+'_'returnPeriod+'F_'+duration+'_ESTRY.csv'    
        working_DF.to_csv(outputString, sep=',')
        








# automatically generate climate change variants



