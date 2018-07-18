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
    if (string[0][-1:] == ':'):
        print("into call state")
        print(string[0][0:-1])
        funcTable.append(Func())
        tindex = len(funcTable) - 1
        #funcTable[len(funcTable)-1].setFuncName(string[0][0:-1])
        funcTable[tindex].funcName = string[0][0:-1]
        funcTable[tindex].funcAddr = now_inst_addr
        funcTable[tindex].defined = 1
        for lindex in range(len(arrival_line)):
            now_inst_addr = analyze_file(arrival_line[lindex], bits, file_descriptor, now_inst_addr, index)
            viewDebugInfo(arrival_line[lindex].split()[0], bits)        

    else: 
        now_inst_addr = analyze_file(line, bits, file_descriptor, now_inst_addr, index)           
        
        ###############################
        # SYS
        #
        if(bits.type == SYS):
            if (string[0] == 'ori'):
                finish_addr = int(string[1], 16)
                if (finish_addr > now_inst_addr):
                    for now_inst_addr in range(now_inst_addr, finish_addr, 4):
                        inst = 0
                        file_descriptor.append(inst)
                        #write_to_file(inst)
                        now_inst_addr += INSTRUCTION_BITS/8
                else:
                    print("The ori address must be over now inst address. (now_inst_addr, ori_addr) = (" + now_inst_addr + "," + finish_addr + ")")
                    exit()
    
            #elif (string[0] == 'call'):
             #   call_narg = len(string)
              #  if (call_narg < 2):
               #     print("Error:In line " + str(index) + ", num of call args must >= 2, these args are "  + str(call_narg))
                #    if(call_narg == 2):
    
        viewDebugInfo(string[0], bits)        
    
        
#write file
for index in range(len(file_descriptor)):
    write_to_file(wfile, file_descriptor[index])

