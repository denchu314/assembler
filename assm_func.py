

#ATTRIBUTE
TYPE_BITS   =   2
OP_BITS     =   4
DST_BITS    =   5
SRC0_BITS   =   5
SRC1_BITS   =   5
MINOR_IMM_BITS   =   16
MAJOR_IMM_BITS   =   26

INSTRUCTION_BITS = 32
TYPE_OFFSET =   INSTRUCTION_BITS - TYPE_BITS 
OP_OFFSET   =   TYPE_OFFSET - OP_BITS
DST_OFFSET  =   OP_OFFSET   - DST_BITS
SRC0_OFFSET =   DST_OFFSET  - SRC0_BITS
SRC1_OFFSET =   SRC0_OFFSET - SRC1_BITS
MINOR_IMM_OFFSET = SRC0_OFFSET - MINOR_IMM_BITS
MAJOR_IMM_OFFSET = OP_OFFSET - MAJOR_IMM_BITS

#TYPE
CR  = 0
LR  = 1
I   = 2
J   = 3
ERR = 4
SYS = 5

def isArrivalLabel(string):
    if (string[0][-1:] == ':'):
        return True
    else:
        return False

def makeCallList(label, call_arg0, call_arg1, call_arg2, call_arg3):
    call_list0 = ['iSubi SP SP 0x10', 'sw A0 SP 0x0C', 'sw A1 SP 0x08', 'sw A2 SP 0x04', 'sw A3 SP 0x00']
    if (isHex(call_arg0)):
        call_arg0 = 'iAddi A0 ZERO ' + call_arg0
    else:
        call_arg0 = 'iAdd A0 ZERO ' + call_arg0

    if (isHex(call_arg1)):
        call_arg1 = 'iAddi A1 ZERO ' + call_arg1
    else:
        call_arg1 = 'iAdd A1 ZERO ' + call_arg1

    if (isHex(call_arg2)):
        call_arg2 = 'iAddi A2 ZERO ' + call_arg2
    else:
        call_arg2 = 'iAdd A2 ZERO ' + call_arg2

    if (isHex(call_arg3)):
        call_arg3 = 'iAddi A3 ZERO ' + call_arg3
    else:
        call_arg3 = 'iAdd A3 ZERO ' + call_arg3

    #call_arg1 = 'iAdd A1 ZERO ' + call_arg1 
    #call_arg2 = 'iAdd A2 ZERO ' + call_arg2 
    #call_arg3 = 'iAdd A3 ZERO ' + call_arg3 
    #call_func_addr = 'jal ' + str(hex(call_func_addr))
    call_label = 'jal ' + label
    call_list1 =  ['lw A0 SP 0x0C', 'lw A1 SP 0x08', 'lw A2 SP 0x04', 'lw A3 SP 0x00', 'iAddi SP SP 0x10']
    call_list = call_list0
    call_list.append(call_arg0)
    call_list.append(call_arg1)
    call_list.append(call_arg2)
    call_list.append(call_arg3)
    call_list.append(call_label)
    call_list += call_list1
    #print(call_line)
    return call_list

#call_line = ['iAddi SP SP -0x10', 'sw A0 SP 0x0C', 'sw A1 SP 0x08', 'sw A2 SP 0x04', 'sw A3 SP 0x00','iAddi A0 ZERO '] + call_arg0 + ['iAddi A1 ZERO '] + call_arg1 + ['iAddi A2 ZERO '] + call_arg2 ['iAddi A3 ZERO '] + call_arg3 + ['jal ']

arrival_list = ['iSubi SP SP 0x38', 'sw S0 SP 0x34', 'sw S1 SP 0x30', 'sw S2 SP 0x2C', 'sw S3 SP 0x28', 'sw S4 SP 0x24', 'sw S5 SP 0x20', 'sw S6 SP 0x1C', 'sw S7 SP 0x18', 'sw S8 SP 0x14', 'sw ASM SP 0x10', 'sw GP SP 0x0C', 'sw SP SP 0x08', 'sw FP SP 0x04', 'sw RA SP 0x00', 'iSubi FP SP 0x04', 'sw ZERO FP 0x00', 'iAddi SP FP 0x00']

return_list = ['iAddi SP FP 0x04', 'lw S0 SP 0x34', 'lw S1 SP 0x30', 'lw S2 SP 0x2C', 'lw S3 SP 0x28', 'lw S4 SP 0x24', 'lw S5 SP 0x20', 'lw S6 SP 0x1C', 'lw S7 SP 0x18', 'lw S8 SP 0x14', 'lw ASM SP 0x10', 'lw GP SP 0x0C', 'lw SP SP 0x08', 'lw FP SP 0x04', 'lw RA SP 0x00', 'iAddi SP SP 0x38', 'jr RA']

