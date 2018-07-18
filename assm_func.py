

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

def makeCallLine(call_func_addr, call_arg0, call_arg1, call_arg2, call_arg3):
    call_line0 = ['iAddi SP SP -0x10', 'sw A0 SP 0x0C', 'sw A1 SP 0x08', 'sw A2 SP 0x04', 'sw A3 SP 0x00']
    call_arg0 = 'iAdd A0 ZERO ' + call_arg0 
    call_arg1 = 'iAdd A1 ZERO ' + call_arg1 
    call_arg2 = 'iAdd A2 ZERO ' + call_arg2 
    call_arg3 = 'iAdd A3 ZERO ' + call_arg3 
    call_func_addr = 'jal ' + str(call_func_addr)
    call_line1 =  ['lw A0 SP 0x0C', 'lw A1 SP 0x08', 'lw A2 SP 0x04', 'lw A3 SP 0x00', 'iAddi SP SP 0x10']
    #call_line = ['iAddi SP SP -0x10', 'sw A0 SP 0x0C', 'sw A1 SP 0x08', 'sw A2 SP 0x04', 'sw A3 SP 0x00','iAddi A0 ZERO '] + call_arg0 + ['', 'iAddi A1 ZERO '] + call_arg1 + ['', 'iAddi A2 ZERO '] + call_arg2 ['', 'iAddi A3 ZERO '] + call_arg3 + ['','jal '] + call_func_addr + ['', 'lw A0 SP 0x0C', 'lw A1 SP 0x08', 'lw A2 SP 0x04', 'lw A3 SP 0x00', 'iAddi SP SP 0x10']
    call_line = call_line0
    call_line.append(call_arg0)
    call_line.append(call_arg1)
    call_line.append(call_arg2)
    call_line.append(call_arg3)
    call_line.append(call_func_addr)
    call_line += call_line1
    print(call_line)
    return call_line

#call_line = ['iAddi SP SP -0x10', 'sw A0 SP 0x0C', 'sw A1 SP 0x08', 'sw A2 SP 0x04', 'sw A3 SP 0x00','iAddi A0 ZERO '] + call_arg0 + ['iAddi A1 ZERO '] + call_arg1 + ['iAddi A2 ZERO '] + call_arg2 ['iAddi A3 ZERO '] + call_arg3 + ['jal ']

arrival_line = ['iAddi SP SP -0x38', 'sw S0 SP 0x34', 'sw S1 SP 0x30', 'sw S2 SP 0x2C', 'sw S3 SP 0x28', 'sw S4 SP 0x24', 'sw S5 SP 0x20', 'sw S6 SP 0x1C', 'sw S7 SP 0x18', 'sw S8 SP 0x14', 'sw ASM SP 0x10', 'sw GP SP 0x0C', 'sw SP SP 0x08', 'sw FP SP 0x04', 'sw RA SP 0x00']

return_line = ['lw S0 SP 0x34', 'lw S1 SP 0x30', 'lw S2 SP 0x2C', 'lw S3 SP 0x28', 'lw S4 SP 0x24', 'lw S5 SP 0x20', 'lw S6 SP 0x1C', 'lw S7 SP 0x18', 'lw S8 SP 0x14', 'lw ASM SP 0x10', 'lw GP SP 0x0C', 'lw SP SP 0x08', 'lw FP SP 0x04', 'lw RA SP 0x00', 'iAddi SP SP 0x38']

class Bits:
    def __init__ (self,):
        self.type = 0
        self.op = 0
        self.dst = 0
        self.src0 = 0
        self.src1 = 0
        self.minor_imm = 0
        self.major_imm = 0


class Func:
    def __init__(self, ):
        self.funcName = '' 
        self.funcAddr = 0x0
        self.defined  = 0
        self.called   = 0
    
    def setFuncName(name):
        self.funcName = name
    
    def setFuncAddr(addr):
        self.funcAddr = addr
    
    def defined():
        self.defined  = 1
    
    def called():
        self.called  = 1
    
    def printStatus():
        print("Func name:" + self.funcName)
        print("Func addr:{0}".format(self.funcAddr))
        print("Func defined:{0}".format(self.defined))
        print("Func called:{0}".format(self.called))
    
    def checkStatus():
        if (self.called==1) and (self.define==0):
            print("Error: Func" + self.funcName + "is called, but not defined.")
            exit()

