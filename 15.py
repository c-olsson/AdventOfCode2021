
import heapq

from dataclasses import dataclass, field
from typing import Any

fo = open("15ins.txt", "r")

matrix = []
for line in fo.readlines():
    line = line.strip()
    row = []
    for d in range(len(line)):
        row.append(int(line[d]))
    matrix.append(row)
#print(matrix)

bigMatrix = []
for i in range(5*len(matrix)):
    row = []
    for j in range(5*len(matrix)):
        row.append(0)
    bigMatrix.append(row)
    
valueMapping = [-10000,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9]#value 9+8 is possible max mappingIndex
for rr in range(5):
    for cc in range(5):
        # formula for each element, (x0y0 + cc ++ rr) mod 10 + (rest + 1_if_rest). Hm not use 0 rest, just use a mapping.
        for smalR in range(len(matrix)):
            for smalC in range(len(matrix[0])):
                bigX = smalC + cc*len(matrix[0])
                bigY = smalR + rr*len(matrix)
                baseValue = matrix[smalR][smalC]
                insertValue = valueMapping[baseValue + cc + rr]
                bigMatrix[bigY][bigX] = insertValue
        
#print(bigMatrix)
for i in bigMatrix:
    minInRow = min(i)
    if minInRow <= 0:
        assert()


def splitUp(m, x, y, dx, dy, risks, currentRisk, steps, MAX_STEPS):
    # scenario optimize, if currentRisk > currentMinimalInSearch -> ignore
    if risks:
        currentMinimalInSearch = min(risks)
    else:
        currentMinimalInSearch = HIGH_RISK
    if currentMinimalInSearch <= currentRisk:
        #print("A Returned when risk length=", len(risks))
        return
    # Scenario 1: outside grid -> add candidate with max cost 9 for each remaining steps, might wanna go there still
    if x >= len(m[0]) or y >= len(m):
        risks.append(currentRisk + 9*(MAX_STEPS - steps))
        #print("B Returned when risk length=", len(risks))
        return
    currentRisk += m[y][x]
    # Scenario 2: end of full m -> add current riks to list
    if x == len(m[0])-1 and y == len(m)-1:
        #print("I can see the opening!")
        risks.append(currentRisk)
        #print("C Returned when risk length=", len(risks))
        return
    # Scenario 3: end of depth search -> add current riks to list
    if steps == MAX_STEPS:
        #print("Adding", currentRisk, "from position", x, y)
        risks.append(currentRisk)
        #print("D Returned when risk length=", len(risks))
        return
    # Scenario 4: continue depth search -> recursivly split up right and down
    elif steps < MAX_STEPS:
        splitUp(m, x+dx, y+dy, 1, 0, risks, currentRisk, steps+1, MAX_STEPS)
        splitUp(m, x+dx, y+dy, 0, 1, risks, currentRisk, steps+1, MAX_STEPS)

HIGH_RISK = 1e20
def part1():
    print("Part1")
    # looking all possible 9x9 forward we know that optimal path, min being 9 all 1s
    # then choose that first step, then check next 9x9
    # Possible ways in a 3x3 grid
    #  1 2 3  1 2 .  1 2 .  1 . .  1 . .  1 . .
    #  . . 4  . 3 4  . 3 .  2 3 4  2 3 .  2 . .
    #  . . 5  . . 5  . 4 5  . . 5  . 4 5  3 4 5
    # Possible ways in a 4x4 grid
    #  1 2 3 4  1 2 3 .  1 2 . .  1 2 . .  1 2 . .  1 . . .  1 . . .  1 . . .  1 . . .  1 . . .  1 . . .  1 . . .  1 . . .
    #  . . . 5  . . 4 5  . 3 4 5  . 3 4 .  . 3 4 .  2 3 4 5  2 3 4 .  2 3 4 .  2 3 . .  2 3 . .  2 3 . .  2 . . .  2 . . .
    #  . . . 6  . . . 6  . . . 6  . . 5 6  . . 5 .  . . . 6  . . 5 6  . . 5 .  . 4 5 6  . 4 5 .  . 4 . .  3 4 . .  3 . . . 
    #  . . . 7  . . . 7  . . . 7  . . . 7  . . 6 7  . . . 7  . . . 7  . . 6 7  . . . 7  . . 6 7  . 5 6 7  . 5 6 7  4 5 6 7
    # So this *luckely* worked well enough on part 1 and example part 2, but not proper part 2, to slow as well dont cover every path
    stepsToGoal = 2*(len(matrix)-1)
    GRID_WIDTH_SEARCH = 8
    MAX_STEPS = 2*(GRID_WIDTH_SEARCH-1) # for a 3x3 grid search
    
    # lets assume you wanna go closer to goal only, that is x+1 or y+1
    # get some cost estimate and then go for the direction with lower risk
    currentX = 0
    currentY = 0
    totalCost = 0
    
    for step in range(stepsToGoal):
        print("Step number", step)
        #check going right
        risksRight = []
        steps = 1
        currentRisk = 0
        splitUp(matrix, currentX+1, currentY, 1, 0, risksRight, currentRisk, steps, MAX_STEPS)
        splitUp(matrix, currentX+1, currentY, 0, 1, risksRight, currentRisk, steps, MAX_STEPS)               
        minRiskRight = HIGH_RISK
        if risksRight:
            minRiskRight = min(risksRight)
        #print("Going right costs",minRiskRight)
        #check going down
        risksDown = []
        steps = 1
        currentRisk = 0
        splitUp(matrix, currentX, currentY+1, 1, 0, risksDown, currentRisk, steps, MAX_STEPS)  
        splitUp(matrix, currentX, currentY+1, 0, 1, risksDown, currentRisk, steps, MAX_STEPS)                    
        minRiskDown = HIGH_RISK
        if risksDown:
            minRiskDown = min(risksDown)
        #print("Going down costs", minRiskDown)
        
        if minRiskDown < minRiskRight:
            currentY += 1
            totalCost += matrix[currentY][currentX]
            print("Down!", currentX, currentY)
        elif minRiskDown > minRiskRight:
            currentX += 1
            totalCost += matrix[currentY][currentX]
            print("Right!", currentX, currentY)
        elif minRiskDown == minRiskRight and minRiskDown != HIGH_RISK:
            currentY += 1
            totalCost += matrix[currentY][currentX]
            print("Costs the same, just go down then", currentX, currentY)
        print("Total cost is", totalCost)


