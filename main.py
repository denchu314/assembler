import sys
from assm_func import *
#import subprocess

args = sys.argv

PREPROCESSED_OUTPUT_FILENAME = "a.prep"
COMPLETED_OUTPUT_FILENAME = "a.comp"
OUTPUT_FILENAME = "a.bin"


bits = Bits()

vflag = False

if (len(args) < 2):
    print("usage: " + args[0] + " [assembly_file_path] [-v]")
    exit()
else:
    print("input file: " + args[1])

if (len(args) == 3):
    if(args[2] == '-v'):
        vflag = True
    else:
        print('Error:args[2]:' + args[2] + ' is not defined.')
        exit()

rfile = open(args[1], 'r')
wfile_m = open(PREPROCESSED_OUTPUT_FILENAME, 'w')
wfile_m2 = open(COMPLETED_OUTPUT_FILENAME, 'w')
wfile = open(OUTPUT_FILENAME, 'wb')

line = rfile.readlines()


# declear arrivalTable
#AT = [LabelTable()]
AT = []

# declear departureTable
#DT = [LabelTable()]
DT = []

# declear arrivalTable
#DAT = [DepartureArrivalTable()]
DAT = []

# declear preprocessInstructinTable(PIT)
#PIT = [InstructionTable()]
PIT = []

# declear completeInstructinTable(PIT)
#CIT = [InstructionTable()]
CIT = []

# instruction bits
InstBits = Bits()

###################
# PRIPROCESS
###################
for index, line in enumerate(line):
    if (vflag):
        print('In line:' + str(index+1)) 
    #
    # check arrival Label
    #
    string = line.split()
    op = string[0]
    
    if (isArrivalLabel(string)):
        arrivalLabel = string[0][0:-1]
        AT.append(LabelTable(arrivalLabel, len(PIT) ))
    
    #
    # chack SYS instruction
    #
    elif (op == 'ori' or op =='call' or op == 'return' or op == 'arrival'):
        if (op == 'ori'):
            ori_proc(string[1], PIT) 
        elif (op == 'call'):
            call_proc(string[1], string[2], string[3], string[4], string[5], PIT, DT)
        elif (op == 'return'):
            return_proc(PIT)
        elif (op == 'arrival'):
            arrival_proc(PIT)

    #
    # chack j or jal instruction
    #
    elif (op == 'j' or op == 'jal'):
        if (isHex(string[1])):
            PIT.append(InstructionTable(op, string[1], '0x0', '0x0'))
        else:
            PIT.append(InstructionTable(op, '0x0', '0x0', '0x0'))#pseudp label
            DT.append(LabelTable(string[1], len(PIT)-1))

    #
    # chack not or jr instruction
    #
    elif (op == 'not'):
            PIT.append(InstructionTable(op, string[1], string[2], 'ZERO'))
    elif (op == 'jr'):
            PIT.append(InstructionTable(op, 'ZERO', string[1], 'ZERO'))

    #
    # set instruction on PIT if type == CR, LR, I
    #
    else:
       PIT.append(InstructionTable(op, string[1], string[2], string[3])) 

if (vflag):
    for i in range(len(PIT)):
        wfile_m.write(PIT[i].op + ' ' + PIT[i].operand0 + ' ' + PIT[i].operand1 + ' ' + PIT[i].operand2 + '\n')

#####################
# REPLACE PHASE
#####################

#
# make DepartureArrivalTable
#
for i in range(len(DT)):
    detect = False
    for j in range(len(AT)):
        if (DT[i].labelName == AT[j].labelName):
            detect = True
            DAT.append(DepartureArrivalTable(DT[i].labelName, DT[i].labelIndex, AT[j].labelIndex))
            
    if (detect == False):
        print('Error:There is no Arrival Label in file, ' + DT[i].labelName)
        exit()

#
# make Complete Instruction Table
#
CIT = PIT

for i in range(len(DAT)):
    CIT[DAT[i].posOfDeparture].operand0 = hex((INSTRUCTION_BITS/8) * DAT[i].posOfArrival)

if (vflag):
    for i in range(len(CIT)):
            wfile_m2.write(CIT[i].op + ' ' + CIT[i].operand0 + ' ' + CIT[i].operand1 + ' ' + CIT[i].operand2 + '\n')

#
# binalize and write file
#
for i in range(len(CIT)):
    write_to_file(wfile, binalize_instruction(CIT[i].op, CIT[i].operand0, CIT[i].operand1, CIT[i].operand2, InstBits, i, vflag))