def set_type_and_op(line, bits, index):
    string = line.split()
    op      = string[0]

    # SYS
    if      op == 'ori':
        bits.type   = SYS
        bits.op     = 0x0
    elif    op == '#':
        bits.type   = SYS
        bits.op     = 0x1
    elif    op == 'call':
        bits.type   = SYS
        bits.op     = 0x2
    elif    op == 'calli':
        bits.type   = SYS
        bits.op     = 0x3
    elif    op == 'return':
        bits.type   = SYS
        bits.op     = 0x4

    #CR
    elif      op == 'iAdd':
        bits.type   = CR
        bits.op     = 0x0
    elif    op == 'iSub':
        bits.type   = CR
        bits.op     = 0x2
    elif    op == 'iMul':
        bits.type   = CR
        bits.op     = 0x4
    elif    op == 'iDev':
        bits.type   = CR
        bits.op     = 0x6
    elif    op == 'fAdd':
        bits.type   = CR
        bits.op     = 0x8
    elif    op == 'fSub':
        bits.type   = CR
        bits.op     = 0xa
    elif    op == 'fMul':
        bits.type   = CR
        bits.op     = 0xc
    elif    op == 'fDev':
        bits.type   = CR
        bits.op     = 0xe
    
    #LR
    elif    op == 'and':
        bits.type   = LR
        bits.op     = 0x0
    elif    op == 'or':
        bits.type   = LR
        bits.op     = 0x1
    elif    op == 'xor':
        bits.type   = LR
        bits.op     = 0x2
    elif    op == 'not':
        bits.type   = LR
        bits.op     = 0x3
    elif    op == 'Lsft':
        bits.type   = LR
        bits.op     = 0x4
    elif    op == 'Rsft':
        bits.type   = LR
        bits.op     = 0x5
    elif    op == 'cmp':
        bits.type   = LR
        bits.op     = 0x6
    elif    op == 'jr':
        bits.type   = LR
        bits.op     = 0x7
    
    #I
    elif    op == 'iAddi':
        bits.type   = I
        bits.op     = 0x0
    elif    op == 'iSubi':
        bits.type   = I
        bits.op     = 0x2
    elif    op == 'iMuli':
        bits.type   = I
        bits.op     = 0x4
    elif    op == 'iDevi':
        bits.type   = I
        bits.op     = 0x6
    elif    op == 'lw':
        bits.type   = I
        bits.op     = 0x8
    elif    op == 'sw':
        bits.type   = I
        bits.op     = 0x9
    elif    op == 'Lsfti':
        bits.type   = I
        bits.op     = 0xa
    elif    op == 'Rsfti':
        bits.type   = I
        bits.op     = 0xb
    elif    op == 'be':
        bits.type   = I
        bits.op     = 0xc
    elif    op == 'bne':
        bits.type   = I
        bits.op     = 0xd
    elif    op == 'cmpi':
        bits.type   = I
        bits.op     = 0xe

    #J
    elif    op == 'j':
        bits.type   = J
        bits.op     = 0x0
    elif    op == 'jal':
        bits.type   = J
        bits.op     = 0x1
    else:
        print("Error:In line " + str(index) + ", Not implemented op: " + op)
        bits.type   = ERR
        bits.op     = 0xf
        exit()

def set_dst(line, bits, index):
    string = line.split()
    dst     = string[1]
    if dst == 'ZERO':
        bits.dst = 0
    elif dst == 'K0': 
        bits.dst = 1
    elif dst == 'K1': 
        bits.dst = 2
    elif dst == 'R0': 
        bits.dst = 3
    elif dst == 'R1': 
        bits.dst = 4
    elif dst == 'A0': 
        bits.dst = 5
    elif dst == 'A1': 
        bits.dst = 6
    elif dst == 'A2': 
        bits.dst = 7
    elif dst == 'A3': 
        bits.dst = 8
    elif dst == 'S0': 
        bits.dst = 9
    elif dst == 'S1': 
        bits.dst = 10
    elif dst == 'S2': 
        bits.dst = 11
    elif dst == 'S3': 
        bits.dst = 12
    elif dst == 'S4': 
        bits.dst = 13
    elif dst == 'S5': 
        bits.dst = 14
    elif dst == 'S6': 
        bits.dst = 15
    elif dst == 'S7': 
        bits.dst = 16
    elif dst == 'S8': 
        bits.dst = 17
    elif dst == 'T0': 
        bits.dst = 18
    elif dst == 'T1': 
        bits.dst = 19
    elif dst == 'T2': 
        bits.dst = 20
    elif dst == 'T3': 
        bits.dst = 21
    elif dst == 'T4': 
        bits.dst = 22
    elif dst == 'T5': 
        bits.dst = 23
    elif dst == 'T6': 
        bits.dst = 24
    elif dst == 'T7': 
        bits.dst = 25
    elif dst == 'T8': 
        bits.dst = 26
    elif dst == 'ASM':
        bits.dst = 27
    elif dst == 'GP': 
        bits.dst = 28
    elif dst == 'SP': 
        bits.dst = 29
    elif dst == 'FP': 
        bits.dst = 30
    elif dst == 'RA': 
        bits.dst = 31
    else:
        print("Error:In line " + str(index) + ", Not implemented dst: " + dst)
        exit()

