
fo = open("3/input.txt", "r")
input = []
for line in fo.readlines():
    input.append(line.strip())

def getCommonBit(list, bitIndex, isCommon=True):
    countZeroes = 0
    countOnes = 0
    for number in list:        
        if number[bitIndex] == '1':
            countOnes += 1
        else:
            countZeroes += 1
    if isCommon:
        if countOnes >= countZeroes:
            return '1'
        else:
            return '0'
    else:
        if countOnes >= countZeroes:
            return '0'
        else:
            return '1'

def part1():
    gammaRate = ''   #most common digit for each bitIndex
    epsilonRate = '' #least common
    for bitIndex in range(0,len(input[0])):
        commonBit = getCommonBit(input, bitIndex)
        gammaRate += commonBit
        if commonBit == '1':
            epsilonRate += '0'
        else:
            epsilonRate += '1'

    fuel = int(gammaRate, 2) * int(epsilonRate, 2)
    print(fuel)

def extractCommonNumber(list, common=True):
    bitIndex = 0
    while len(list) != 1:
        commonBit = getCommonBit(list, bitIndex, common)
        #remove unqualified list items
        listIndex = 0
        while listIndex < len(list):
            if list[listIndex][bitIndex] != commonBit:
                del list[listIndex]
                listIndex -= 1
            listIndex += 1
        bitIndex += 1
    return list[0]

def part2():
    theCommon = input.copy()
    commonNumber = extractCommonNumber(theCommon)
    theNotCommon = input.copy()
    notCommonNumber = extractCommonNumber(theNotCommon, False)
    
    lifeSupportRating = int(commonNumber, 2) * int(notCommonNumber, 2)
    print(lifeSupportRating)

#3549854
part1()
#3765399
part2()