from collections import Counter
from collections import defaultdict
from collections import deque
from scipy.spatial.transform import Rotation
import numpy as np

fo = open("24in.txt", "r")

# Input has 14 ALU instructions
# investigate one each to see possible outputs to try out for full MONAD

input = []
inputAlu = []
prevWasInp = False
for line in fo.readlines():
    lineList = line.strip().split()
    if lineList[0] == 'inp':
        if inputAlu:
            input.append(inputAlu)
        inputAlu = []
    inputAlu.append(lineList)
input.append(inputAlu)
#print(input)

# Operations
# inp  add  mul  div mod  eql
# Registers, ranges 1-9
# w  x  y  z

def operation(inst, REGISTERS):
    if inst[0] == 'mul':
        workRegisterId = inst[1]
        if inst[2] not in REGISTERS.keys():
            REGISTERS[workRegisterId] *= int(inst[2])
        else:
            REGISTERS[workRegisterId] *= REGISTERS[inst[2]]
    elif inst[0] == 'eql':
        workRegisterId = inst[1]
        if inst[2] not in REGISTERS.keys():
            REGISTERS[workRegisterId] = int(REGISTERS[inst[1]] == int(inst[2]))
        else:
            REGISTERS[workRegisterId] = int(REGISTERS[inst[1]] == REGISTERS[inst[2]])
    elif inst[0] == 'add':
        workRegisterId = inst[1]
        if inst[2] not in REGISTERS.keys():
            REGISTERS[workRegisterId] += int(inst[2])
        else:
            REGISTERS[workRegisterId] += REGISTERS[inst[2]]
    elif inst[0] == 'mod':
        REGISTERS[inst[1]] = REGISTERS[inst[1]] % int(inst[2])
    elif inst[0] == 'div':
        REGISTERS[inst[1]] = int(REGISTERS[inst[1]] / int(inst[2]))
    else:
        assert()

# always w=1 except the -Indexes, "3":5, "7":4, "8":5, "10":NA_twodigit, "11":5, "12":5
MIN_W = [0, 8,213,5547,213, 5544, 144159,3748147,144159,5544,144152,144151,144153,144149,5544] 
# always w=9 and growing, interesting only to know we can maximze until valid. Aka higher W gives expected result ?? offset 1 usually per iteration.
MAX_W = [0,16,429,11171,11164,290278,7547251] #...
POS = 2

def printZrange():
    for wToChange in range(1,10):
        #MODEL_NUMBER[0] = wToChange
        #for w in MODEL_NUMBER:
        REGISTERS = {'w':0, 'x':0, 'y':0, 'z': MIN_W[POS]}
        for instIteration in input[POS:POS+1]:
            for inst in instIteration:
                if inst[0] == 'inp':
                    REGISTERS[inst[1]] = wToChange
                    continue
                operation(inst, REGISTERS)
        print(REGISTERS)
#printZrange()

divisor = [1,1,1,26,1,1,1,26,26,1,26,26,26,26]
adder = [14,12,11,-4,10,10,15,-9,-9,12,-15,-7,-10,0]
adder2 = [7,4,8,1,5,14,12,10,5,7,6,8,4,6]

def compiledCode(input,z,i):
    """
    x = (z % 26)
    check = int((x  + adder[i]) != input)
    z = z//divisor[i]

    y1 = 25*check + 1
    z = z*y1
    y2 = input + adder2[i]
    y2 = y2 * check

    z = z+y2
    """
    if ((z % 26)  + adder[i]) == input:
        z = z //divisor[i]
    else:
        z = z //divisor[i]
        z = z*26
        z = z + input + adder2[i]
    #print(z)
    return z
    
#for w in range(1,10):
#    compiledCode(w,213,2)


MODEL_NUMBER = []
#example = "13579246899999"
maxPart1 = "29599469991739"
minPart2 = "17153114691118"
try_out = minPart2
for d in try_out:
    MODEL_NUMBER.append(int(d))
    
def evaluate(mn):
    
    #REGISTERS = {'w':0, 'x':0, 'y':0, 'z': 0}
    zPrev = 0
    for i,w in enumerate(mn):
        for instIteration in input:
            for inst in instIteration:
                if inst[0] == 'inp':
                    #EGISTERS['w'] = int(w)
                    zPrev = compiledCode(int(w),zPrev,i)
                    break
                else:
                    #my operation function didnt work well
                    #operation(inst, REGISTERS)
                    continue
    # If not 0 here its invalid
    print(zPrev)
    
evaluate(maxPart1)
evaluate(minPart2)
print("Stop here")

def calNextZ(w, zPrev, sbIndex):
    REGISTERS = {'w':w, 'x':0, 'y':0, 'z': zPrev}
    for instIteration in input[sbIndex:sbIndex+1]:
        for inst in instIteration:
            if inst[0] == 'inp':
                #already inited
                continue
            operation(inst, REGISTERS)
    return REGISTERS['z']

def part1():
    print("Part1")
    aluStates = {}
    aluStates[(1,0,0,0)] = 0
    
    #for sbIndex in range(14):
        #REGISTER()
        #for w in range(1,10):
            #if 
        
    print("end")

def part1Impossible():
    print("Part1 Impossible style")

    # Init first 9 z values to be used for the recursion
    values = {}
    for w0 in range(1,10):
        z0 = calNextZ(w0, 0, 0)
        for w1 in range(1,10):
            z1 = calNextZ(w1, z0, 1)
            for w2 in range(1,10):
                z2 = calNextZ(w2, z1, 2)
                for w3 in range(1,10):
                    z3 = calNextZ(w3, z2, 3)
                    """
                    for w4 in range(1,10):
                        z4 = calNextZ(w4, z3, 4)
                        
                        for w5 in range(1,10):
                            z5 = calNextZ(w5, z4, 5)"""
                    values[(w0,w1,w2,w3)] = z3
                    if z3 < 250:
                        print("Value",z3,w0,w1,w2,w3)
            #print(z)
    print(max(values.values()))
    print(min(values.values()))
    
    ##for sbIndex in range(14):
     #   for nextW in range(1,10):
     #       value = calNextZ(nextW, 0, sbIndex)
            
    print("end")


def part2():
    print("Part2")
 
    print("end")


# Largest valid 14 digit number (no 0s), valid if z is 0. Each inst. is 18 in len
# First four inst the same: inp w, mul x 0 (reset x), add x z (z->x), mod x 26 (inits z%26)
# x reset 1 and y reset 2, z is used as continues output, last value must be -7 to -15 to make valid MONAD. 6 of 14 has a single negativ add
# 9 valid w combinations for each SigBit step, to build on Zprevious
# Conclusion: function for next Z is given as f(w,Zn-1,nextAluInstructions), countable compared to 9**14
part1()

# 
#part2()