# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# TO DO
# 1. Flags - reset
# 2. Errors
# 3. Labels
# 4. Variables

# KEEP IN MIND THE FOLLOWING
# 1. No printing for variable but it must be declared in the starting of the program before use else error
# 2. We might need to keep track of value of registers after instruction
# 3.Assume that all the registers are initialised with 0 before the program starts to execute in the simulator.
# 4. Only variable names will be used in place of mem_addr fields of loads and stores.

import sys

REGISTERS = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

ISA = {"add": "0000", "sub": "00001", "mov": "00010", "ld": "00100", "st": "00101", "mul": "00110", "div": "00111",
       "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011", "and": "01100", "not": "01101", "cmp": "01110",
       "jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010", "hlt": "10011"}

# list to keep track of variables
var = {}

# initialising all values as 0
reg_values = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0, "FLAGS": 0}


# flag codes
# overflow set flag=1
# less than set flag=2
# greater than set flag=3
# equal set flag=4


################################### OPERATIONS OF ISA
# all type A operations- add,sub,mul,xor,or
def addISA(l):
    if len(l) != 4:
        print(current_line, ": Invalid Syntax of instruction")
        return True

    if (l[1][0] != 'R' or l[2][0] != 'R' or l[3][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in add instruction")
        return True

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS or l[3] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    reg_values[l[1]] = reg_values[l[2]] + reg_values[l[3]]

    # check for flag overflow here
    if (reg_values[l[1]] > 255):
        reg_values['FLAGS'] = 1
        reg_values[l[1]] = 0
    return False  # if no error


def subISA(l):
    if len(l) != 4:
        print(current_line, ": Invalid Syntax of instruction")
        return True

    # perform subtraction , check errors and check flags
    if (l[1][0] != 'R' or l[2][0] != 'R' or l[3][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in sub instruction")
        return True

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS or l[3] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    reg_values[l[1]] = reg_values[l[2]] - reg_values[l[3]]

    if (reg_values[l[3]] > reg_values[l[2]]):
        reg_values['FLAGS'] = 1
        reg_values[l[1]] = 0

    return False  # if no error


def mulISA(l):
    if len(l) != 4:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    # perform multiplication , check errors and check flags
    if (l[1][0] != 'R' or l[2][0] != 'R' or l[3][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in mul instruction")
        return True

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS or l[3] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return

    reg_values[l[1]] = reg_values[l[2]] * reg_values[l[3]]

    if (reg_values[l[1]] > 255):
        reg_values['FLAGS'] = 1
        reg_values[l[1]] = 0

    return False  # if no error


def divISA(l):
    if len(l) != 4:
        print(current_line, ": Invalid Syntax of instruction")
        return True

    if (l[1][0] != 'R' or l[2][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in div instruction")
        return True

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return

    q = reg_values[l[1]] // reg_values[l[2]]
    r = reg_values[l[1]] % reg_values[l[2]]

    reg_values[l[1]] = q
    reg_values[l[2]] = r

    return False  # if no error


def xorISA(l):
    if len(l) != 4:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    if (l[1][0] != 'R' or l[2][0] != 'R' or l[3][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in xor instruction")
        return True

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS or l[3] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    reg_values[l[1]] = reg_values[l[2]] ^ reg_values[l[3]]

    # perform xor , check errors and check flags

    return False  # if no error


def orISA(l):
    if len(l) != 4:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    if (l[1][0] != 'R' or l[2][0] != 'R' or l[3][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in or instruction")
        return True

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS or l[3] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    reg_values[l[1]] = reg_values[l[2]] | reg_values[l[3]]

    # perform xor , check errors and check flags

    return False  # if no error


def andISA(l):
    if len(l) != 4:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    if (l[1][0] != 'R' or l[2][0] != 'R' or l[3][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in and instruction")
        return True

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS or l[3] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    reg_values[l[1]] = reg_values[l[2]] & reg_values[l[3]]

    return False


# type B - mov imm, rs,ls,
def mov_imm_ISA(l):
    if len(l) != 3:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    if (l[1][0] != 'R' and l[2][0] != "$"):
        print(current_line, ": Invalid Syntax - error in mov instruction")
        return True

    elif (l[1] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    elif (l[2][1:] < 0 or l[2][1:] > 255):
        print(current_line, ": Error: Value of Immediate must be between 0 and 255")
        return True

        # flags

    reg_values[l[1]] = int(l[2][1:])

    return False  # if no error


def rsISA(l):
    if len(l) != 3:
        print(current_line, ": Invalid Syntax of instruction")
        return True

    if (l[1][0] != 'R' and l[2][0] != "$"):
        print(current_line, ": Invalid Syntax - error in rs instruction")
        return True

    elif (l[1] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    elif (l[2][1:] < 0 or l[2][1:] > 255):
        print(current_line, ": Error: Value of Immediate must be between 0 and 255")
        return True

    reg_values[l[1]] = reg_values[l[1]] >> 1

    return False  # if no error


def lsISA(l):
    if len(l) != 3:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    if (l[1][0] != 'R' and l[2][0] != "$"):
        print(current_line, ": Invalid Syntax - error in ls instruction")
        return True

    elif (l[1] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    elif (l[2][1:] < 0 or l[2][1:] > 255):
        print(current_line, ": Error: Value of Immediate must be between 0 and 255")
        return True

    reg_values[l[1]] = reg_values[l[1]] << 1
    return False  # if no error


# type C- not,cmp
def notISA(l):
    if len(l) != 3:
        print(current_line, ": Invalid Syntax of instruction")
        return True

    if (l[1][0] != 'R' and l[2][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in invert instruction syntax")
        return True

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    reg_values[l[1]] = ~reg_values[l[1]]

    return False  # if no error


def cmpISA(l):
    if len(l) != 3:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    if (l[1][0] != 'R' and l[2][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in compare instruction syntax")
        return True

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    if (reg_values[l[1]] < reg_values[l[2]]):
        reg_values['FLAGS'] = 2
    elif (reg_values[l[1]] > reg_values[l[2]]):
        reg_values['FLAGS'] = 3
    else:
        reg_values['FLAGS'] = 4

    # overflow set flag=1
    # less than set flag=2
    # greater than set flag=3
    # equal set flag=4

    return False  # if no error


# type D- ld,st
def ldISA(l):
    if len(l) != 3:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    if (l[1][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in load instruction syntax")
        return True

    elif (l[1] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    elif (l[2] not in var.keys()):
        print(current_line, ":Invalid Memory address: Variable has not been declared")
        return True

    reg_values[l[1]] = var[l[2]]
    return False  # if no error


def stISA(l):
    if len(l) != 3:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    if (l[1][0] != 'R'):
        print(current_line, ": Invalid Syntax - error in load instruction syntax")
        return True

    elif (l[1] not in REGISTERS):
        print(current_line, ": Invalid Register - Register does not exist")
        return True

    elif (l[2] not in var.keys()):
        print(current_line, ":Invalid Memory address: Variable has not been declared")
        return True

    var[l[2]] = reg_values[l[1]]

    # perform or , check errors and check flags
    return False  # if no error


# type E-["jmp","jlt","jgt","je"]
def jmpISA(l):
    if len(l) != 2:
        print(current_line, ": Invalid Syntax of instruction")
        return True

    # perform operation , check errors and check flags
    return False  # if no error


def jltISA(l):
    if len(l) != 2:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    # perform operation , check errors and check flags
    return False  # if no error


def jgtISA(l):
    if len(l) != 2:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    # perform operation , check errors and check flags
    return False  # if no error


def jeISA(l):
    if len(l) != 2:
        print(current_line, ": Invalid Syntax of instruction")
        return True
    # perform operation , check errors and check flags
    return False  # if no error


def hlt():
    return False


############################# different types of ISA
def type_A(l):
    if l[0] == 'add':
        error = addISA(l)
    elif l[0] == "sub":
        error = subISA(l)
    elif l[0] == "mul":
        error = mulISA(l)
    elif l[0] == "xor":
        error = xorISA(l)
    elif l[0] == "or":
        error = orISA(l)
    elif l[0] == "and":
        error = andISA(l)
    # else:
    # error
    # return

    # mul xor or
    if error == True:
        return  # we print error type we won't print the machine code
    opcode = str(ISA[l[0]])
    unused = "00"
    reg1 = str(REGISTERS[l[1]])
    reg2 = str(REGISTERS[l[2]])
    reg3 = str(REGISTERS[l[3]])
    print(opcode + unused + reg1 + reg2 + reg3)


def type_B(l):
    if ISA[l[0]] == "mov":
        opcode = "00010"
    else:
        opcode = str(ISA[l[0]])
    reg1 = str(REGISTERS[l[1]])
    im = int(l[2][1:])
    imm = '{0:08b}'.format(im)
    print(opcode + reg1 + imm)


def type_C(l):
    if ISA[l[0]] == "mov":
        opcode = "00011"
    else:
        opcode = str(ISA[l[0]])
    unused = "00000"
    reg1 = str(REGISTERS[l[1]])
    reg2 = str(REGISTERS[l[2]])
    print(opcode + unused + reg1 + reg2)


def type_D(l):
    opcode = str(ISA[l[0]])
    reg1 = str(REGISTERS[l[1]])
    mem = '{0:08b}'.format(current_line)
    print(opcode + reg1 + mem)


def type_E(l):
    opcode = str(ISA[l[0]])
    unused = "000"
    # memory address????
    mem = "00000000"  # CHANGE
    print(opcode + unused + mem)


#############################checking for ISA type
def checkISA(l):
    l0 = l[0]

    # MAYBE MAKE A DIFF FUNCTION FOR THIS - INSTRUCTION
    if l0 in ["add", "sub", "mul", "xor", "or", "and"]:
        type_A(l)

    # ignoring mov
    elif l0 in ["rs", "ls"]:
        type_B(l)

    # ignoring mov
    elif l0 in ["not", "cmp"]:
        type_C(l)

    elif l0 in ["ld", "st"]:
        type_D(l)

    elif l0 in ["jmp", "jlt", "jgt", "je"]:
        type_E(l)

    elif l0 == "mov":
        if l[2] not in REGISTERS.keys():
            type_B(l)
        else:
            type_C(l)

    else:
        return
        # error


###########################CHECKING IF LABEL
# def checkLabel(l)  # to do-----------------
#     # first check for label errors
#     l0 = l[0]
#     if "label" and ":" in l0:
#         return  # have to complete


############################## CHECKING IF VAR
def checkVar(l):
    l0 = l[0]
    if l0 == "var":
        return True


###################### step 2- read type of line : ISA , var or label
def CheckType(line):
    if line == "":
        return

    l = line.split()
    l0 = l[0]

    if l0 in ISA.keys():
        checkISA(l)

    elif "label" and ":" in l0:
        checkLabel(l)

    # elif "var"==l0:
    # checkVar(l)

    else:
        print(current_line, "Error: Unidentifiable syntax")

    ############### hlt error


def hlt_error(line):
    return  # make this function


########################### step 1- read input
if __name__ == '__main__':
    check_hlt = False
    lines = []
    for line in sys.stdin.readlines():
        lines.append(line[0:-1])

    totalines = 0
    varline = 0
    hlt_lines = []
    label_mem = {}
    for line in lines:
        l = line.split()
        totalines += 1
        if l == '':
            continue
        elif l[0] == 'var':
            varline += 1
        if "hlt" in l:
            hlt_lines.append(totalines)
        elif "label" in l[0] and l[0][-1] == ':':
            lname = l[0][0:-1]
            label_mem[lname] = 0  # IDK PLEASE HELP-----------to do

    current_line = 0
    var_allowed = True
    var_list = []
    for line in lines:
        current_line += 1
        if checkVar(line.split()) == True:
            if var_allowed == True:
                var_list.append(line.split()[1])
                continue
            elif var_allowed == False:
                print(current_line, "Error: Variables must be declared at the starting")
                continue
        elif hlt_error(line) == True:
            continue
        else:
            CheckType(line)

    '''if lines[-1]!="hlt":
      print("Error: Last line should be halt")
  
    elif lines.count("hlt")>1:
      print("Error: multiple halts not possible")
  
    elif lines.count("hlt")==0:
      print("Error: hlt not present in program")
  
    elif lines.count("hlt")==1 and lines[-1]!="hlt":
      print("Error: Only last line should be halt")'''

    # for line in lines:
    #   if line=="hlt" and check_hlt=False:
    #     check_hlt=True
    #      print(str(ISA[l[0]])+"00000000000")
    #   elif line=="hlt" and check_hlt=True:

'''
while True:
  line=input()
  l=line.split()
  if line=="hlt":
    print(str(ISA[l[0]])+"00000000000")
    break
  elif l[0]=='var':
    var[l[0]]=line_number
  else:
    CheckType(line)

  line_number+=1

'''