def set_src0(line, bits, index):
    string = line.split()
    src0    = string[2]
    if src0 == 'ZERO':
        bits.src0 = 0
    elif src0 == 'K0': 
        bits.src0 = 1
    elif src0 == 'K1': 
        bits.src0 = 2
    elif src0 == 'R0': 
        bits.src0 = 3
    elif src0 == 'R1': 
        bits.src0 = 4
    elif src0 == 'A0': 
        bits.src0 = 5
    elif src0 == 'A1': 
        bits.src0 = 6
    elif src0 == 'A2': 
        bits.src0 = 7
    elif src0 == 'A3': 
        bits.src0 = 8
    elif src0 == 'S0': 
        bits.src0 = 9
    elif src0 == 'S1': 
        bits.src0 = 10
    elif src0 == 'S2': 
        bits.src0 = 11
    elif src0 == 'S3': 
        bits.src0 = 12
    elif src0 == 'S4': 
        bits.src0 = 13
    elif src0 == 'S5': 
        bits.src0 = 14
    elif src0 == 'S6': 
        bits.src0 = 15
    elif src0 == 'S7': 
        bits.src0 = 16
    elif src0 == 'S8': 
        bits.src0 = 17
    elif src0 == 'T0': 
        bits.src0 = 18
    elif src0 == 'T1': 
        bits.src0 = 19
    elif src0 == 'T2': 
        bits.src0 = 20
    elif src0 == 'T3': 
        bits.src0 = 21
    elif src0 == 'T4': 
        bits.src0 = 22
    elif src0 == 'T5': 
        bits.src0 = 23
    elif src0 == 'T6': 
        bits.src0 = 24
    elif src0 == 'T7': 
        bits.src0 = 25
    elif src0 == 'T8': 
        bits.src0 = 26
    elif src0 == 'ASM': 
        bits.src0 = 27
    elif src0 == 'GP': 
        bits.src0 = 28
    elif src0 == 'SP': 
        bits.src0 = 29
    elif src0 == 'FP': 
        bits.src0 = 30
    elif src0 == 'RA': 
        bits.src0 = 31
    else:
        print("Error:In line " + str(index) + ", Not implemented src0: " + src0)
        exit()

def set_src1(line, bits, index):
    string = line.split()    
    src1    = string[3]
    if src1 == 'ZERO':
        bits.src1 = 0
    elif src1 == 'K0': 
        bits.src1 = 1
    elif src1 == 'K1': 
        bits.src1 = 2
    elif src1 == 'R0': 
        bits.src1 = 3
    elif src1 == 'R1': 
        bits.src1 = 4
    elif src1 == 'A0': 
        bits.src1 = 5
    elif src1 == 'A1': 
        bits.src1 = 6
    elif src1 == 'A2': 
        bits.src1 = 7
    elif src1 == 'A3': 
        bits.src1 = 8
    elif src1 == 'S0': 
        bits.src1 = 9
    elif src1 == 'S1': 
        bits.src1 = 10
    elif src1 == 'S2': 
        bits.src1 = 11
    elif src1 == 'S3': 
        bits.src1 = 12
    elif src1 == 'S4': 
        bits.src1 = 13
    elif src1 == 'S5': 
        bits.src1 = 14
    elif src1 == 'S6': 
        bits.src1 = 15
    elif src1 == 'S7': 
        bits.src1 = 16
    elif src1 == 'S8': 
        bits.src1 = 17
    elif src1 == 'T0': 
        bits.src1 = 18
    elif src1 == 'T1': 
        bits.src1 = 19
    elif src1 == 'T2': 
        bits.src1 = 20
    elif src1 == 'T3': 
        bits.src1 = 21
    elif src1 == 'T4': 
        bits.src1 = 22
    elif src1 == 'T5': 
        bits.src1 = 23
    elif src1 == 'T6': 
        bits.src1 = 24
    elif src1 == 'T7': 
        bits.src1 = 25
    elif src1 == 'T8': 
        bits.src1 = 26
    elif src1 == 'ASM': 
        bits.src1 = 27
    elif src1 == 'GP': 
        bits.src1 = 28
    elif src1 == 'SP': 
        bits.src1 = 29
    elif src1 == 'FP': 
        bits.src1 = 30
    elif src1 == 'RA': 
        bits.src1 = 31
    else:
        print("Error:In line " + str(index) + ", Not implemented src1: " + src1)
        exit()

def set_minor_imm(line, bits, index):
    string = line.split()
    bits.minor_imm    = int(string[3], 16)
    if (bits.minor_imm > 0xffff):
        bits.minor_imm = 0xffff
        print("Error:In line " + str(index) + ", Minor immediate value is over 16bit, 0xffff: " + bits.minor_imm)
        exit()