#def makeLiList(dst_reg, li_imm):
#    li_inst0 = 'iAddi ' + dst_reg + ' ZERO ' + li_imm

#def splitter(oplist):
#    string = oplist.split()
    

class InstructionTable:
    def __init__ (self, op, operand0, operand1, operand2):
        self.op = op #str
        self.operand0 = operand0 #str
        self.operand1 = operand1 #str
        self.operand2 = operand2 #str

class Bits:
    def __init__ (self,):
        self.type = 0
        self.op = 0
        self.dst = 0
        self.src0 = 0
        self.src1 = 0
        self.minor_imm = 0
        self.major_imm = 0


class LabelTable:
    def __init__(self, name, index):
        self.labelName = name #str
        self.labelIndex = index #int
    
    def printStatus():
        print("Label name:" + self.labelName)
        print("Label addr:{0}".format(self.labelIndex))
    
class DepartureArrivalTable:
    def __init__(self, name, pod, poa):
        self.labelName = name #str
        self.posOfDeparture = pod #int
        self.posOfArrival = poa #int
    
    def printStatus():
        print("Label name:" + self.labelName)
        print("Label posOfDeparture:{0}".format(self.posOfDeparture))
        print("Label posOfArrival:{0}".format(self.posOfArrival))

def set_type_and_op(op, InstBits, index):

    #CR
    if      op == 'iAdd':
        InstBits.type   = CR
        InstBits.op     = 0x0
    elif    op == 'iSub':
        InstBits.type   = CR
        InstBits.op     = 0x2
    elif    op == 'iMul':
        InstBits.type   = CR
        InstBits.op     = 0x4
    elif    op == 'iDev':
        InstBits.type   = CR
        InstBits.op     = 0x6
    elif    op == 'fAdd':
        InstBits.type   = CR
        InstBits.op     = 0x8
    elif    op == 'fSub':
        InstBits.type   = CR
        InstBits.op     = 0xa
    elif    op == 'fMul':
        InstBits.type   = CR
        InstBits.op     = 0xc
    elif    op == 'fDev':
        InstBits.type   = CR
        InstBits.op     = 0xe
    
    #LR
    elif    op == 'and':
        InstBits.type   = LR
        InstBits.op     = 0x0
    elif    op == 'or':
        InstBits.type   = LR
        InstBits.op     = 0x1
    elif    op == 'xor':
        InstBits.type   = LR
        InstBits.op     = 0x2
    elif    op == 'not':
        InstBits.type   = LR
        InstBits.op     = 0x3
    elif    op == 'Lsft':
        InstBits.type   = LR
        InstBits.op     = 0x4
    elif    op == 'Rsft':
        InstBits.type   = LR
        InstBits.op     = 0x5
    elif    op == 'cmp':
        InstBits.type   = LR
        InstBits.op     = 0x6
    elif    op == 'jr':
        InstBits.type   = LR
        InstBits.op     = 0x7
    
    #I
    elif    op == 'iAddi':
        InstBits.type   = I
        InstBits.op     = 0x0
    elif    op == 'iSubi':
        InstBits.type   = I
        InstBits.op     = 0x2
    elif    op == 'iMuli':
        InstBits.type   = I
        InstBits.op     = 0x4
    elif    op == 'iDevi':
        InstBits.type   = I
        InstBits.op     = 0x6
    elif    op == 'lw':
        InstBits.type   = I
        InstBits.op     = 0x8
    elif    op == 'sw':
        InstBits.type   = I
        InstBits.op     = 0x9
    elif    op == 'Lsfti':
        InstBits.type   = I
        InstBits.op     = 0xa
    elif    op == 'Rsfti':
        InstBits.type   = I
        InstBits.op     = 0xb
    elif    op == 'be':
        InstBits.type   = I
        InstBits.op     = 0xc
    elif    op == 'bne':
        InstBits.type   = I
        InstBits.op     = 0xd
    elif    op == 'cmpi':
        InstBits.type   = I
        InstBits.op     = 0xe

    #J
    elif    op == 'j':
        InstBits.type   = J
        InstBits.op     = 0x0
    elif    op == 'jal':
        InstBits.type   = J
        InstBits.op     = 0x1
    else:
        print("Error:In line " + str(index) + ", Not implemented op: " + op)
        InstBits.type   = ERR
        InstBits.op     = 0xf
        exit()

