import sys
from assm_func import *
#import subprocess

args = sys.argv

OUTPUT_FILENAME = "a.bin"


bits = Bits()

if len(args) != 2:
    print("usage: " + args[0] + " [assembly_file_path] ")
    exit()
else:
    print("input file: " + args[1])

rfile = open(args[1], 'r')
wfile = open(OUTPUT_FILENAME, 'wb')

line = rfile.readlines()


# declear functable
funcTable = []
funcTable.append(Func())
funcTable[0].funcName = 'main'
funcTable[0].defined = 1
# buffer to write file
# 16 byte in head of binary file is reserved to use jump for main
file_descriptor = [0x00000000, 0x00000000, 0x00000000, 0x00000000]

# start address
now_inst_addr = INSTRUCTION_BITS * len(file_descriptor)/8


for index, line in enumerate(line):
    ###############################
    # check Func define
    #
    string = line.split()
    if (string[0][:] == 'main:'):
        funcTable[0].funcAddr = now_inst_addr
        funcTable[0].called = 1
    elif (string[0][-1:] == ':'):
        print("into call state")
        print(string[0][0:-1])
        funcTable.append(Func())
        tindex = len(funcTable) - 1
        #funcTable[len(funcTable)-1].setFuncName(string[0][0:-1])
        funcTable[tindex].funcName = string[0][0:-1]
        funcTable[tindex].funcAddr = now_inst_addr
        funcTable[tindex].defined = 1
        for i in range(len(funcTable)):
            print(funcTable[i].funcName)
            print(funcTable[i].funcAddr)
        for lindex in range(len(arrival_line)):
            now_inst_addr = analyze_file(arrival_line[lindex], bits, file_descriptor, now_inst_addr, index, funcTable)
            viewDebugInfo(arrival_line[lindex].split()[0], bits)        

    else: 
        now_inst_addr = analyze_file(line, bits, file_descriptor, now_inst_addr, index, funcTable)           
        
        ###############################
        # SYS
        #
    
            #elif (string[0] == 'call'):
             #   call_narg = len(string)
              #  if (call_narg < 2):
               #     print("Error:In line " + str(index) + ", num of call args must >= 2, these args are "  + str(call_narg))
                #    if(call_narg == 2):
    
        viewDebugInfo(string[0], bits)        
    
        
#write file
file_descriptor[0] = funcTable[0].funcAddr + 0xC0000000
for index in range(len(file_descriptor)):
    write_to_file(wfile, file_descriptor[index])

