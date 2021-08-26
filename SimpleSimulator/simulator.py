import sys
import matplotlib.pyplot as plt

program_counter = 0
programcounter = []
memory = []
lines = []

for i in range(0, 256):
    memory.append("0" * 16)

flags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

REGISTERS = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

registers1 = {"000": "0000000000000000",
              "001": "0000000000000000",
              "010": "0000000000000000",
              "011": "0000000000000000",
              "100": "0000000000000000",
              "101": "0000000000000000",
              "110": "0000000000000000",
              "111": "0000000000000000"}


def makebin(cookie):
    onya = '{0:08b}'.format(cookie)
    while len(onya) < 16:
        onya = '0' + onya
    return onya


# dsa reference xD

def reset_flags():
    global flags
    flags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def print_call():
    print('{0:08b}'.format(program_counter), end=" ")
    print(registers1["000"], end=" ")
    print(registers1["001"], end=" ")
    print(registers1["010"], end=" ")
    print(registers1["011"], end=" ")
    print(registers1["100"], end=" ")
    print(registers1["101"], end=" ")
    print(registers1["110"], end=" ")
    for i in flags:
        print(i, end="")
    print()


def add(reg1, reg2, reg3):
    global program_counter
    r1 = registers1[reg1]
    r2 = registers1[reg2]
    r3 = registers1[reg3]
    reset_flags()
    registers1[reg1] = makebin(int(r2, 2) + int(r3, 2))
    print_call()
    program_counter += 1


def sub(reg1, reg2, reg3):
    global program_counter
    r2 = registers1[reg2]
    r3 = registers1[reg3]
    if (int(r3, 2) > int(r2, 2)):
        registers1[reg1] = makebin(0)
        flags[12] = 1
    else:
        registers1[reg1] = makebin(int(r2, 2) - int(r3, 2))
    print_call()
    program_counter += 1


def mov_Imm(reg, Imm):
    global program_counter
    reset_flags()
    registers1[reg] = makebin(int(Imm, 2))
    print_call()
    program_counter += 1


def mov_Reg(reg1, reg2):
    global program_counter
    if (reg2 == "111"):
        f = ""
        for i in flags:
            f = f + str(i)
            registers1[reg1] = f
    else:
        r2 = registers1[reg2]
        registers1[reg1] = r2
    reset_flags()
    print_call()
    program_counter += 1


def ld(reg1, memory_address):
    reset_flags()
    registers1[reg1] = memory[int(memory_address, 2)]
    print_call()
    global program_counter
    program_counter += 1


def st(reg1, memory_address):
    global program_counter
    r1 = registers1[reg1]
    reset_flags()
    memory[int(memory_address, 2)] = r1
    print_call()
    program_counter += 1


def mul(reg1, reg2, reg3):
    global program_counter
    r1 = registers1[reg1]
    r2 = registers1[reg2]
    r3 = registers1[reg3]
    reset_flags()
    registers1[reg1] = makebin(int(r2, 2) * int(r3, 2))
    print_call()
    program_counter += 1


def div(reg3, reg4):
    global program_counter
    r3 = registers1[reg3]
    r4 = registers1[reg4]
    reset_flags()
    r3_int = int(r3, 2)
    r4_int = int(r4, 2)
    registers1["000"] = makebin(r3_int / r4_int)
    registers1["001"] = makebin(r3_int % r4_int)
    print_call()
    program_counter += 1


def rs(reg, Imm):
    global program_counter
    r = registers1[reg]
    reset_flags()
    registers1[reg] = makebin(int(r, 2) >> int(Imm, 2))
    print_call()
    program_counter += 1


def ls(reg, Imm):
    global program_counter
    r = registers1[reg]
    reset_flags()
    registers1[reg] = makebin(int(r, 2) << int(Imm, 2))
    print_call()
    program_counter += 1


def xorISA(reg1, reg2, reg3):
    global program_counter
    r2 = registers1[reg2]
    r3 = registers1[reg3]
    reset_flags()
    registers1[reg1] = makebin(int(r2, 2) ^ int(r3, 2))
    print_call()
    program_counter += 1


def orISA(reg1, reg2, reg3):
    global program_counter
    r2 = registers1[reg2]
    r3 = registers1[reg3]
    reset_flags()
    registers1[reg1] = makebin(int(r2, 2) or int(r3, 2))
    print_call()
    program_counter += 1


def andISA(reg1, reg2, reg3):
    global program_counter
    r2 = registers1[reg2]
    r3 = registers1[reg3]
    reset_flags()
    registers1[reg1] = makebin(int(r2, 2) and int(r3, 2))
    print_call()
    program_counter += 1


def notISA(reg1, reg2):
    global program_counter
    r1 = registers1[reg2]
    reset_flags()
    registers1[reg1] = makebin(~int(r1, 2))
    print_call()
    program_counter += 1