def set_dst(dst, InstBits, index):
    if dst == 'ZERO':
        InstBits.dst = 0
    elif dst == 'K0': 
        InstBits.dst = 1
    elif dst == 'K1': 
        InstBits.dst = 2
    elif dst == 'R0': 
        InstBits.dst = 3
    elif dst == 'R1': 
        InstBits.dst = 4
    elif dst == 'A0': 
        InstBits.dst = 5
    elif dst == 'A1': 
        InstBits.dst = 6
    elif dst == 'A2': 
        InstBits.dst = 7
    elif dst == 'A3': 
        InstBits.dst = 8
    elif dst == 'S0': 
        InstBits.dst = 9
    elif dst == 'S1': 
        InstBits.dst = 10
    elif dst == 'S2': 
        InstBits.dst = 11
    elif dst == 'S3': 
        InstBits.dst = 12
    elif dst == 'S4': 
        InstBits.dst = 13
    elif dst == 'S5': 
        InstBits.dst = 14
    elif dst == 'S6': 
        InstBits.dst = 15
    elif dst == 'S7': 
        InstBits.dst = 16
    elif dst == 'S8': 
        InstBits.dst = 17
    elif dst == 'T0': 
        InstBits.dst = 18
    elif dst == 'T1': 
        InstBits.dst = 19
    elif dst == 'T2': 
        InstBits.dst = 20
    elif dst == 'T3': 
        InstBits.dst = 21
    elif dst == 'T4': 
        InstBits.dst = 22
    elif dst == 'T5': 
        InstBits.dst = 23
    elif dst == 'T6': 
        InstBits.dst = 24
    elif dst == 'T7': 
        InstBits.dst = 25
    elif dst == 'T8': 
        InstBits.dst = 26
    elif dst == 'ASM':
        InstBits.dst = 27
    elif dst == 'GP': 
        InstBits.dst = 28
    elif dst == 'SP': 
        InstBits.dst = 29
    elif dst == 'FP': 
        InstBits.dst = 30
    elif dst == 'RA': 
        InstBits.dst = 31
    else:
        print("Error:In line " + str(index) + ", Not implemented dst: " + dst)
        exit()

def set_src0(src0, InstBits, index):
    if src0 == 'ZERO':
        InstBits.src0 = 0
    elif src0 == 'K0': 
        InstBits.src0 = 1
    elif src0 == 'K1': 
        InstBits.src0 = 2
    elif src0 == 'R0': 
        InstBits.src0 = 3
    elif src0 == 'R1': 
        InstBits.src0 = 4
    elif src0 == 'A0': 
        InstBits.src0 = 5
    elif src0 == 'A1': 
        InstBits.src0 = 6
    elif src0 == 'A2': 
        InstBits.src0 = 7
    elif src0 == 'A3': 
        InstBits.src0 = 8
    elif src0 == 'S0': 
        InstBits.src0 = 9
    elif src0 == 'S1': 
        InstBits.src0 = 10
    elif src0 == 'S2': 
        InstBits.src0 = 11
    elif src0 == 'S3': 
        InstBits.src0 = 12
    elif src0 == 'S4': 
        InstBits.src0 = 13
    elif src0 == 'S5': 
        InstBits.src0 = 14
    elif src0 == 'S6': 
        InstBits.src0 = 15
    elif src0 == 'S7': 
        InstBits.src0 = 16
    elif src0 == 'S8': 
        InstBits.src0 = 17
    elif src0 == 'T0': 
        InstBits.src0 = 18
    elif src0 == 'T1': 
        InstBits.src0 = 19
    elif src0 == 'T2': 
        InstBits.src0 = 20
    elif src0 == 'T3': 
        InstBits.src0 = 21
    elif src0 == 'T4': 
        InstBits.src0 = 22
    elif src0 == 'T5': 
        InstBits.src0 = 23
    elif src0 == 'T6': 
        InstBits.src0 = 24
    elif src0 == 'T7': 
        InstBits.src0 = 25
    elif src0 == 'T8': 
        InstBits.src0 = 26
    elif src0 == 'ASM': 
        InstBits.src0 = 27
    elif src0 == 'GP': 
        InstBits.src0 = 28
    elif src0 == 'SP': 
        InstBits.src0 = 29
    elif src0 == 'FP': 
        InstBits.src0 = 30
    elif src0 == 'RA': 
        InstBits.src0 = 31
    else:
        print("Error:In line " + str(index) + ", Not implemented src0: " + src0)
        exit()

