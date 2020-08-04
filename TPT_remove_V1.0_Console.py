import re
from pathlib import Path
import os.path
from os import path
import os

try:
    print("\nStarting...\n")
    sedge = os.getcwd()

    results = []

    for file in os.listdir(sedge):
        if file.endswith(".tpt"):
            tptfile = os.path.join(sedge, file) 
        if file.endswith("TPT.log"):
            tptlog = os.path.join(sedge, file)             
    if path.exists(tptfile) == True: 
        tptFile = open(tptfile).read()
    else:
        print('Not found tptfile in working space')
    if path.exists(tptlog) == True: 
        tptLog = open(tptlog).read()
    else:
        print('Not found tptlog in working space')
    #=====================================================================================================================================
    if path.exists(tptfile) == True: 
        tptFile = open(tptfile).read()
        i = 0
        results = re.search('([a-zA-Z0-9_]+)(xxx+[0-9])', tptFile)
        while results != None:
            i = 1
            result2 = results[1]
            tptFile = tptFile.replace(results[0], result2)
            results = re.search('([a-zA-Z0-9_]+)(xxx+[0-9])', tptFile)
        if i == 1:
            print('Success for tpt file!\n')
        tptFile1 = open(tptfile,'w')
        tptFile1.write(tptFile)
        tptFile1.close()
    else:
        print("\nNot found tptfile in working space\n")
    #================================================================================================== 
    if path.exists(tptlog) == True: 
        tptLog = open(tptlog).read()
        i = 0
        results = re.search('([a-zA-Z0-9_]+)(xxx+[0-9])', tptLog)
        while results != None:
            i = 1
            result2 = results[1]
            tptLog = tptLog.replace(results[0], result2)
            results = re.search('([a-zA-Z0-9_]+)(xxx+[0-9])', tptLog)
        if i == 1:
            print('Success for tpt log!\n')
        tptLog1 = open(tptlog,'w')
        tptLog1.write(tptLog)
        tptLog1.close()
    else:
        print("\nNot found tpt log in working space\n")   
              
    print("\nTool run completed ...")

except ValueError as outputError:
    print(outputError)  
    os.system("pause")
#os.system("pause")
