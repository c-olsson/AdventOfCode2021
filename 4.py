
#init
fo = open("4/input.txt", "r")
numbers = fo.readline().strip().split(",")
grids = []
rowNum = 0
gridNum = 0
for line in fo.readlines():
    if len(line) == 1:
        rowNum += 1
    else:
        line = line.strip().split()
        lineInfo = []
        for number in line:
            markable = [number, False]
            lineInfo.append(markable)
        if rowNum == 1: 
            newGrid = []
            newGrid.append(lineInfo)
            grids.append(newGrid)
        else:
            grids[gridNum].append(lineInfo)
        rowNum += 1
        if rowNum == 6:
            gridNum += 1
            rowNum = 0


def markNumber(grid, number):
    for r in range(5):
        for c in range(5):
            if grid[r][c][0] == number:
                grid[r][c][1] = True
                return

def checkAnyWinnerPart1(grids):
    gridNum = 0
    for grid in grids:
        for r in range(5):
            numMarked = 0
            for num in grid[r]:
                if num[1]:
                    numMarked +=1
            if numMarked == 5:
                return gridNum
        for c in range(5):
            numMarked = 0
            for r in range(5):
                if grid[r][c][1]:
                    numMarked +=1
            if numMarked == 5:
                return gridNum
        gridNum += 1
    return -1

def addWinnerPart2(grids, winners):
    gridNum = 0
    for grid in grids:
        for r in range(5):
            numMarked = 0
            for num in grid[r]:
                if num[1]:
                    numMarked +=1
            if numMarked == 5 and winners.count(gridNum) == 0:
                winners.append(gridNum)
        for c in range(5):
            numMarked = 0
            for r in range(5):
                if grid[r][c][1]:
                    numMarked +=1
            if numMarked == 5 and winners.count(gridNum) == 0:
                winners.append(gridNum)
        gridNum += 1

def getUnmarkedSum(grid):
    sum = 0
    for r in range(5):
        for c in range(5):
            if grid[r][c][1] == False:
                sum += int(grid[r][c][0])
    return sum

def part1():
    #mark until winner
    curNumberIndex = 0
    while True:
        winningGridNum = checkAnyWinnerPart1(grids)
        if winningGridNum != -1:
            break
        for grid in grids:
            markNumber(grid, numbers[curNumberIndex])
        curNumberIndex += 1
    #res   
    sumOfUnmarked = getUnmarkedSum(grids[winningGridNum])
    result = int(numbers[curNumberIndex-1]) * sumOfUnmarked
    print(result)

def part2():
    #mark until winner
    curNumberIndex = 0
    winners = []
    for next in numbers:
        addWinnerPart2(grids, winners)
        if len(winners) == len(grids):
            break
        for grid in grids:
            markNumber(grid, next)
        curNumberIndex += 1
    #res   
    winningGridNum = winners[-1]
    sumOfUnmarked = getUnmarkedSum(grids[winningGridNum])
    result = int(numbers[curNumberIndex-1]) * sumOfUnmarked
    print(result)

    
#11536
part1()
#1284
part2()