from collections import Counter

fo = open("8in.txt", "r")


inputParts = []
inputString = []
inputOut = []
inputSchema = []
for line in fo.readlines():
    inputParts = line.split(" | ")
    inputRight = inputParts[1].split()
    inputOut.append(inputRight)
    inputLeft = inputParts[0].split()
    inputSchema.append(inputLeft)
#print(inputOut)
#print(inputSchema)

def part1():
    counter = Counter()
    for l in inputOut:
        for s in l:
            if (len(s) == 2 or len(s) == 4 or len(s) == 3 or len(s) == 7):
                print(s)
            counter.update([len(s)])
    print(counter[2]+counter[4]+counter[3]+counter[7])

#pureSchema = {2: 'acdeg', 3: 'acdfg', 5: 'abdfg', 0: 'abcefg', 6: 'abdefg', 9: 'abcdfg'}

def decideSchema(l):
    schema = {}
    for s in l:
        if len(s) == 2:
            schema[1] = s
        elif len(s) == 4:
            schema[4] = s
        elif len(s) == 3:
            schema[7] = s
        elif len(s) == 7:
            schema[8] = s
    #now we have some more info in schema to do 5 and 6 uniques
    for s in l:
        if len(s) == 5:
            # it is 2, 3 or 5
            num1Match = 0
            num4Match = 0
            for c in s:
                if c in schema[1]:
                    num1Match += 1
                if c in schema[4]:
                    num4Match += 1
            # 3 has both segments in 1, while 2 and 5 only have one
            if num1Match == 2:
                schema[3] = s
            # 2 has two segments in 4, one in 1
            if num4Match == 2 and num1Match == 1:
                schema[2] = s
            # 5 has three segments in 4, one in 1
            if num4Match == 3 and num1Match == 1:
                schema[5] = s
        elif len(s) == 6:
            # it is 0, 6 or 9
            num1Match = 0
            num4Match = 0
            for c in s:
                if c in schema[1]:
                    num1Match += 1
                if c in schema[4]:
                    num4Match += 1
            # 6 has only one segments in 1, 2 and 5 has both
            if num1Match == 1:
                schema[6] = s
            # 0 has three segments in 4, one in 1
            if num4Match == 3 and num1Match == 2:
                schema[0] = s
            # 9 has all four segments in 4, one in 1
            if num4Match == 4 and num1Match == 2:
                schema[9] = s
    schemaWithSortedPattern = {}
    for i in range(len(schema)):
        stringPatternList = list(schema[i])
        stringPatternList.sort()
        sortedString = ""
        for c in stringPatternList:
            sortedString += c
        #sortedString = str(stringPatternList)
        schemaWithSortedPattern[i] = sortedString
    return schemaWithSortedPattern

def part2():
    ack = 0
    for i in range(len(inputSchema)):
        schemaSortedStringValues = decideSchema(inputSchema[i])
        #print(schema)
        value = 0
        indexInValue = 3
        for pattern in inputOut[i]:
            patternList = list(pattern)
            patternList.sort()
            sortedPattern = ""
            for c in patternList:
                sortedPattern += c
            #print(sortedPattern)
            for matchCandKey in schemaSortedStringValues:
                if schemaSortedStringValues[matchCandKey] == sortedPattern:
                    value += matchCandKey*(10**indexInValue)
                    indexInValue -= 1
        #print("row Value =", value)
        ack += value
    print(ack)
            
    
#390
#part1()
#1011785
part2()