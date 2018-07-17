import sys

args = sys.argv

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
ERR = 0
SYS = 5

if len(args) != 2:
    print("usage: " + args[0] + " [assembly_file_path] ")
    exit()
else:
    print("input file: " + args[1])

rfile = open(args[1], 'r')
wfile = open("a.bin", 'wb')

line = rfile.readlines()
now_inst_addr = 0
for index, line in enumerate(line):
    string = line.split()
    op      = string[0]

    ######################   
    # System operation
    if      op == 'ori':
        finish_addr = int(string[1], 16)
        if (finish_addr > now_inst_addr):
            for now_inst_addr in range(now_inst_addr, finish_addr-4, 4):
                type_bits = SYS
                inst = 0
                now_inst_addr += INSTRUCTION_BITS/8
                wfile.write(bytearray([((inst & 0xFF000000) >> 24), ((inst & 0xFF0000) >> 16), ((inst & 0xFF00) >> 8), (inst & 0xFF)]))
        else:
                print("The ori address must be over now inst address. (now_inst_addr, ori_addr) = (" + now_inst_addr + "," + finish_addr + ")")
                exit()
    ######################   
    # TYPE and OP bits set

    #Calc Register
    elif      op == 'iAdd':
        type_bits   = CR
        op_bits     = 0x0
    elif    op == 'iSub':
        type_bits   = CR
        op_bits     = 0x2
    elif    op == 'iMul':
        type_bits   = CR
        op_bits     = 0x4
    elif    op == 'iDev':
        type_bits   = CR
        op_bits     = 0x6
    elif    op == 'fAdd':
        type_bits   = CR
        op_bits     = 0x8
    elif    op == 'fSub':
        type_bits   = CR
        op_bits     = 0xa
    elif    op == 'fMul':
        type_bits   = CR
        op_bits     = 0xc
    elif    op == 'fDev':
        type_bits   = CR
        op_bits     = 0xe
    
    #Logic Register
    elif    op == 'and':
        type_bits   = LR
        op_bits     = 0x0
    elif    op == 'or':
        type_bits   = LR
        op_bits     = 0x1
    elif    op == 'xor':
        type_bits   = LR
        op_bits     = 0x2
    elif    op == 'not':
        type_bits   = LR
        op_bits     = 0x3
    elif    op == 'Lsft':
        type_bits   = LR
        op_bits     = 0x4
    elif    op == 'Rsft':
        type_bits   = LR
        op_bits     = 0x5
    elif    op == 'cmp':
        type_bits   = LR
        op_bits     = 0x6
    elif    op == 'jr':
        type_bits   = LR
        op_bits     = 0x7
    
    #Immediate
    elif    op == 'iAddi':
        type_bits   = I
        op_bits     = 0x0
    elif    op == 'iSubi':
        type_bits   = I
        op_bits     = 0x2
    elif    op == 'iMuli':
        type_bits   = I
        op_bits     = 0x4
    elif    op == 'iDevi':
        type_bits   = I
        op_bits     = 0x6
    elif    op == 'lw':
        type_bits   = I
        op_bits     = 0x8
    elif    op == 'st':
        type_bits   = I
        op_bits     = 0x9
    elif    op == 'Lsfti':
        type_bits   = I
        op_bits     = 0xa
    elif    op == 'Rsfti':
        type_bits   = I
        op_bits     = 0xb
    elif    op == 'be':
        type_bits   = I
        op_bits     = 0xc
    elif    op == 'bne':
        type_bits   = I
        op_bits     = 0xd
    elif    op == 'cmpi':
        type_bits   = I
        op_bits     = 0xe

    #Jump
    elif    op == 'j':
        type_bits   = J
        op_bits     = 0x0
    elif    op == 'jal':
        type_bits   = J
        op_bits     = 0x1
    else:
        print("In line " + str(index) + ", Not implemented op: " + op)
        type_bits   = ERR
        op_bits     = 0xf


    ###############################
    # DST set
    #
    if ((type_bits == CR)|(type_bits == LR)|(type_bits == I)):
        dst     = string[1]
        if dst == 'ZERO':
            dst_bits = 0
        elif dst == 'K0': 
            dst_bits = 1
        elif dst == 'K1': 
            dst_bits = 2
        elif dst == 'R0': 
            dst_bits = 3
        elif dst == 'R1': 
            dst_bits = 4
        elif dst == 'A0': 
            dst_bits = 5
        elif dst == 'A1': 
            dst_bits = 6
        elif dst == 'A2': 
            dst_bits = 7
        elif dst == 'A3': 
            dst_bits = 8
        elif dst == 'S0': 
            dst_bits = 9
        elif dst == 'S1': 
            dst_bits = 10
        elif dst == 'S2': 
            dst_bits = 11
        elif dst == 'S3': 
            dst_bits = 12
        elif dst == 'S4': 
            dst_bits = 13
        elif dst == 'S5': 
            dst_bits = 14
        elif dst == 'S6': 
            dst_bits = 15
        elif dst == 'S7': 
            dst_bits = 16
        elif dst == 'S8': 
            dst_bits = 17
        elif dst == 'T0': 
            dst_bits = 18
        elif dst == 'T1': 
            dst_bits = 19
        elif dst == 'T2': 
            dst_bits = 20
        elif dst == 'T3': 
            dst_bits = 21
        elif dst == 'T4': 
            dst_bits = 22
        elif dst == 'T5': 
            dst_bits = 23
        elif dst == 'T6': 
            dst_bits = 24
        elif dst == 'T7': 
            dst_bits = 25
        elif dst == 'T8': 
            dst_bits = 26
        elif dst == 'ASM':
            dst_bits = 27
        elif dst == 'GP': 
            dst_bits = 28
        elif dst == 'SP': 
            dst_bits = 29
        elif dst == 'FP': 
            dst_bits = 30
        elif dst == 'RA': 
            dst_bits = 31
        else:
            print("In line " + str(index) + ", Not implemented dst: " + dst)
            dst_bits = 31


    ###############################
    # SRC0 set
    #
    if ((type_bits == CR)|(type_bits == LR)|(type_bits == I)):
        src0    = string[2]
        if src0 == 'ZERO':
            src0_bits = 0
        elif src0 == 'K0': 
            src0_bits = 1
        elif src0 == 'K1': 
            src0_bits = 2
        elif src0 == 'R0': 
            src0_bits = 3
        elif src0 == 'R1': 
            src0_bits = 4
        elif src0 == 'A0': 
            src0_bits = 5
        elif src0 == 'A1': 
            src0_bits = 6
        elif src0 == 'A2': 
            src0_bits = 7
        elif src0 == 'A3': 
            src0_bits = 8
        elif src0 == 'S0': 
            src0_bits = 9
        elif src0 == 'S1': 
            src0_bits = 10
        elif src0 == 'S2': 
            src0_bits = 11
        elif src0 == 'S3': 
            src0_bits = 12
        elif src0 == 'S4': 
            src0_bits = 13
        elif src0 == 'S5': 
            src0_bits = 14
        elif src0 == 'S6': 
            src0_bits = 15
        elif src0 == 'S7': 
            src0_bits = 16
        elif src0 == 'S8': 
            src0_bits = 17
        elif src0 == 'T0': 
            src0_bits = 18
        elif src0 == 'T1': 
            src0_bits = 19
        elif src0 == 'T2': 
            src0_bits = 20
        elif src0 == 'T3': 
            src0_bits = 21
        elif src0 == 'T4': 
            src0_bits = 22
        elif src0 == 'T5': 
            src0_bits = 23
        elif src0 == 'T6': 
            src0_bits = 24
        elif src0 == 'T7': 
            src0_bits = 25
        elif src0 == 'T8': 
            src0_bits = 26
        elif src0 == 'ASM': 
            src0_bits = 27
        elif src0 == 'GP': 
            src0_bits = 28
        elif src0 == 'SP': 
            src0_bits = 29
        elif src0 == 'FP': 
            src0_bits = 30
        elif src0 == 'RA': 
            src0_bits = 31
        else:
            print("In line " + str(index) + ", Not implemented src0: " + src0)
            src0_bits = 31

    ###############################
    # SRC1 set
    #
    if ((type_bits == CR) | (type_bits == LR)):
        src1    = string[3]
        if src1 == 'ZERO':
            src1_bits = 0
        elif src1 == 'K0': 
            src1_bits = 1
        elif src1 == 'K1': 
            src1_bits = 2
        elif src1 == 'R0': 
            src1_bits = 3
        elif src1 == 'R1': 
            src1_bits = 4
        elif src1 == 'A0': 
            src1_bits = 5
        elif src1 == 'A1': 
            src1_bits = 6
        elif src1 == 'A2': 
            src1_bits = 7
        elif src1 == 'A3': 
            src1_bits = 8
        elif src1 == 'S0': 
            src1_bits = 9
        elif src1 == 'S1': 
            src1_bits = 10
        elif src1 == 'S2': 
            src1_bits = 11
        elif src1 == 'S3': 
            src1_bits = 12
        elif src1 == 'S4': 
            src1_bits = 13
        elif src1 == 'S5': 
            src1_bits = 14
        elif src1 == 'S6': 
            src1_bits = 15
        elif src1 == 'S7': 
            src1_bits = 16
        elif src1 == 'S8': 
            src1_bits = 17
        elif src1 == 'T0': 
            src1_bits = 18
        elif src1 == 'T1': 
            src1_bits = 19
        elif src1 == 'T2': 
            src1_bits = 20
        elif src1 == 'T3': 
            src1_bits = 21
        elif src1 == 'T4': 
            src1_bits = 22
        elif src1 == 'T5': 
            src1_bits = 23
        elif src1 == 'T6': 
            src1_bits = 24
        elif src1 == 'T7': 
            src1_bits = 25
        elif src1 == 'T8': 
            src1_bits = 26
        elif src1 == 'ASM': 
            src1_bits = 27
        elif src1 == 'GP': 
            src1_bits = 28
        elif src1 == 'SP': 
            src1_bits = 29
        elif src1 == 'FP': 
            src1_bits = 30
        elif src1 == 'RA': 
            src1_bits = 31
        else:
            print("In line " + str(index) + ", Not implemented src1: " + src1)
            src1_bits = 31

    ###############################
    # MINOR_IMMEDIATE set
    #
    if (type_bits == I):
        minor_imm_bits    = int(string[3], 16)
        if (minor_imm_bits > 0xffff):
            minor_imm_bits = 0xffff
            print("In line " + str(index) + ", Minor immediate value is over 16bit, 0xffff: " + minor_imm_bits)

    ###############################
    # SRC1 set
    #
    if (type_bits == J):
        major_imm_bits    = int(string[1], 16)
        if (major_imm_bits > 0x3ffffff):
            major_imm_bits    = 0x3ffffff
            print("In line " + str(index) + ", Major immediate value is over 26bit, 0x3ffffff: " + major_imm_bits)
         
    ###############################
    # set instruction binary
    #
    if ((type_bits == CR)|(type_bits == LR)):
        inst = (type_bits << TYPE_OFFSET) + (op_bits << OP_OFFSET) + (dst_bits << DST_OFFSET) + (src0_bits << SRC0_OFFSET) + (src1_bits << SRC1_OFFSET)
    elif (type_bits == I):
        inst = (type_bits << TYPE_OFFSET) + (op_bits << OP_OFFSET) + (dst_bits << DST_OFFSET) + (src0_bits << SRC0_OFFSET) + (minor_imm_bits << MINOR_IMM_OFFSET)
    elif (type_bits == J):
        inst = (type_bits << TYPE_OFFSET) + (op_bits << OP_OFFSET) + (major_imm_bits << MAJOR_IMM_OFFSET)

    now_inst_addr += INSTRUCTION_BITS/8

    ###############################
    # DEBUG info
    #
    if ((type_bits == CR) | (type_bits == LR)):
        print("Op:"  + op)
        print("type_bits:\t"  + str(type_bits))
        print("op_bits:\t"    + str(op_bits))
        print("dst_bits:\t"    + str(dst_bits))
        print("src0_bits:\t"   + str(src0_bits))
        print("src1_bits:\t"   + str(src1_bits))
        print("")
    elif (type_bits == I):
        print("Op:"  + op)
        print("type_bits:\t"  + str(type_bits))
        print("op_bits:\t"    + str(op_bits))
        print("dst_bits:\t"    + str(dst_bits))
        print("src0_bits:\t"   + str(src0_bits))
        print("minor_imm_bits:\t"   + str(minor_imm_bits))
        print("")
    elif (type_bits == J):
        print("Op:"  + op)
        print("type_bits:\t"  + str(type_bits))
        print("op_bits:\t"    + str(op_bits))
        print("major_imm_bits:\t"   + str(major_imm_bits))
        print("")

    ###############################
    # write instruction binary
    #
    wfile.write(bytearray([((inst & 0xFF000000) >> 24), ((inst & 0xFF0000) >> 16), ((inst & 0xFF00) >> 8), (inst & 0xFF)]))

