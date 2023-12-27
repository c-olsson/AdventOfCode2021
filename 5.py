
fo = open("5in.txt", "r")

input = []
boarders = [99999, -1, 99999, -1] #minX, maxX, minY, maxY
for line in fo.readlines():
    split = line.split()
    start = split[0].split(",")
    start[0] = int(start[0])
    start[1] = int(start[1])
    end = split[2].split(",")
    end[0] = int(end[0])
    end[1] = int(end[1])
    input.append([start, end])
    #print(start, end)
for i in input:
    startX = i[0][0]
    endX = i[1][0]
    startY = i[0][1]
    endY = i[1][1]
    if boarders[0] > startX:
        boarders[0] = startX
    if boarders[0] > endX:
        boarders[0] = endX
    if boarders[1] < startX:
        boarders[1] = startX
    if boarders[1] < endX:
        boarders[1] = endX
    if boarders[2] > startY:
        boarders[2] = startY
    if boarders[2] > endY:
        boarders[2] = endY
    if boarders[3] < startY:
        boarders[3] = startY
    if boarders[3] < endY:
        boarders[3] = endY
#[10, 988, 10, 990]
print(boarders)
area = []
for y in range(1+boarders[3]):
    rowValues = []
    for x in range(1+boarders[1]):
        rowValues.append(0)
    area.append(rowValues)
#print(area)

def part1():
    for i in input:
        startX = i[0][0]
        endX = i[1][0]
        startY = i[0][1]
        endY = i[1][1]
        if startY == endY:
            if startX > endX:
                tmp = endX
                endX = startX
                startX = tmp
            for x in range(startX, 1+endX):
                area[startY][x] += 1
        elif startX == endX:
            if startY > endY:
                tmp = endY
                endY = startY
                startY = tmp
            for y in range(startY, 1+endY):
                area[y][startX] += 1
        else:
            print("Ignore diagonal line")
    res = 0
    for r in range(len(area)):
        for c in range(len(area[r])):
            if area[r][c] > 1:
                res += 1
    print(res)
    

def part2():
    for i in input:
        startX = i[0][0]
        endX = i[1][0]
        startY = i[0][1]
        endY = i[1][1]
        if startY == endY:
            if startX > endX:
                tmp = endX
                endX = startX
                startX = tmp
            for x in range(startX, 1+endX):
                area[startY][x] += 1
        elif startX == endX:
            if startY > endY:
                tmp = endY
                endY = startY
                startY = tmp
            for y in range(startY, 1+endY):
                area[y][startX] += 1
        else:
            dx = -1
            if startX < endX:
                dx = 1
            dy = -1
            if startY < endY:
                dy = 1
            rangeLen = abs(startX-endX) + 1
            for step in range(rangeLen):
                area[startY+step*dy][startX+step*dx] += 1
            
    res = 0
    for r in range(len(area)):
        for c in range(len(area[r])):
            if area[r][c] > 1:
                res += 1
    print(res)
    
#4826
#part1()
#16793
part2()