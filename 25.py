from collections import Counter
from collections import defaultdict
from collections import deque
from scipy.spatial.transform import Rotation
import numpy as np

fo = open("25in.txt", "r")

rightCucumbers = set()
downCucumbers = set()
MAX_COL = 0
MAX_ROW = 0
for row,line in enumerate(fo.readlines()):
    line = line.strip()
    for column,c in enumerate(line):
        if c == '>':
            rightCucumbers.add((column,row))
            if column > MAX_COL:
                MAX_COL = column
        elif c == 'v':
            downCucumbers.add((column,row))
            if row > MAX_ROW:
                MAX_ROW = row
#print(rightCucumbers)
#print(downCucumbers)

MOVE_COUNT = 0

def moveRight(rc, dc):
    global MOVE_COUNT
    newRc = set()
    for r in rc:
        rightCandidate = (r[0]+1, r[1])
        if rightCandidate[0] == MAX_COL+1:
            rightCandidate = (0, r[1])
        if rightCandidate not in rc and rightCandidate not in dc:
            MOVE_COUNT += 1
            newRc.add(rightCandidate)
        else:
            newRc.add(r)
    return newRc

def moveDown(rc, dc):
    global MOVE_COUNT
    newDc = set()
    for d in dc:
        downCandidate = (d[0], d[1]+1)
        if downCandidate[1] == MAX_ROW+1:
            downCandidate = (d[0], 0)
        if downCandidate not in rc and downCandidate not in dc:
            MOVE_COUNT += 1
            newDc.add(downCandidate)
        else:
            newDc.add(d)
    return newDc

def part1():
    print("Part1")
    global rightCucumbers, downCucumbers, MOVE_COUNT
    
    currentStep = 0
    #for i in range(58):
    while True:   
        print("Iteration:", currentStep)
        """
        for row in range(MAX_ROW+1):
            rowToPrint = ""
            for col in range(MAX_COL+1):
                spot = (col,row)
                if spot in rightCucumbers:
                    rowToPrint += '>'
                elif spot in downCucumbers:
                    rowToPrint += 'v'
                else:
                    rowToPrint += '.'
            print(rowToPrint)
        """
        currentStep += 1
        rightCucumbers = moveRight(rightCucumbers,downCucumbers)
        downCucumbers = moveDown(rightCucumbers,downCucumbers)

        if MOVE_COUNT == 0:
            break
        else:
            MOVE_COUNT = 0
            
    print(currentStep)
    print("end")


# 351
part1()
# No part 2 puzzle 