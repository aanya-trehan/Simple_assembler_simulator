import sys

output = []
error = {}
label_error = {}
REGISTERS = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

ISA = {
    "add": "00000",
    "sub": "00001",
    "mov": "00010",
    "ld": "00100",
    "st": "00101",
    "mul": "00110",
    "div": "00111",
    "rs": "01000",
    "ls": "01001",
    "xor": "01010",
    "or": "01011",
    "and": "01100",
    "not": "01101",
    "cmp": "01110",
    "jmp": "01111",
    "jlt": "10000",
    "jgt": "10001",
    "je": "10010",
    "hlt": "10011"}

reg_values = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0, "FLAGS": 0}

hlt_status = False
# when hlt appears status becomes True after this print error
var_status = False
# when var status is true variables can't be declared error
var = {}
labels = {}


# label name =[current_count,instruction]

############################# different types of ISA
def type_A(l):
    if len(l) != 4:
        error[current_count] = str("Line " + str(current_count) + ": Invalid Syntax of instruction")
        return

    if (l[1][0] != 'R' or l[2][0] != 'R' or l[3][0] != 'R'):
        error[current_count] = str("Line " + str(current_count) + ": Invalid Syntax - error in instruction syntax")
        return

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS or l[3] not in REGISTERS):
        error[current_count] = str("Line " + str(current_count) + ": Invalid Register - Register does not exist")
        return

    opcode = str(ISA[l[0]])
    unused = "00"
    reg1 = str(REGISTERS[l[1]])
    reg2 = str(REGISTERS[l[2]])
    reg3 = str(REGISTERS[l[3]])
    output.append(opcode + unused + reg1 + reg2 + reg3)


def type_B(l):
    if len(l) != 3:
        error[current_count] = str("Line " + str(current_count) + ": Syntax Error: Invalid Syntax of instruction")
        return
    if (l[1][0] != 'R' and l[2][0] != "$"):
        error[current_count] = str(
            "Line " + str(current_count) + ": Syntax Error: Invalid Syntax - error in instruction syntax")
        return

    elif (l[1] not in REGISTERS):
        error[current_count] = str(
            "Line " + str(current_count) + ": Syntax Error: Invalid Register - Register does not exist")
        return

    elif int(l[2][1:]) < 0 or int(l[2][1:]) > 255:
        error[current_count] = str(
            "Line " + str(current_count) + ": Syntax Error: Syntax Error: Value of Immediate must be between 0 and 255")
        return
    if ISA[l[0]] == "mov":
        opcode = "00010"
    else:
        opcode = str(ISA[l[0]])
    reg1 = str(REGISTERS[l[1]])
    im = int(l[2][1:])
    imm = '{0:08b}'.format(im)
    output.append(opcode + reg1 + imm)


def type_C(l):
    if len(l) != 3:
        error[current_count] = str("Line " + str(current_count) + ": Syntax Error: Invalid Syntax of instruction")
        return

    if (l[1][0] != 'R' and l[2][0] != 'R'):
        error[current_count] = str(
            "Line " + str(current_count) + ": Syntax Error: Invalid Syntax - error in instruction syntax")
        return

    elif (l[1] not in REGISTERS or l[2] not in REGISTERS):
        error[current_count] = str(
            "Line " + str(current_count) + ": Syntax Error: Invalid Register - Register does not exist")
        return
    if l[0] == "mov":
        opcode = "00011"
    else:
        opcode = str(ISA[l[0]])
    unused = "00000"
    reg1 = str(REGISTERS[l[1]])
    reg2 = str(REGISTERS[l[2]])
    output.append(opcode + unused + reg1 + reg2)


def type_D(l):
    if len(l) != 3:
        error[current_count] = str("Line " + str(current_count) + ": Syntax Error: Invalid Syntax of instruction")
        return
    if (l[1][0] != 'R'):
        error[current_count] = str(
            "Line " + str(current_count) + ": Syntax Error: Invalid Syntax - error in load instruction syntax")
        return

    elif (l[1] not in REGISTERS):
        error[current_count] = str(
            "Line " + str(current_count) + ": Syntax Error: Invalid Register - Register does not exist")
        return

    elif (l[2] not in var.keys()):
        error[current_count] = str(
            "Line " + str(current_count) + ": Syntax Error: Invalid Memory address: Variable has not been declared")
        return
    opcode = str(ISA[l[0]])
    reg1 = str(REGISTERS[l[1]])
    mem = '{0:08b}'.format((total_count - len(var)) + var[l[2]] - 1)
    output.append(opcode + reg1 + mem)


