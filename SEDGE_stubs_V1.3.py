import re
from pathlib import Path
import os.path
from os import path
import os

print('\n\t\t\t _______________________________________')
print('\n\t\t\t| SEDGE_stubs Modify Tool - by Hung Duy |')
print('\n\t\t\t|             Version 1.3               |')
print('\n\t\t\t --------------------------------------- ')
print("\n\n      Usage:\n          - Enter Pver path\n          - Enter SEDGE folder path\n\n          -> Rte_FC.h file will be modify Tx, Rx, Ms\n          -> sedge_stubs.c file will be added all RTE Interface from Rte.c")

# input #=================================================================================================================================================
print("\nEnter Pver path: ")
pver = input()
while path.exists(pver) == False:
    print("\nNot found the Pver path above ...\n\nPlease Enter right Pver path again: ")
    pver = input()
print("\nEnter SEDGE FC path:")
sedge = input()
while path.exists(sedge) == False:
    print("\nNot found the SEDGE FC path above ...\n\nPlease Enter right SEDGE FC path again: ")
    sedge = input()

try:
    print("\nStarting...\n")
    results = []
    mesage = ''
    stubfile = sedge + '\\_stubs\\sedge_stubs.c'
    rtefile = pver + '\\_gen\\swb\\filegroup\\src_files\\rtegen\\Rte.c' 
    results = re.search('([a-zA-Z0-9: \\\,\(\)\/\-._]+\\\)(([a-zA-Z0-9]+[a-zA-Z_]+[a-zA-Z]))',sedge)
    module = results[2]
    rteFile = open(rtefile).read()
    result2 = ''
    print("\n[INFO]: FC name to run: ",module,'\n')
    # Modify .h file #=====================================================================================================================================
    rteHfile = sedge + '\\includes\\inc\\Rte_'+module+ '.h' 
    if path.exists(rteHfile) == True: 
        rteHFile = open(rteHfile).read()
        i = 0
        results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)', rteHFile)
        while results != None:
            i = 1
            result2 = results[2] + '_RTE'
            rteHFile = rteHFile.replace(results[0], result2)
            results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)', rteHFile)

        if i == 1:
            #print('Success for Rte_%s.h file!\n' %module)
            mesage = mesage + '\t[INFO]: Success for Rte_' + module + '.h file!\n'
        else:
            #print('Not found any point to modify in Rte_%s.h file!\n' %module)
            mesage = mesage + '\t[WARNING]: Not found any point to modify in Rte_' + module + '.h file!\n'
        rteH_File = open(rteHfile,'w')
        rteH_File.write(rteHFile)
        rteH_File.close()
    else:
        #print("\nFile Rte_%s.h not found!\n" %module)
        mesage = mesage + '\t[ERROR]: File Rte_' + module + '.h not found!\n'
    #Copy data from Rte.c to sedge_stubs.c #================================================================================================================
    hFile = '#include "RTE_Type.h"\n#include "dll_stubs.h"\n#include "Sedge_MsgDef.h"\n#include "Sedge_stubs.h"\n'
    
    results = re.findall('(FUNC[\(\)_a-zA-Z0-9,\- ]+Rte_[a-zA-Z0-9_]+'+module+'[a-zA-Z_]+\([a-zA-Z0-9]+\(DT_[a-zA-Z_, \)\&]+;)', rteFile) 
    for listitem in results:
        hFile = hFile + '\n' + listitem
    results = re.findall('(FUNC[\(\)_a-zA-Z0-9,\- ]+\nRte_[a-zA-Z0-9_]+'+module+'[_a-zA-Z_0-9\(, \)/*\n;:\-={.\t\r+&?]+})', rteFile) 
    for listitem in results:
        hFile = hFile + '\n' + listitem
    #Init variable #========================================================================================================================================
    i = 0 #flag to check copy Rte_memcpy()
    duplicate = []
    temp = ''
    result1 = ''
    result2 = ''
    # Read RTE Array #====================================================================================================================================== 
    results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)(, sizeof\()(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+\))', hFile)
    while results != None:
        i = 1 #flag to check copy Rte_memcpy()
        result1 = results[5]
        result1 = result1.replace(')','_RTE)')
        result2 = results[2] + '_RTE' + results[3] + result1 #+ '_RTE)'#(&\2_RTE\3\5_RTE)
        print('[INFO]: <Read-ARRAY> Replace for ', result1)
        hFile = hFile.replace(results[0], result2)
        results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)(, sizeof\()(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+\))', hFile)
    # Write RTE Array #======================================================================================================================================    
    results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)(, data, sizeof\()(DA_)([a-zA-Z0-9_]+\))', hFile)
    while results != None:
        i = 1 #flag to check copy Rte_memcpy()
        result1 = results[5]
        result1 = result1.replace(')','_RTE)')
        result2 = results[2] + '_RTE' + results[3] + result1 #+ '_RTE\)'#(\2_RTE\3\5_RTE)
        print('[INFO]: <Write-ARRAY> Replace for ', result1 )
        hFile = hFile.replace(results[0], result2)
        results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)(, data, sizeof\()(DA_)([a-zA-Z0-9_]+\))', hFile)
    # Read not array  1 #=====================================================================================================================================
    # results = re.search('(rtn = [a-zA-Z0-9_\(]+DA_)([a-zA-Z0-9_]+)([a-zA-Z_0-9, \)\(]+\))', hFile)
    # while results != None:
        # result2 = '(*(data)) = ' + results[2] + '_RTE;\n   rtn = ((VAR(Std_ReturnType, AUTOMATIC))RTE_E_OK)'
        # print('Replace for ', result2 )
        # hFile = hFile.replace(results[0], result2)
        # results = re.search('(rtn = [a-zA-Z0-9_\(]+DA_)([a-zA-Z0-9_]+)([a-zA-Z_0-9, \)\(]+\))', hFile)
    # Read not array #========================================================================================================================================
    results = re.search('(rtn[ =a-zA-Z]+_)(Rte[_RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)([\(\), _a-zA-Z0-9]+;)', hFile)
    while results != None:
        result2 = '(*(data)) = ' + results[3] + '_RTE;\n   rtn = ((VAR(Std_ReturnType, AUTOMATIC))RTE_E_OK);'
        print('[INFO]: Replace for %s_RTE' %results[3] )
        hFile = hFile.replace(results[0], result2)
        results = re.search('(rtn[ =a-zA-Z]+_)(Rte[_RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)([\(\), _a-zA-Z0-9]+;)', hFile)
    # Write RTE not Array 1 #=================================================================================================================================
    results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)( =[\(a-zA-Z0-9_, \)]+;)', hFile)
    while results != None:
        result2 = results[2] + '_RTE = data;'
        temp = 'Rte_memcpy\(' + results[2] + '_RTE'
        duplicate = re.search('('+temp+')',hFile)
        if duplicate == None:
            temp = results[2] + '_RTE = data;'
            duplicate = re.search('('+temp+')',hFile)
            if duplicate == None:
                print('[INFO]: Replace for %s_RTE' %results[2])
                hFile = hFile.replace(results[0], result2)
            else:
                result2 = '//Duplicate RTE was removed'
                hFile = hFile.replace(results[0], result2)
        else:
                result2 = '//Duplicate RTE in memcpy() was removed'
                hFile = hFile.replace(results[0], result2)
        results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)( =[\(a-zA-Z0-9_, \)]+;)', hFile)
    # Write RTE not Array 2 #=================================================================================================================================
    results = re.search('(\(void\)IocWrite_Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)([\(\)a-zA-Z0-9_, ]+;)', hFile)
    while results != None:
        result2 = results[2] + '_RTE = data;'
        temp = 'Rte_memcpy\(' + results[2] + '_RTE'
        duplicate = re.search('('+temp+')',hFile)
        if duplicate == None:
            temp = results[2] + '_RTE = data;'
            duplicate = re.search('('+temp+')',hFile)
            if duplicate == None:
                print('[INFO]: Replace for %s_RTE' %results[2] )
                hFile = hFile.replace(results[0], result2)
            else:
                result2 = '//Duplicate RTE was removed'
                hFile = hFile.replace(results[0], result2)
        else:
                result2 = '//Duplicate RTE in memcpy() was removed'
                hFile = hFile.replace(results[0], result2)
        results = re.search('(\(void\)IocWrite_Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)([\(\)a-zA-Z0-9_, ]+;)', hFile)
    # cover all case at least #===============================================================================================================================

    # results = re.search('(Ioc[a-zA-Z0-9]+_Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)', hFile)
    # while results != None:
        # if x == 0:
        # result2 = results[2] + '_RTE'
        # print('Replace for ', result2 )
        # hFile = hFile.replace(results[0], result2)
        # results = re.search('(Ioc[a-zA-Z0-9]+_Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)', hFile)
            
    results = re.search('(Rte[RxMsT_]+_[0-9]+_)([a-zA-Z0-9_]+)', hFile)
    while results != None:
        result2 = results[2] + '_RTE'
        print('[INFO]: Replace for ', result2 )
        hFile = hFile.replace(results[0], result2)
        results = re.search('(Rte[RxMsT_]+_[0-9]+_)([a-zA-Z0-9_]+)', hFile)
    # Copy Rte_memcpy() #====================================================================================================================================== 
    if i == 1:
        rte_libfile = pver + '\\_gen\\swb\\filegroup\\src_files\\rtegen\\Rte_Lib.c' #\_gen\swb\filegroup\src_files\rtegen
        if path.exists(rte_libfile) == True: 
            rte_libFile = open(rte_libfile).read()
            results = re.findall('(FUNC\([a-zA-Z, _]+\)\nRte_memcpy[_a-zA-Z_0-9\(, \)/*\n;:\-={}.\t\r+]+})', rte_libFile)
            for listitem in results:
                hFile = hFile + '\n' + listitem
        else:
            #print('\nNot found Rte_Lib.c in Pver path')
            mesage = mesage + '\t[ERROR]: Not found Rte_Lib.c in Pver path - Can\'t copy memcpy() function to sedge_stubs.c\n'
    # Remove GetResource #======================================================================================================================================          
    hFile = hFile.replace('Rte_GetResource', '//Rte_GetResource')
    hFile = hFile.replace('Rte_ReleaseResource', '//Rte_ReleaseResource')
    
    # results = re.findall('([a-zA-Z0-9_]+_RTE)',hFile)
    # for listitem in results:
        # i = 0
        # temp = listitem
        # for list2 in results:
            # if temp == list2:
                # i= i+1
        # if i > 1:
            # print('\nDuplicate RTE: ', temp)
    # Write file #===============================================================================================================================================         
    #hFileNew = open(os.path.splitext(rtefile)[0] + "_sedge_stubs.c", 'w')
    #stubfile.write(hFile)
    stubFile = open(stubfile,'w')
    stubFile.write(hFile)
    stubFile.close()
    #=============================================================================================================================================================              
    print("\n\nTool run completed ...\n\n[RESULTS]:\n\n",mesage)
    
    print("\nPlease check results in sedge_stubs.c & Rte_%s.h\n" %module)
except ValueError as outputError:
    print(outputError)  

os.system("pause")