def set_src1(src1, InstBits, index):
    if src1 == 'ZERO':
        InstBits.src1 = 0
    elif src1 == 'K0': 
        InstBits.src1 = 1
    elif src1 == 'K1': 
        InstBits.src1 = 2
    elif src1 == 'R0': 
        InstBits.src1 = 3
    elif src1 == 'R1': 
        InstBits.src1 = 4
    elif src1 == 'A0': 
        InstBits.src1 = 5
    elif src1 == 'A1': 
        InstBits.src1 = 6
    elif src1 == 'A2': 
        InstBits.src1 = 7
    elif src1 == 'A3': 
        InstBits.src1 = 8
    elif src1 == 'S0': 
        InstBits.src1 = 9
    elif src1 == 'S1': 
        InstBits.src1 = 10
    elif src1 == 'S2': 
        InstBits.src1 = 11
    elif src1 == 'S3': 
        InstBits.src1 = 12
    elif src1 == 'S4': 
        InstBits.src1 = 13
    elif src1 == 'S5': 
        InstBits.src1 = 14
    elif src1 == 'S6': 
        InstBits.src1 = 15
    elif src1 == 'S7': 
        InstBits.src1 = 16
    elif src1 == 'S8': 
        InstBits.src1 = 17
    elif src1 == 'T0': 
        InstBits.src1 = 18
    elif src1 == 'T1': 
        InstBits.src1 = 19
    elif src1 == 'T2': 
        InstBits.src1 = 20
    elif src1 == 'T3': 
        InstBits.src1 = 21
    elif src1 == 'T4': 
        InstBits.src1 = 22
    elif src1 == 'T5': 
        InstBits.src1 = 23
    elif src1 == 'T6': 
        InstBits.src1 = 24
    elif src1 == 'T7': 
        InstBits.src1 = 25
    elif src1 == 'T8': 
        InstBits.src1 = 26
    elif src1 == 'ASM': 
        InstBits.src1 = 27
    elif src1 == 'GP': 
        InstBits.src1 = 28
    elif src1 == 'SP': 
        InstBits.src1 = 29
    elif src1 == 'FP': 
        InstBits.src1 = 30
    elif src1 == 'RA': 
        InstBits.src1 = 31
    else:
        print("Error:In line " + str(index) + ", Not implemented src1: " + src1)
        exit()

def set_minor_imm(minor_imm, InstBits, index):
    InstBits.minor_imm    = int(minor_imm, 16)
    if (InstBits.minor_imm > 0xffff):
        InstBits.minor_imm = 0xffff
        print("Error:In line " + str(index) + ", Minor immediate value is over 16bit, 0xffff: " + InstBits.minor_imm)
        exit()

def set_major_imm(major_imm, InstBits, index):
    InstBits.major_imm    = int(major_imm, 16)
    if (InstBits.major_imm > 0x3ffffff):
        InstBits.major_imm    = 0x3ffffff
        print("Error:In line " + str(index) + ", Major immediate value is over 26bit, 0x3ffffff: " + InstBits.major_imm)
        exit()

def set_inst_binary_CR(InstBits):
    return (InstBits.type << TYPE_OFFSET) + (InstBits.op << OP_OFFSET) + (InstBits.dst << DST_OFFSET) + (InstBits.src0 << SRC0_OFFSET) + (InstBits.src1 << SRC1_OFFSET)

def set_inst_binary_LR(InstBits):
    return (InstBits.type << TYPE_OFFSET) + (InstBits.op << OP_OFFSET) + (InstBits.dst << DST_OFFSET) + (InstBits.src0 << SRC0_OFFSET) + (InstBits.src1 << SRC1_OFFSET)

def set_inst_binary_I(InstBits):
    return (InstBits.type << TYPE_OFFSET) + (InstBits.op << OP_OFFSET) + (InstBits.dst << DST_OFFSET) + (InstBits.src0 << SRC0_OFFSET) + (InstBits.minor_imm << MINOR_IMM_OFFSET)

def set_inst_binary_J(InstBits):
    return (InstBits.type << TYPE_OFFSET) + (InstBits.op << OP_OFFSET) + (InstBits.major_imm << MAJOR_IMM_OFFSET)

def write_to_file(wfile, inst):
    wfile.write(bytearray([((inst & 0xFF000000) >> 24), ((inst & 0xFF0000) >> 16), ((inst & 0xFF00) >> 8), (inst & 0xFF)]))

