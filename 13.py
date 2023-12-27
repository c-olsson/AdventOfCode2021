from collections import Counter
from collections import defaultdict

fo = open("13in.txt", "r")

#hmm using it as set but it had some very weird type issue
coordinates = {}
MAXX = 0
MAXY = 0
folds = []
for line in fo.readlines():
    line = line.strip()
    if line != "" and line[0] != 'f':
        split = line.split(",")
        l = int(split[0])
        r = int(split[1])
        coordinate = (l,r)
        coordinates[coordinate] = True
        if l > MAXX:
            MAXX = l
        if r > MAXY:
            MAXY = r
    elif line != "" and line[0] == 'f':
        split = line.split()
        inst = split[-1]
        folds.append(inst)
print(MAXX, MAXY)

def part1():
    print("Part1")
    inst = folds[0]
    split = inst.split("=")
    foldtype = split[0]
    foldvalue = int(split[1])
    newcoordinates = {}
    for c in coordinates:
        print(c)
        x = c[0]
        y = c[1]
        newx = x
        newy = y
        if foldtype == 'x' and x > foldvalue:
            newx = foldvalue - (x - foldvalue)
        elif foldtype == 'y' and y > foldvalue:
            newy = foldvalue - (y - foldvalue)
        newcoordinate = (newx,newy)
        newcoordinates[newcoordinate] = True
        
    print(len(newcoordinates))
        

def part2(coordinates, MAXX, MAXY):
    for i in range(len(folds)):
        inst = folds[i]
        split = inst.split("=")
        foldtype = split[0]
        foldvalue = int(split[1])
        newcoordinates = {}
        for c in coordinates:
            x = c[0]
            y = c[1]
            newx = x
            newy = y
            if foldtype == 'x' and x > foldvalue:
                newx = foldvalue - (x - foldvalue)
            elif foldtype == 'y' and y > foldvalue:
                newy = foldvalue - (y - foldvalue)
            newcoordinate = (newx,newy)
            newcoordinates[newcoordinate] = True
        coordinates = newcoordinates
        
        if foldtype == 'x':
            MAXX = int(MAXX/2)
        elif foldtype == 'y':
            MAXY = int(MAXY/2)
        print(len(coordinates))
    
    for y in range(MAXY):
        row = ""
        for x in range(MAXX):
            coord = (x,y)
            if coord in coordinates:
                row += "#"
            else:
                row += " "
        print(row)
            
    print("end")

# 753
#part1()
# HZLEHJRK
part2(coordinates, MAXX, MAXY)