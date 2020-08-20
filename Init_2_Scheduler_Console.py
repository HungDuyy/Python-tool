import re
from pathlib import Path
import os.path
from os import path
import os

print('\n\t\t\t ________________________________________________')
print('\n\t\t\t| Add Init to tpt_scheduler.c Tool - by Hung Duy |')
print('\n\t\t\t|                   Version 1.0                  |')
print('\n\t\t\t ------------------------------------------------')
print("\n         Usage:\n                - Enter SEDGE path with testdata folder inside\n")

# input #=================================================================================================================================================

try:
    print("\nStarting...\n")
    sedgepath = os.getcwd()

    results = []
    htmlUpath = sedgepath + '\\testdata\\FUSION_Platform\\ctcReport\\indexU.html'
    scheduler = sedgepath + '\\_targets\\default\\tpt_scheduler.c'
    if path.exists(htmlUpath) == True & path.exists(scheduler) == True:
        htmlU = open(htmlUpath).read()
        schedulerfile = open(scheduler).read()
        result2 = ''
        result3 = ''
        result4 = ''
        temp = ''
        i = 0
        # Modify .txt file #=====================================================================================================================================
        results = re.findall('([a-zA-Z0-9_]+nit)', htmlU)
        for listitem in results:
            temp = re.search(listitem, schedulerfile)
            if(temp == None):
                result2 = result2 + '\n' + 'void ' + listitem + '();'
                i = 1
            else:
                print('\n[INFO]: This Proc was available in tpt_scheduler.c: ',listitem)
        result3 = result2
        result4 = result2


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
            
        
        results = re.search('(void [a-zA-Z0-9_]+\(\);)', schedulerfile)
        temp = results[1] + '\n//Begin of added by tool ===============================' + result2 + '\n//End of added by tool ================================='
        schedulerfile = schedulerfile.replace(results[0],temp)
        
        results = re.search('(procs[\[\]= ]+{)', schedulerfile)
        temp = results[1] + '\n//Begin of added by tool ===============================' + result3 + '\n//End of added by tool ================================='
        schedulerfile = schedulerfile.replace(results[0], temp)
        
        results = re.search('(Pre_Proc[_INI\(\)]+;)', schedulerfile)
        temp = results[1] + '\n//Begin of added by tool ===============================' + result4 + '\n//End of added by tool ================================='
        schedulerfile = schedulerfile.replace(results[0], temp)
        
        #txtfile2 = result2 + '\n====================================================================================\n' +  result3 + '\n====================================================================================\n' + result4
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
