from collections import Counter
from collections import defaultdict
from collections import deque

fo = open("18in.txt", "r")

input = []
for line in fo.readlines():
    input.append(line.strip())
#print(input)

def isdigit(c):
    return c != '[' and c != ']' and c != ','

def getExplodingIndex(s):
    numberOfLeftBrackets = 0
    for i, char in enumerate(s):
        if char == '[':
            numberOfLeftBrackets += 1
            if numberOfLeftBrackets == 5:
                # due to previous explotions we now its here a digit
                if not isdigit(s[i+1]):
                    assert()
                return i+1
        elif char == ']':
            numberOfLeftBrackets -= 1
    return -1

def getLeftDigitIndex(i, s):
    while i > 0:
        i -= 1
        if isdigit(s[i]):
            return i
    return -1

def getRightDigitIndex(i, s):
    while i < len(s)-1:
        i += 1
        if isdigit(s[i]):
            return i
    return -1

def explode(i, s):
    leftDigit = int(s[i])
    rightDigit = int(s[i+2])
    #print("Exploding", leftDigit, rightDigit)
    #print("When current is", s)
    li = getLeftDigitIndex(i,s)
    if li != -1:
        lNumber = int(s[li])
        s[li] = str(leftDigit + lNumber)
    ri = getRightDigitIndex(i+2,s)
    if ri != -1:
        rNumber = int(s[ri])
        s[ri] = str(rightDigit + rNumber)
    #replace [leftDigit,rightDigit] to 0
    for _ in range(4):
        del s[i-1]
    s[i-1] = '0'
    #print("After explode", s)
    return s

def getSplitIndex(s):
    for i, char in enumerate(s):
        if isdigit(char) and int(char) >= 10:
            return i
    return -1

def split(i, s):
    #print("Splitting", s[i], i)
    #print("When current is", s)
    splitNumber = int(s[i])
    leftInPair = int(splitNumber / 2)
    rightInPair = int(splitNumber / 2) + splitNumber%2
    s[i] = ']'
    s.insert(i, str(rightInPair))
    s.insert(i, ',')
    s.insert(i, str(leftInPair))
    s.insert(i, '[')
    #print("After split", s)
    return s

def getPairIndex(s):
    for i in range(len(s)-4):
        if s[i] == "[" and s[i+4] == "]":
            return i
    assert()

def getMagnitude(s):
    magnitude = 0
    while len(s)>4:
        pairIndex = getPairIndex(s)
        newValue = 3*int(s[pairIndex+1]) + 2*int(s[pairIndex+3])
        for _ in range (4):
            del s[pairIndex]
        s[pairIndex] = newValue
    return s[0]

def fishAdd(lNumber, rNumber):
    lNumber.insert(0, "[")
    lNumber.append(",")
    for char in rNumber:
        lNumber.append(char)
    lNumber.append("]")
    
    # Prio list is
    # 1. Do explotion (can generate splits)
    # 2. Do splits (can generate explotions, so do explotion first before a possible second split)
    reduceActions = True
    while reduceActions:
        while True:
            # do all explotions
            explodeIndex = getExplodingIndex(lNumber)
            if explodeIndex != -1:
                lNumber = explode(explodeIndex, lNumber)
            else:
                break;
        
        # do posssible split
        splitIndex = getSplitIndex(lNumber)
        if splitIndex != -1:
            lNumber = split(splitIndex, lNumber)
        else:
            reduceActions = False
            break;
    return lNumber


def part1():
    print("Part1")
    
    currentNumber = []
    for char in input[0]:
        currentNumber.append(char)
    
    for i in range(1,len(input)):
        newNumber = []
        for char in input[i]:
            newNumber.append(char)
        currentNumber = fishAdd(currentNumber, newNumber)
            
    # Count magnitude
    resString = ""
    for char in currentNumber:
        resString += char
    magnitude = getMagnitude(currentNumber)
    print(resString)
    print(magnitude)


def part2():
    print("Part2")
    
    maxMagnitude = 0
    maxString = ""
    for leftNumberString in input:     
        for rightNumberString in input:
            if leftNumberString == rightNumberString:
                continue
            lNumber = []
            for char in leftNumberString:
                lNumber.append(char)
            rNumber = []
            for char in rightNumberString:
                rNumber.append(char)
            
            addedNumber = fishAdd(lNumber,rNumber)
            
            resString = ""
            for char in addedNumber:
                resString += char
            magnitude = getMagnitude(addedNumber)
            if magnitude > maxMagnitude:
                maxMagnitude = magnitude
                maxString = resString
            #print(resString)
            print(magnitude)
    
    print("Max magnitude is", maxMagnitude)
    print("Max magnitude for res", maxString)

# 3734
#part1()
# 4837 could probably be faster, alot of list iterations and manipulations done.
# Eg tree representation rather than list, then no storing of chars '[' ',' ']'
#    pair removal then easy (always a leaf), also left/right values are in neighbour nodes
part2()