def type_E(l):
    if len(l) != 2:
        error[current_count] = str("Line " + str(current_count) + ": Syntax Error: Invalid Syntax of instruction")
        return
    if (l[1] not in var) and (l[1] not in labels.keys()):
        error[current_count] = str("Line " + str(
            current_count) + ":Syntax Error: Invalid Memory address: Variable or label has not been declared")
        return
    opcode = str(ISA[l[0]])
    unused = "000"
    mem = '{0:08b}'.format(int(labels[l[1]][0]) - 2)
    output.append(opcode + unused + str(mem))


#############################checking for ISA type
def check_ISA(l, current_count):
    l0 = l[0]

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


def check_label(l, current_count):
    name = l[0][:-1]
    if name in var.keys():
        label_error[current_count] = str(
            "Line " + str(current_count) + " Error:Misuse of variable name as label and vice versa")
        return
    elif name in labels.keys():
        label_error[current_count] = str("Line " + str(current_count) + " Error: Duplicate label")
        return
    else:
        labels[name] = [current_count, l[1:]]


def f1(line, current_count):
    global hlt_status
    global var_status
    l = line.split()

    if l[0] == "hlt" and hlt_status == False:
        hlt_status = True
        output.append("1001100000000000")
        return
    elif l[0] == "hlt" and hlt_status == True:
        error[current_count] = str("Line " + str(current_count) + current_count, " Error: multiple hlt instructions")
        return

    elif line == lines[-1] and l[0] == "hlt":
        hlt_status = True
        output.append("1001100000000000")
        return

    elif l[0] == "var" and var_status == True:
        error[current_count] = str("Line " + str(current_count) + " Error: Variable must be declared at the starting ")
        return

    elif l[0] == "var":
        if(len(l)==1):
            error[current_count] = str(
                "Line " + str(current_count) + " Syntax Error: nothing declared in front of var ")
            return
        var[l[1]] = current_count

        return

    elif "FLAGS" in line and l[0] != "mov":
        error[current_count] = str("Line " + str(current_count) + " Error: illegal use of flags ")
        return

    if l[0][0:-1] in labels.keys():
        if len(l) == 1:
            error[current_count] = str("Line " + str(current_count) + " Error: label is empty ")
            return

        a = ""
        for b in range(1, len(l) - 1):
            a = a + l[b] + " "
        a = a + l[-1]
        f1(a, current_count)
        return

    if l[0] in ISA.keys():
        if var_status != True:
            var_status = True
        check_ISA(l, current_count)
        return
    else:
        error[current_count] = str("Line " + str(current_count) + " Syntax Error: Not a valid instruction ")
        return


# input - assembler starts from here
total_count = 0
current_count = 0
lines = []
label_count = 1
for line in sys.stdin.readlines():
    l = line.split()
    if l[0][-1] == ":" and l[0] not in ISA:
        check_label(l, label_count)
    lines.append(line)
    total_count += 1
    label_count += 1

for line in lines:
    current_count += 1
    # print(current_count)
    if line == "":
        continue
    elif (line.split()[0] == "hlt"):
        hlt_status = True
        output.append("1001100000000000")
    elif (hlt_status == True):
        error[current_count] = str("Line " + str(current_count) + " Error: Instruction not allowed after hlt")
    else:
        f1(line, current_count)
for lerror in label_error.keys():
    error[lerror] = label_error[lerror]
if len(error) == 0:
    if "1001100000000000" in output and output[-1] != "1001100000000000":
        print("Syntax Error: Hlt instruction should be in the end")
    elif output[-1] != "1001100000000000":
        print("Syntax Error :Hlt instruction missing from end")
    elif output.count("1001100000000000") > 1:
        print("Syntax Error:Multiple hlt statements")
    else:
        for a in output:
            print(a)
elif len(error) != 0:
    for errors in sorted(error):
        print(error[errors])
        # break

# /Users/amolikabansal/Downloads/CO_M21_Assignment_submission-main_two
