from collections import Counter
from collections import defaultdict
from collections import deque

from scipy.spatial.transform import Rotation
import numpy as np

fo = open("20ins.txt", "r")

algoritmString = fo.readline().strip()
fo.readline()
baseMap = []
for line in fo.readlines():
    baseMap.append(line.strip())
#print(baseMap)

def addInifinityBoarders(m,t):
    topAndBottom = ""
    for _ in range(len(m)):
        # Either infinity is all . or # making it 
        # TODO fix this boarder infinity shit
        topAndBottom += t
    m.append(topAndBottom)
    m.insert(0, topAndBottom)
    for i,row in enumerate(m):
        m[i] = t + row + t

DC = [-1,0,1,-1,0,1,-1,0,1]
DR = [-1,-1,-1,0,0,0,1,1,1]

def getBinaryString(mb,r,c):
    ret = ""
    for i in range(len(DR)):
        rowIndex = r+DR[i]
        colIndex = c+DC[i]
        char = mb[rowIndex][colIndex]
        if char == '#':
            ret += '1'
        else:
            ret += '0'
    return ret

def populateNextMap(mn, mb):
    for r in range(1,len(mb)-1):
        nextPixelRow = ""
        for c in range(1,len(mb)-1):
            binaryString = getBinaryString(mb,r,c)
            binaryIndex = int(binaryString,2)
            nextPixel = algoritmString[binaryIndex]
            nextPixelRow += nextPixel
        #mn[r] = nextPixelRow
        mn.append(nextPixelRow)

def solve(iterations):
    print("Part1")
    global baseMap
    
    # Tricky, if alg[0] is "#" and alg[-1] is "." the infinity will be flashing
    # Either way, init with '.'
    nextBoardertype = '.'
    
    for i in range(iterations):
        # run algorithm twice, 
        # add around boarder either algoritmString[0] if prev_boarder='.' or algoritmString[-1] if prev_boarder='#'
        for it in range(2):
            addInifinityBoarders(baseMap, nextBoardertype)
        nextMap = []
        populateNextMap(nextMap,baseMap)
        baseMap = nextMap
        
        #cherry-pick any boarder char
        nextBoardertype = nextMap[0][0]
        print(i)
        
    countHash = 0
    for row in nextMap:
        countHash += row.count("#")
        print(row)
    print(countHash)
        

# Part1: 5347
#solve(2)
# Part2: 17172
solve(50)