def ori_proc(finish_addr, PIT):
    if (finish_addr < (INSTRUCTION_BITS/8) * len(PIT)):
        print("In ori fin addr must over now addr. (now_addr, fin_addr) = (" + (INSTRUCTION_BITS/8) * len(PIT) + "," + finish_addr + ")")
        exit()
    else:
        for i in range(len(PIT), int(finish_addr,16)/(INSTRUCTION_BITS/8)):
            PIT.append(InstructionTable('iAdd', 'ZERO', 'ZERO', 'ZERO'))

def call_proc(departureLabel, arg0, arg1, arg2, arg3, PIT, DT):
    call_list = makeCallList(departureLabel, arg0, arg1, arg2, arg3)
    #print(call_list)
    for i in range(len(call_list)):
        string = call_list[i].split()
        if (string[0] == 'jal'or string[0] == 'j'):
            op = string[0]
            if (isHex(string[1])):
                PIT.append(InstructionTable(op, string[1], '0x0', '0x0'))
            else:
                PIT.append(InstructionTable(op, '0x0', '0x0', '0x0'))#pseudp label
                DT.append(LabelTable(string[1], len(PIT)-1))
        else:
            PIT.append(InstructionTable(string[0], string[1], string[2], string[3])) 

def return_proc(PIT):
    for i in range(len(return_list)):
        string = return_list[i].split()
        if (string[0] == 'jr'):
            PIT.append(InstructionTable(string[0], 'ZERO', string[1], 'ZERO')) 
        else:
            PIT.append(InstructionTable(string[0], string[1], string[2], string[3])) 

def arrival_proc(PIT):
    for i in range(len(arrival_list)):
        string = arrival_list[i].split()
        PIT.append(InstructionTable(string[0], string[1], string[2], string[3]))

#def li_proc(PIT, dst, imm):
#    li_list = makeLiList(imm)
#    for i in range(len(li_list)):
#        string = li_list[i].split()
#        PIT.append(InstructionTable(string[0], string[1], string[2], string[3])) 

def isHex(val):
    try:
        int(val, 16)
        return True
    except:
        return False

def binalize_instruction(op, operand0, operand1, operand2, InstBits, index, vflag):

    ###############################
    # set TYPE and OP
    #
    set_type_and_op(op, InstBits, index)

    ###############################
    # CR
    #
    if(InstBits.type == CR):
        set_dst(operand0, InstBits, index)
        set_src0(operand1, InstBits, index)
        set_src1(operand2, InstBits, index)
        if (vflag):
            viewDebugInfo(op, InstBits)
        return set_inst_binary_CR(InstBits)
    ###############################
    # LR
    #
    elif(InstBits.type == LR):
        set_dst(operand0, InstBits, index)
        set_src0(operand1, InstBits, index)
        set_src1(operand2, InstBits, index)
        if (vflag):
            viewDebugInfo(op, InstBits)
        return set_inst_binary_LR(InstBits)

    ###############################
    # I
    #
    elif(InstBits.type == I):
        set_dst(operand0, InstBits, index)
        set_src0(operand1, InstBits, index)
        set_minor_imm(operand2, InstBits, index)
        if (vflag):
            viewDebugInfo(op, InstBits)
        return set_inst_binary_I(InstBits)

    ###############################
    # J
    #
    elif(InstBits.type == J):
        set_major_imm(operand0, InstBits, index)
        if (vflag):
            viewDebugInfo(op, InstBits)
        return set_inst_binary_J(InstBits)

def viewDebugInfo(op, bits):
    ###############################
    # DEBUG info
    #
    if ((bits.type == CR) | (bits.type == LR)):
        print("Op:"  + op)
        print("bits.type:\t"  + str(bits.type))
        print("bits.op:\t"    + str(bits.op))
        print("bits.dst:\t"    + str(bits.dst))
        print("bits.src0:\t"   + str(bits.src0))
        print("bits.src1:\t"   + str(bits.src1))
        print("")
    elif (bits.type == I):
        print("Op:"  + op)
        print("bits.type:\t"  + str(bits.type))
        print("bits.op:\t"    + str(bits.op))
        print("bits.dst:\t"    + str(bits.dst))
        print("bits.src0:\t"   + str(bits.src0))
        print("bits.minor_imm:\t"   + str(bits.minor_imm))
        print("")
    elif (bits.type == J):
        print("Op:"  + op)
        print("bits.type:\t"  + str(bits.type))
        print("bits.op:\t"    + str(bits.op))
        print("bits.major_imm:\t"   + str(bits.major_imm))
        print("")
# set main func table
#arrivalTable[0].setFuncName('main')
#arrivalTable[0].called()
