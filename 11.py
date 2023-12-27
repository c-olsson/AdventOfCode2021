from collections import Counter
from collections import deque

fo = open("11in.txt", "r")

matrix = []
for line in fo.readlines():
    line = line.strip()
    row = []
    for c in line:
        row.append(int(c))
    matrix.append(row)
print(matrix)

STEPSX = [1, 1, 0,-1,-1,-1, 0, 1]
STEPSY = [0, 1, 1, 1, 0,-1,-1,-1]

MAXX = len(matrix[0])
MAXY = len(matrix)

def notOutsideBorder(x,y):
    return not(x<0 or x>=MAXX or y<0 or y>=MAXY)

def part1():
    numFlashes = 0
    for iteration in range(1,601):
        for y in range(MAXY):
            for x in range(MAXX):
                matrix[y][x] += 1
        
        #init neoghbours to all 10s, bigger than 9 but not multiples like 11+
        que = deque()
        for y in range(MAXY):
            for x in range(MAXX):
                if notOutsideBorder(x,y) and matrix[y][x] == 10:
                    for i in range(len(STEPSX)):
                        dx = STEPSX[i]
                        dy = STEPSY[i]
                        if notOutsideBorder(x+dx,y+dy):
                            que.append((x+dx,y+dy))
        #we have first flashers, check chain reactions for these neighbours
        while que:
            coord = que.popleft()
            # always +1 due to previous neighbour
            matrix[coord[1]][coord[0]] += 1
            # trigger more neighbours if flash triggered
            if matrix[coord[1]][coord[0]] == 10:
                for i in range(len(STEPSX)):
                    dx = STEPSX[i]
                    dy = STEPSY[i]
                    if notOutsideBorder(coord[0]+dx,coord[1]+dy):
                        que.append((coord[0]+dx,coord[1]+dy))
            # if 11+, already visited dont want new neighbours again
               
        prevFlashes = numFlashes 
        for y in range(MAXY):
            for x in range(MAXX):
                if matrix[y][x] > 9:
                    numFlashes += 1
                    matrix[y][x] = 0
        if numFlashes-prevFlashes == MAXX*MAXY:
            print("All flashed at #", iteration)
        #print("After #", iteration, numFlashes)
        if iteration == 100:
            print("After 100 iterations:",numFlashes)

def part2():
    completions = []
    
    print(0)

#1713
part1()
#502
#part2()