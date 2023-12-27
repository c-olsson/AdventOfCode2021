from collections import Counter

fo = open("9ins.txt", "r")

matrix = []
for line in fo.readlines():
    col = 0
    line = line.strip()
    rowList = []
    for d in line:
        rowList.append(int(d))
    matrix.append(rowList)
print(matrix)

STEPS = [(1,0), (0,1), (-1,0), (0,-1)]
                
def part1():
    res = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            current = matrix[y][x]
            lowCount = 0
            for step in STEPS:
                nx = x + step[0]
                ny = y + step[1]
                if nx >= len(matrix[0]) or nx < 0:
                    lowCount += 1
                    continue
                if ny >= len(matrix) or ny < 0:
                    lowCount += 1
                    continue
                neighbour = matrix[ny][nx]
                if current < neighbour:
                    lowCount += 1
            if lowCount == 4:
                res += 1 + current
                #print("row",y+1,"col",x+1,"current",current)
    print(res)


def recursive(basin, matrix, x, y):
    for step in STEPS:
        nx = x + step[0]
        ny = y + step[1]
        if nx >= len(matrix[0]) or nx < 0:
            continue
        if ny >= len(matrix) or ny < 0:
            continue
        currentValue = matrix[ny][nx]
        current = (nx,ny)
        if currentValue != 9 and current not in basin:
            basin.add(current)
            recursive(basin, matrix, nx, ny)
        else:
            continue

def part2():
    basins = []
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 9:
                continue
            inBasin = False
            for basin in basins:
                if (x,y) in basin:
                    inBasin = True
                    break
            if not inBasin:
                # None existing, start new basin and deep search remaining in that basin
                basin = set([(x,y)])
                basins.append(basin)
                recursive(basin, matrix, x, y)
    # check top 3 len(set) in basins and multiply them     
    basinLengths = []
    for basin in basins:
        basinLengths.append(len(basin))
    basinLengths.sort(reverse=True)
    print(basinLengths[0]*basinLengths[1]*basinLengths[2])


#528
part1()
#920448
part2()