def cmp(reg1, reg2):
    global program_counter
    r1 = registers1[reg1]
    r2 = registers1[reg2]
    reset_flags()
    r1_int = int(r1, 2)
    r2_int = int(r2, 2)
    if (r1_int == r2_int):
        flags[15] = 1
    elif (r1_int > r2_int):
        flags[14] = 1
    elif (r1_int < r2_int):
        flags[13] = 1
    print_call()
    program_counter += 1


def jmp(memory_address):
    global program_counter
    reset_flags()
    print_call()
    program_counter = int(memory_address, 2)


def jlt(memory_address):
    global program_counter
    if flags[14] == 1:
        reset_flags()
        print_call()
        program_counter = int(memory_address, 2)
    else:
        reset_flags()
        print_call()
        program_counter += 1


def jgt(memory_address):
    global program_counter
    if flags[14] == 1:
        reset_flags()
        print_call()
        program_counter = int(memory_address, 2)
    else:
        reset_flags()
        print_call()
        program_counter += 1


def je(memory_address):
    global program_counter
    if (flags[15] == 1):
        reset_flags()
        print_call()
        program_counter = int(memory_address, 2)
    else:
        reset_flags()
        print_call()
        program_counter += 1


def hlt():
    global program_counter
    reset_flags()
    print_call()
    program_counter += 1


def simulator(instruction):
    ISA = instruction[0:5]
    if (ISA == "00000"):
        reg1 = instruction[7:10]
        reg2 = instruction[10:13]
        reg3 = instruction[13:16]
        add(reg1, reg2, reg3)

    elif (ISA == "00001"):
        reg1 = instruction[7:10]
        reg2 = instruction[10:13]
        reg3 = instruction[13:16]
        sub(reg1, reg2, reg3)

    elif (ISA == "00010"):
        reg1 = instruction[5:8]
        imm = instruction[8:16]
        mov_Imm(reg1, imm)

    elif (ISA == "00011"):
        reg1 = instruction[10:13]
        reg2 = instruction[13:16]
        mov_Reg(reg1, reg2)

    elif (ISA == "00100"):
        reg1 = instruction[5:8]
        memory_address = instruction[8:16]
        ld(reg1, memory_address)

    elif (ISA == "00101"):
        reg1 = instruction[5:8]
        memory_address = instruction[8:16]
        st(reg1, memory_address)

    elif (ISA == "00110"):
        reg1 = instruction[7:10]
        reg2 = instruction[10:13]
        reg3 = instruction[13:16]
        mul(reg1, reg3, reg3)

    elif (ISA == "00111"):
        reg3 = instruction[10:13]
        reg4 = instruction[13:16]
        div(reg3, reg4)

    elif (ISA == "01000"):
        reg1 = instruction[5:8]
        imm = instruction[8:16]
        rs(reg1, imm)

    elif (ISA == "01001"):
        reg1 = instruction[5:8]
        imm = instruction[8:16]
        ls(reg1, imm)

    elif (ISA == "01010"):
        reg1 = instruction[7:10]
        reg2 = instruction[10:13]
        reg3 = instruction[13:16]
        xorISA(reg1, reg2, reg3)

    elif (ISA == "01011"):
        reg1 = instruction[7:10]
        reg2 = instruction[10:13]
        reg3 = instruction[13:16]
        orISA(reg1, reg2, reg3)

    elif (ISA == "01100"):
        reg1 = instruction[7:10]
        reg2 = instruction[10:13]
        reg3 = instruction[13:16]
        andISA(reg1, reg2, reg3)

    elif (ISA == "01101"):
        reg1 = instruction[10:13]
        reg2 = instruction[13:16]
        notISA(reg1, reg2)

    elif (ISA == "01111"):
        jmp(instruction[8:16])

    elif (ISA == "10000"):
        jlt(instruction[8:16])

    elif (ISA == "10001"):
        jgt(instruction[8:16])

    elif (ISA == "10010"):
        je(instruction[8:16])

    elif (ISA == "01110"):
        cmp(instruction[10:13], instruction[13:16])

    elif (ISA == "10011"):
        hlt()


for linee in sys.stdin.readlines():
    lines.append(str(linee))
c = 0
for line in lines:
    memory[c] = line.strip('\n')
    c = c + 1
    programcounter.append(program_counter)
    current_instruction = line[0:5]
    if (memory[c - 1] == "10011"):
        break
    else:
        simulator(line)
for i in memory:
    print(i)

pooo=[]
for i in range(0,len(programcounter)):
    pooo.append(i)
plt.scatter(programcounter, pooo)
plt.xlabel('Cycle')
plt.ylabel('Address')
plt.title('Memory accesses vs Cycles')
plt.show()