def part2():
    print("Dijkstra algortihm")
    # Implement Dijkstras shortest path algorithm
    # 1. Initilize a map with all vertexes with distance (inf for all except start 0) and prev. vertex (unknown).
    # 2. Initilize two sets, visited (empty) and not visited (all nodes). Init current vertex as start.
    # 3. While unvisted vertexes
    # 3.1   Gather the unvisited neighbours from current vertex
    # 3.2   For each neighbour
    # 3.2.1     calculate distance from start vertex
    # 3.2.2     if dist. is shorter than known, update info of short dist. and "prev. vertex" (here current vertex)
    # 3.3   add current vertex as visited
    # 3.4 greedy?: update current vertex to the closest neighbour recently visited. Can close you in, better is a prio queue.
    # 3.4 brute: so you need nextvisit to be carefully choosen, can't go through all in any order
    # 3.4 prioqueue: only proper way! Datastructure of heaptree is preferred, updated with the prio of total risk
    # 4. Done, all info is now in map
    
    # 1 and 2
    djikstra = {}
    visited = set()
    unvisited = set()
    # inf distance and last visited non existing
    #m = bigMatrix
    m = matrix
    dummyDjikstraElement = [10e9, -1, -1]
    for x in range(len(m)):
        for y in range(len(m)):
            djikstra[(x,y)] = dummyDjikstraElement.copy()
            unvisited.add((x,y))
    currentVertex = (0,0)
    prioQueue = []
    heapq.heappush(prioQueue, (0, currentVertex))
    djikstra[currentVertex][0] = 0
    
    # 3
    iteration = 0
    while unvisited:
        currentVertexPop = heapq.heappop(prioQueue)
        currentVertex = currentVertexPop[1]
        while currentVertex not in unvisited:
            currentVertexPop = heapq.heappop(prioQueue)
            currentVertex = currentVertexPop[1]
        
        # 3.1
        neighboursFour = []
        currentX = currentVertex[0]
        currentY = currentVertex[1]
        # add all four possible, then use only if we are inside boarder and that spot is unvisited
        neighboursFour.append((currentX+1, currentY))
        neighboursFour.append((currentX, currentY+1))
        neighboursFour.append((currentX-1, currentY))
        neighboursFour.append((currentX, currentY-1))
        neighboursNotVisitAndInBorder = []
        for i in range(4):
            coord = neighboursFour[i]
            nx = coord[0]
            ny = coord[1]
            if (0 <= nx and nx < len(m)) and (0 <= ny and ny < len(m)):
                if (nx,ny) in unvisited:
                    neighboursNotVisitAndInBorder.append(coord)
        # 3.2
        for n in neighboursNotVisitAndInBorder:
            nx = n[0]
            ny = n[1]
            neighbourDistance = m[ny][nx]
            # 3.2.1
            neighbourDistFromStart = djikstra[currentVertex][0] + neighbourDistance
            # 3.2.2 update dist and prev. neigh. if lower start distance
            if neighbourDistFromStart < djikstra[(nx,ny)][0]:
                djikstra[(nx,ny)][0] = neighbourDistFromStart
                djikstra[(nx,ny)][1] = currentX
                djikstra[(nx,ny)][2] = currentY
        # 3.3
        visited.add(currentVertex) # not really used, unvisited is enough for this problem
        unvisited.remove(currentVertex)
        # 3.4         
        # Add neighbors not visited yet, to get highest prio vertex for next current
        for remainer in neighboursNotVisitAndInBorder:
            remainerTuple = tuple(remainer)
            newPrio = (djikstra[remainerTuple][0], remainerTuple)
            heapq.heappush(prioQueue, newPrio)
        
        heapq.heapify(prioQueue)
        
        #iteration += 1
        #if iteration % 100000 == 0:
            #print("Iteration", iteration, "len of prioQueue", len(prioQueue))

    bottomRightCorner = (len(m)-1, len(m[0])-1)
    totalCost = djikstra[bottomRightCorner][0]
    print("Total cost is", totalCost)
    
# 40 small input
# 523 full input
#part1()
# small input: 315
# real input: 3022 guess is to high. Deep search approach
# real input: 2882, djikstra row by row update, also to high... hmm improper next step
# real input: 2876, djikstra with bad heap prioqueue usage (searched duplicates)... took like 30 min
# real input: 2876, djikstra with "heap prioqueue" and adding duplicates and using unvisited to pop of the duplicated... about 40 seconds
part2()