def set_major_imm(line, bits, index):
    string = line.split()
    bits.major_imm    = int(string[1], 16)
    if (bits.major_imm > 0x3ffffff):
        bits.major_imm    = 0x3ffffff
        print("Error:In line " + str(index) + ", Major immediate value is over 26bit, 0x3ffffff: " + bits.major_imm)
        exit()

def set_inst_binary_CR(bits):
    return (bits.type << TYPE_OFFSET) + (bits.op << OP_OFFSET) + (bits.dst << DST_OFFSET) + (bits.src0 << SRC0_OFFSET) + (bits.src1 << SRC1_OFFSET)

def set_inst_binary_LR(bits):
    return (bits.type << TYPE_OFFSET) + (bits.op << OP_OFFSET) + (bits.dst << DST_OFFSET) + (bits.src0 << SRC0_OFFSET) + (bits.src1 << SRC1_OFFSET)

def set_inst_binary_I(bits):
    return (bits.type << TYPE_OFFSET) + (bits.op << OP_OFFSET) + (bits.dst << DST_OFFSET) + (bits.src0 << SRC0_OFFSET) + (bits.minor_imm << MINOR_IMM_OFFSET)

def set_inst_binary_J(bits):
    return (bits.type << TYPE_OFFSET) + (bits.op << OP_OFFSET) + (bits.major_imm << MAJOR_IMM_OFFSET)

def write_to_file(wfile, inst):
    wfile.write(bytearray([((inst & 0xFF000000) >> 24), ((inst & 0xFF0000) >> 16), ((inst & 0xFF00) >> 8), (inst & 0xFF)]))

def analyze_file(line, bits, file_descriptor, now_inst_addr, index, funcTable):

    ###############################
    # set TYPE and OP
    #
    set_type_and_op(line, bits, index)

    ###############################
    # CR
    #
    if(bits.type == CR):
        set_dst(line, bits, index)
        set_src0(line, bits, index)
        set_src1(line, bits, index)
        inst = set_inst_binary_CR(bits)
        file_descriptor.append(inst)
        #write_to_file(inst)
        now_inst_addr += INSTRUCTION_BITS/8
        return now_inst_addr
        #print(now_inst_addr)    
    ###############################
    # LR
    #
    elif(bits.type == LR):
        set_dst(line, bits, index)
        set_src0(line, bits, index)
        set_src1(line, bits, index)
        inst = set_inst_binary_LR(bits)
        file_descriptor.append(inst)
        #write_to_file(inst)
        now_inst_addr += INSTRUCTION_BITS/8
        return now_inst_addr

    ###############################
    # I
    #
    elif(bits.type == I):
        set_dst(line, bits, index)
        set_src0(line, bits, index)
        set_minor_imm(line, bits, index)
        inst = set_inst_binary_I(bits)
        file_descriptor.append(inst)
        #write_to_file(inst)
        now_inst_addr += INSTRUCTION_BITS/8
        return now_inst_addr

    ###############################
    # J
    #
    elif(bits.type == J):
        set_major_imm(line, bits, index)
        inst = set_inst_binary_J(bits)
        file_descriptor.append(inst)
        #write_to_file(inst)
        now_inst_addr += INSTRUCTION_BITS/8
        return now_inst_addr
    
    ###############################
    # SYS
    #
    elif(bits.type == SYS):
        string = line.split()
        if (string[0] == 'ori'): 
            finish_addr = int(string[1], 16)
            if (finish_addr > now_inst_addr):
                for now_inst_addr in range(now_inst_addr, finish_addr, 4):
                    inst = 0
                    file_descriptor.append(inst)
                    now_inst_addr += INSTRUCTION_BITS/8
                return now_inst_addr
            else:
                    print("The ori address must be over now inst address. (now_inst_addr, ori_addr) = (" + now_inst_addr + "," + finish_addr + ")")
                    exit()
        
        elif (string[0] == 'call'):
            call_narg = len(string)
            if(call_narg != 6):
                print("Error:In line " + str(index) + ", num of call args must == 6, these args are "  + str(call_narg))
                exit()
            else:

                #search
                for tindex in range(len(funcTable)):
                    print(funcTable[tindex].funcName)
                    print(funcTable[tindex].funcAddr)
                    if (string[1] == funcTable[tindex].funcName):
                        call_line = makeCallLine(funcTable[tindex].funcAddr, string[2], string[3], string[4], string[5])
                        for lindex in range(len(call_line)):
                            now_inst_addr = analyze_file(call_line[lindex], bits, file_descriptor, now_inst_addr, index, funcTable)
                        return now_inst_addr
               
                print('Error: func ' + string[1] + ' is not found in funcTable')
                print('     : func ' + string[1] + ' is called, but not defined.')
                exit()

    
    else:
        return now_inst_addr

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
#funcTable[0].setFuncName('main')
#funcTable[0].called()
