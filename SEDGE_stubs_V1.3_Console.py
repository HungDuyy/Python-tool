import re
from pathlib import Path
import os.path
from os import path
import os

print("\n\nModify SEDGE FC Tool - by Hung Duy\n\n     Usage:\n          This is console version:\n          - put Tool to SEDGE folder\n          - copy Rte.c & Rte_Lib.c to SEDGE folder\n          - run Tool")

# input #=================================================================================================================================================
#print("Enter Pver path: ")
#pver = input()
#while path.exists(pver) == False:
    #print("\nNot found the Pver path above ...\n\nPlease Enter right Pver path again: ")
    #pver = input()
#print("\nEnter SEDGE FC path:")
#sedge = input()
#while path.exists(sedge) == False:
    #print("\nNot found the SEDGE FC path above ...\n\nPlease Enter right SEDGE FC path again: ")
    #sedge = input()
try:
    print("\nStarting...\n")
    sedge = os.getcwd()

    results = []
    stubfile = sedge + '\\sedge_stubs.c'
    rtefile = sedge + '\\Rte.c'
    for file in os.listdir(sedge):
        if file.endswith(".h"):
            rteHfile = os.path.join(sedge, file)  
    results = re.search('([a-zA-Z0-9: \\\,\(\)\/\-._]+\\\)+Rte_([a-zA-Z0-9]+[a-zA-Z_]+[a-zA-Z])',rteHfile) #([a-zA-Z0-9]+[a-zA-Z_]+[a-zA-Z])
    module = results[2]
    if path.exists(rtefile) == True: 
        rteFile = open(rtefile).read()
    else:
        print('Not found Rte.c in working space')
    result2 = ''
    print("\nFC name to run: ",module,'\n')
    # Modify .h file #=====================================================================================================================================
    #rteHfile = sedge + '\\Rte_' + module + '.h' 
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
            print('Success for Rte_%s.h file!\n' %module)
        else:
            print('Don\'t found any point to modify in Rte_%s.h file!\n' %module)
        rteH_File = open(rteHfile,'w')
        rteH_File.write(rteHFile)
        rteH_File.close()
    else:
        print("\nFile Rte_%s.h not found!\n" %module)
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
    x = 0 #flag to check duplicate RTE
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
        print('Replace for ', result1)
        hFile = hFile.replace(results[0], result2)
        results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)(, sizeof\()(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+\))', hFile)
    # Write RTE Array #======================================================================================================================================    
    results = re.search('(Rte_[RxTMs]+_[0-9]+_)([a-zA-Z0-9_]+)(, data, sizeof\()(DA_)([a-zA-Z0-9_]+\))', hFile)
    while results != None:
        i = 1 #flag to check copy Rte_memcpy()
        result1 = results[5]
        result1 = result1.replace(')','_RTE)')
        result2 = results[2] + '_RTE' + results[3] + result1 #+ '_RTE\)'#(\2_RTE\3\5_RTE)
        print('Replace for ', result1 )
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
        print('Replace for %s_RTE' %results[3] )
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
            result2 = '//'
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
            result2 = '//'
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
        print('Replace for ', result2 )
        hFile = hFile.replace(results[0], result2)
        results = re.search('(Rte[RxMsT_]+_[0-9]+_)([a-zA-Z0-9_]+)', hFile)
    # Copy Rte_memcpy() #====================================================================================================================================== 
    if i == 1:
        rte_libfile = sedge + '\\Rte_Lib.c'
        if path.exists(rte_libfile) == True: 
            rte_libFile = open(rte_libfile).read()
            results = re.findall('(FUNC\([a-zA-Z, _]+\)\nRte_memcpy[_a-zA-Z_0-9\(, \)/*\n;:\-={}.\t\r+]+})', rte_libFile)
            for listitem in results:
                hFile = hFile + '\n' + listitem
        else:
            print('\nNot found Rte_Lib.c in Pver path')
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
    print("\nTool run completed ...")
    
    print("\nPlease check results in sedge_stubs.c & Rte_%s.h\n" %module)
except ValueError as outputError:
    print(outputError)  
    os.system("pause")
#os.system("pause")
