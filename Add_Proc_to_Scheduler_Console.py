import re
from pathlib import Path
import os.path
from os import path
import os

print('\n\t\t\t ___________________________________________________________________')
print('\n\t\t\t| Add Missing PROC INIT & RUN to tpt_scheduler.c Tool - by Hung Duy |')
print('\n\t\t\t|                              Version 1.0                          |')
print('\n\t\t\t -------------------------------------------------------------------')
print("\n         Usage:\n                - Enter SEDGE path with testdata folder inside\n")

# input #                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/=====================

try:
    print("\nStarting...\n")
    sedgepath = os.getcwd()

    results = []
    resultsRun = []
    moveproc = []
    moveproc2 = []
    proctomove = []
    proctomove2 = ''
    htmlUpath = sedgepath + '\\testdata\\FUSION_Platform\\ctcReport\\indexU.html'
    scheduler = sedgepath + '\\_targets\\default\\tpt_scheduler.c'
    if path.exists(htmlUpath) == True & path.exists(scheduler) == True:
        htmlU = open(htmlUpath).read()
        schedulerfile = open(scheduler).read()
        result2 = ''
        result3 = ''
        result4 = ''
        result2run = ''
        result3run = ''
        result4run = ''
        temp = ''
        i = 0
        # Modify .txt file #                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/=========
        results = re.findall('([a-zA-Z0-9_]+nit\(\))', htmlU)
        resultsRun = re.findall('([a-zA-Z0-9_]+Run\(\))', htmlU)
        for listitem in results:
            temp = re.search(listitem, schedulerfile)
            if(temp == None):
                result2 = result2 + '\n' + 'void ' + listitem + ';'
                i = 1
        result3 = result2
        result4 = result2
        for listitem in resultsRun:
            temp = re.search(listitem, schedulerfile)
            if(temp == None):
                result2run = result2run + '\n' + 'void ' + listitem + ';'
                i = 1
        result3run = result2run
        result4run = result2run


        results = re.search('(void )([a-zA-Z0-9_]+nit)(\(\);)', result3)
        while results != None:
            temp = '{\t"' + results[2] + '",\n\t&' + results[2] + ',\n\tTINI},'
            result3 = result3.replace(results[0], temp)
            results = re.search('(void )([a-zA-Z0-9_]+nit)(\(\);)', result3)
            
        results = re.search('(void )([a-zA-Z0-9_]+nit)(\(\);)', result4)
        while results != None:
            temp = '\t' + results[2] + '();' 
            result4 = result4.replace(results[0], temp)
            results = re.search('(void )([a-zA-Z0-9_]+nit)(\(\);)', result4)
        #Run
        resultsRun = re.search('(void )([a-zA-Z0-9_]+Run)(\(\);)', result3run)
        while resultsRun != None:
            temp = '{\t"' + resultsRun[2] + '",\n\t&' + resultsRun[2] + ',\n\tT10MS},'
            result3run = result3run.replace(resultsRun[0], temp)
            resultsRun = re.search('(void )([a-zA-Z0-9_]+Run)(\(\);)', result3run)
            
        resultsRun = re.search('(void )([a-zA-Z0-9_]+Run)(\(\);)', result4run)
        while resultsRun != None:
            temp = '\t' + resultsRun[2] + '();' 
            result4run = result4run.replace(resultsRun[0], temp)
            resultsRun = re.search('(void )([a-zA-Z0-9_]+Run)(\(\);)', result4run)
            
        #Syn0
        moveproc = re.search('(SEDGe_Pre_Proc_SYNC_TASK0[{\n\ta-zA-Z0-9_?+= \)\(;]+})', schedulerfile)
        if moveproc != None:
            #move Run
            proctomove = re.findall('([a-zA-Z0-9_]+_Run\(\);)', moveproc[0])
            moveproc2 = moveproc[0]
            for listitem in proctomove:
                moveproc2 = moveproc2.replace(listitem, '//Moved to PROC 10ms: ' + listitem)
                proctomove2 = proctomove2 + '\n\t' + listitem
            #move Sync
            proctomove = re.findall('([a-zA-Z0-9_]+_Sync\(\);)', moveproc[0])
            for listitem in proctomove:
                moveproc2 = moveproc2.replace(listitem, '//Moved to PROC 10ms: ' + listitem)
                proctomove2 = proctomove2 + '\n\t' + listitem
            schedulerfile = schedulerfile.replace('TSYNCRO0}', 'T10MS}') 
            schedulerfile = schedulerfile.replace(moveproc[0], moveproc2)
        #Syn1
        moveproc = re.search('(SEDGe_Pre_Proc_SYNC_TASK1[{\n\ta-zA-Z0-9_?+= \)\(;]+})', schedulerfile)
        if moveproc != None:
            #move Run
            proctomove = re.findall('([a-zA-Z0-9_]+_Run\(\);)', moveproc[0])
            moveproc2 = moveproc[0]
            for listitem in proctomove:
                moveproc2 = moveproc2.replace(listitem, '//Moved to PROC 10ms: ' + listitem)
                proctomove2 = proctomove2 + '\n\t' + listitem
            #move Sync
            proctomove = re.findall('([a-zA-Z0-9_]+_Sync\(\);)', moveproc[0])
            for listitem in proctomove:
                moveproc2 = moveproc2.replace(listitem, '//Moved to PROC 10ms: ' + listitem)
                proctomove2 = proctomove2 + '\n\t' + listitem
            schedulerfile = schedulerfile.replace('TSYNCRO1}', 'T10MS}') 
            schedulerfile = schedulerfile.replace(moveproc[0], moveproc2)
        #Syn2
        moveproc = re.search('(SEDGe_Pre_Proc_SYNC_TASK2[{\n\ta-zA-Z0-9_?+= \)\(;]+})', schedulerfile)
        if moveproc != None:
            #move Run
            proctomove = re.findall('([a-zA-Z0-9_]+_Run\(\);)', moveproc[0])
            moveproc2 = moveproc[0]
            for listitem in proctomove:
                moveproc2 = moveproc2.replace(listitem, '//Moved to PROC 10ms: ' + listitem)
                proctomove2 = proctomove2 + '\n\t' + listitem
            #move sync
            proctomove = re.findall('([a-zA-Z0-9_]+_Sync\(\);)', moveproc[0])
            for listitem in proctomove:
                moveproc2 = moveproc2.replace(listitem, '//Moved to PROC 10ms: ' + listitem)
                proctomove2 = proctomove2 + '\n\t' + listitem
            schedulerfile = schedulerfile.replace('TSYNCRO2}', 'T10MS}') 
            schedulerfile = schedulerfile.replace(moveproc[0], moveproc2)       
            
        if proctomove2 != None:
            proctomove2 = '\n/*\tList moved from PROC Sync:\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/' + proctomove2
        if result2run != None:
            result2run = '\n/*\tList of PROC Run:\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/' + result2run
        if result3run != None:
            result3run = '\n/*\tList of PROC Run:\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/' + result3run
            
        results = re.search('(void [a-zA-Z0-9_]+\(\);)', schedulerfile)
        temp = results[1] + '\n/* Begin of added by tool\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/\n/*\tList of PROC Init:\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/' + result2 + result2run + '\n/* End of added by tool\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/'
        schedulerfile = schedulerfile.replace(results[0],temp)
        
        results = re.search('(procs[\[\]= ]+{)', schedulerfile)
        temp = results[1] + '\n/* Begin of added by tool\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/\n/*\tList of PROC Init:\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/' + result3 + result3run + '\n/* End of added by tool\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/'
        schedulerfile = schedulerfile.replace(results[0], temp)
        
        results = re.search('(Pre_Proc[_INI\(\)]+;)', schedulerfile)
        temp = results[1] + '\n/* Begin of added by tool\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/' + result4 + '\n/* End of added by tool\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/'
        schedulerfile = schedulerfile.replace(results[0], temp)
        
        results = re.search('(Pre_Proc_10ms[\(\)]+;)', schedulerfile)
        temp = results[1] + '\n/* Begin of added by tool\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/' + result4run + proctomove2 +'\n/* End of added by tool\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/'
        schedulerfile = schedulerfile.replace(results[0], temp)
        
        
        #txtfile2 = result2 + '\n                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/======================\n' +  result3 + '\n                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/                              \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t*/======================\n' + result4
        #schedulerfiletowrite = open(scheduler,'w')
        if i == 1:
            if path.exists(scheduler + '_old') == False:
                os.rename(scheduler, scheduler.replace('.c', '.c_old'))
            schedulerfiletowrite = open((os.path.splitext(scheduler)[0]) + ".c", 'w')
            schedulerfiletowrite.write(schedulerfile)
            schedulerfiletowrite.close()
        else: 
            print('[WARNING]: Have nothing to add to tpt_scheduler.c !\n')
        print("\nTool run completed ...\n")
    else:
        print("[WARNING]: Stop run due to not found 'testdata' folder or 'tpt_scheduler.c' file in SEDGE path...\n")
    
except ValueError as outputError:
    print('[ERROR]: ',outputError)  

#os.system("pause")
