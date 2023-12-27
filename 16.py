from collections import Counter
from collections import defaultdict
from collections import deque

fo = open("16in.txt", "r")

line = fo.readline()
queue = deque()
for c in line:
    h = int(c,16)
    b = bin(h)
    paddSize = 6-len(b)
    bPadd = b[2:]
    for _ in range(paddSize):
        bPadd = '0' + bPadd
    for i in range(4):
        queue.append(bPadd[i])
    #print(bPadd, paddSize)

accVersions = 0

def extractLiteralValue(q):
    binTot = ''
    packetHeadValue = q.popleft()
    while packetHeadValue == '1':
        #value = int(queue[0]+queue[1]+queue[2]+queue[3],2)
        for _ in range(4):
            binTot += q.popleft()
        packetHeadValue = q.popleft()
    #value = int(queue[0]+queue[1]+queue[2]+queue[3],2)
    for _ in range(4):
        binTot += q.popleft()
    ret = int(binTot,2)
    return(ret)

def extractTypeId0(q, values):
    binTot = ''
    for _ in range(15):
        binTot += q.popleft()
    subPacketLength = int(binTot,2)
    subQueue = deque()
    for _ in range(subPacketLength):
        subQueue.append(q.popleft())
    while '1' in subQueue:
        values.append(interpret(subQueue))

def extractTypeId1(q, values):
    binTot = ''
    for _ in range(11):
        binTot += q.popleft()
    numOfSubPackets = int(binTot,2)
    for interpretOrder in range(numOfSubPackets):
        values.append(interpret(q))

def interpret(q):
    #Header
    packetVersion = int(q.popleft()+q.popleft()+q.popleft(),2)
    global accVersions
    accVersions += packetVersion
    #print("Packet version", packetVersion)
    packetTypeId = int(q.popleft()+q.popleft()+q.popleft(),2)
    #Operation
    if packetTypeId == 4:
        retLiteral = extractLiteralValue(q)
        print("Literal", retLiteral)
        return retLiteral
    else:
        #not a value, one or more subpackets with possible operations within
        lengthTypeId = q.popleft()
        # get values from subpackets
        values = []
        if lengthTypeId == '0':
            extractTypeId0(q, values)
        else:
            extractTypeId1(q, values)
        if packetTypeId == 0:
            sum = 0
            for v in values:
                sum += v
            print("Sum is", sum)
            return sum
        elif packetTypeId == 1:
            mult = 1
            for v in values:
                mult *= v
            print("Product is", mult)
            return mult
        elif packetTypeId == 2:
            minimum = min(values)
            print("Minimum is", minimum)
            return minimum
        elif packetTypeId == 3:
            maximum = max(values)
            print("Maximum is", maximum)
            return maximum
        elif packetTypeId == 5:
            isGreater = int(values[0] > values[1])
            print("isGreater is", isGreater)
            return isGreater
        elif packetTypeId == 6:
            isLower = int(values[0] < values[1])
            print("isLower is", isLower)
            return isLower
        elif packetTypeId == 7:
            isEquals = int(values[0] == values[1])
            print("isEquals is", isEquals)
            return isEquals
        else:
            assert()

def part1():
    print("Part1")
    #broken for part 2?
    while '1' in queue:
        interpret(queue)
    print(accVersions)

def part2():
    print("Part2")
    # Id 0,+  1,*  2,min  3,max  (can have 1 or multiple)
    #    5,>  6,<  7,==          (these have exactly two arguments)
    ret = 0
    while '1' in queue:
        ret = interpret(queue)
    print(ret)
    
# 974
#part1()
# 180616437720... wow, very glad I didnt need to debug and it worked after examples :D
part2()