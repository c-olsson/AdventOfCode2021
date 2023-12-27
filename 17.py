from collections import Counter
from collections import deque

fo = open("17in.txt", "r")

line = fo.readline()
split = line.strip().split()
XR = split[2][2:-1].split("..")
MINX = int(XR[0])
MAXX = int(XR[1])
YR = split[3][2:].split("..")
MINY = int(YR[0])
MAXY = int(YR[1])

X = [i for i in range(1,MAXX+2)]
Y = [i for i in range(MINY-2,MAXX)]
#use set it can be inside range multiple times, just count one of them
initPairs = set()
peakYs = []
for initx in X:
    for inity in Y:
        dx = initx
        dy = inity
        x,y = 0,0
        iteration = 0            
        peakY = 0
        while y > MINY:
            iteration += 1
            x += dx
            y += dy
            if dx > 0:
                dx -= 1
            elif dx == 0:
                dx = 0
            else:
                assert()
            dy -= 1
            if y > peakY:
                peakY = y
            if MINX <= x <= MAXX and MINY <= y <= MAXY:
                #print("INSIDE with start", (initx,inity), "and peak", peakY)
                initPairs.add((initx,inity))
                peakYs.append(peakY)
            #print(iteration)
    
# 5565
print("Part1")
print(max(peakYs))
# 2118
print("Part2")
print(len(initPairs))