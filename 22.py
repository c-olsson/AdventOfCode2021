from collections import Counter
from collections import defaultdict
from collections import deque
from scipy.spatial.transform import Rotation
import numpy as np

fo = open("22in.txt", "r")

input = []
inputBoolean = []
for line in fo.readlines():
    boolean, ranges = line.strip().split()
    inputBoolean.append(boolean)
    
    xr,yr,zr = ranges.split(",")
    xlow,xmax = xr.split("..")
    ylow,ymax = yr.split("..")
    zlow,zmax = zr.split("..")
    input.append([[xlow[2:],xmax],[ylow[2:],ymax],[zlow[2:],zmax]])
#print(input)

# Starts with all off

VOLUMES_PART1 = []
def part1():
    global VOLUMES_PART1
    print("Part1")
    # Only boarders -50<= x,y,z <= 50 is of interest for now
    cube = set()
    for onOffIndex,row in enumerate(input):
        XMIN = int(row[0][0])
        XMAX = int(row[0][1])+1
        YMIN = int(row[1][0])
        YMAX = int(row[1][1])+1
        ZMIN = int(row[2][0])
        ZMAX = int(row[2][1])+1
        
        # input could actually visibly be filtered, just took subpart of it, no need for +-50 guards
        if -50<=XMIN and XMAX<=50 and -50<=YMIN and YMAX<=50 and -50<=ZMIN and ZMAX<=50:
            for x in range(XMIN,XMAX):
                for y in range(int(row[1][0]),int(row[1][1])+1):
                    for z in range(int(row[2][0]),int(row[2][1])+1):
                        currentTuple = (x,y,z)
                        if inputBoolean[onOffIndex] == 'on':
                            #if -50<=x<=50 and -50<=y<=50 and -50<=z<=50:
                            cube.add(currentTuple)
                        else:
                            if currentTuple in cube:
                                cube.remove(currentTuple)
        #print(f"It {onOffIndex}, len {len(cube)}")
        VOLUMES_PART1.append(len(cube))
    print(f"{VOLUMES_PART1[-1]}")
    print("end")


def calculateSmallCubes(cube):
    diffx = cube[0][0] - cube[1][0]
    diffy = cube[0][1] - cube[1][1]
    diffz = cube[0][2] - cube[1][2]
    # Invalid cube if any has (0,0), so 1 width at origa, not in input
    inOrigo = cube[0][0] == 0 and cube[1][0] == 0 or cube[0][1] == 0 and cube[1][1] or cube[0][2] == 0 and cube[1][2]
    if inOrigo and (diffx == 0 or diffy == 0 or diffz == 0):
        return 0
    # 1 + diff, need to include the boarder
    widthx = 1 + abs(diffx)
    widthy = 1 + abs(diffy)
    height = 1 + abs(diffz)
    res = widthx * widthy * height
    return res

def getOneDimRanges(c1, c2):
    # Return c1's overlapp on c2
    c1Min = c1[0]
    c1Max = c1[1]
    c2Min = c2[0]
    c2Max = c2[1]
    retOverlapRange = (0,0)
    retSplitRanges = []
    retCase = ""
    # Case 1 no overlap left or right
    if c1Max < c2Min or c1Min > c2Max: 
        retCase = "none"
        retOverlapRange = (0,0)
        retSplitRanges = []
    # Case 2 overlap left side
    elif c1Min <= c2Min and c1Max <= c2Max:
        retCase = "left"
        retOverlapRange = (c2Min,c1Max)
        if c1Max == c2Max:
            retSplitRanges = []
        else:
            retSplitRanges.append((c1Max+1,c2Max))
    # Case 3 overlap right side
    elif c1Max >= c2Max and c1Min >= c2Min:
        retCase = "right"
        retOverlapRange = (c1Min,c2Max)
        if c1Min == c2Min:
            retSplitRanges = []
        else:
            retSplitRanges.append((c2Min,c1Min-1))
    # Case 4 full overlap inside
    elif c1Min > c2Min and c1Max < c2Max:
        retCase = "inside"
        retOverlapRange = (c1Min, c1Max)
        retSplitRanges.append((c2Min,c1Min-1))
        retSplitRanges.append((c1Max+1,c2Max))
    # Case 5 full overlap outside, new is bigger on both side
    elif c1Max >= c2Max and c1Min <= c2Min:
        retCase = "eaten"
        retOverlapRange = (c2Min, c2Max)
        retSplitRanges = []
    else:
        assert()
    #print("Case:",retCase)
    return retCase, retOverlapRange, retSplitRanges

def overlapHandling(cube, oldCube):
    # All dimensions needs to overlapp for a cube to be noted as overlap
    caseX,oRangesX,sRangesX = getOneDimRanges((cube[0][0], cube[1][0]), (oldCube[0][0], oldCube[1][0]))
    caseY,oRangesY,sRangesY = getOneDimRanges((cube[0][1], cube[1][1]), (oldCube[0][1], oldCube[1][1]))
    caseZ,oRangesZ,sRangesZ = getOneDimRanges((cube[0][2], cube[1][2]), (oldCube[0][2], oldCube[1][2]))
    
    if (caseX == 'none' or caseY == 'none' or caseZ == 'none'):
        return False,[]
    elif not sRangesX and not sRangesY and not sRangesZ:
        #caseX == 'eaten' and caseY == 'eaten' and caseZ == 'eaten'):
        return True,[]
    # Create up to 6 splited cubes, take account for variations of what dimension has what overlap
    didOverlap = True
    splitedCubes = []
    # Case: 1, 2 x-dim
    if sRangesX and not sRangesY and not sRangesZ:
        for i in range(len(sRangesX)):
            splitedCubes.append(((sRangesX[i][0],oRangesY[0],oRangesZ[0]),
                                (sRangesX[i][1],oRangesY[1],oRangesZ[1])))
    # Case: 1, 2 y-dim
    elif not sRangesX and sRangesY and not sRangesZ:
        for i in range(len(sRangesY)):
            splitedCubes.append(((oRangesX[0],sRangesY[i][0],oRangesZ[0]),
                                 (oRangesX[1],sRangesY[i][1],oRangesZ[1])))
    # Case: 1, 2 z-dim
    elif not sRangesX and not sRangesY and sRangesZ:
        for i in range(len(sRangesZ)):
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[i][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[i][1])))
    # Case: 2, 3, 4 x-dim and y-dim
    elif sRangesX and sRangesY and not sRangesZ:
        if len(sRangesX) == 1 and len(sRangesY) == 1:
            splitedCubes.append(((sRangesX[0][0],oldCube[0][1],oRangesZ[0]),
                                 (sRangesX[0][1],oldCube[1][1],oRangesZ[1])))
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oRangesZ[0]),
                                 (oRangesX[1],sRangesY[0][1],oRangesZ[1])))
        elif len(sRangesX) == 2 and len(sRangesY) == 1:
            splitedCubes.append(((sRangesX[0][0],oldCube[0][1],oRangesZ[0]),
                                 (sRangesX[0][1],oldCube[1][1],oRangesZ[1])))
            splitedCubes.append(((sRangesX[1][0],oldCube[0][1],oRangesZ[0]),
                                 (sRangesX[1][1],oldCube[1][1],oRangesZ[1])))
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oRangesZ[0]),
                                 (oRangesX[1],sRangesY[0][1],oRangesZ[1])))
        elif len(sRangesX) == 1 and len(sRangesY) == 2:
            splitedCubes.append(((oldCube[0][0],sRangesY[0][0],oRangesZ[0]),
                                 (oldCube[1][0],sRangesY[0][1],oRangesZ[1])))
            splitedCubes.append(((oldCube[0][0],sRangesY[1][0],oRangesZ[0]),
                                 (oldCube[1][0],sRangesY[1][1],oRangesZ[1])))
            splitedCubes.append(((sRangesX[0][0],oRangesY[0],oRangesZ[0]),
                                 (sRangesX[0][1],oRangesY[1],oRangesZ[1])))
        elif len(sRangesX) == 2 and len(sRangesY) == 2:
            splitedCubes.append(((oldCube[0][0],sRangesY[0][0],oRangesZ[0]),
                                 (oldCube[1][0],sRangesY[0][1],oRangesZ[1])))
            splitedCubes.append(((oldCube[0][0],sRangesY[1][0],oRangesZ[0]),
                                 (oldCube[1][0],sRangesY[1][1],oRangesZ[1])))
            splitedCubes.append(((sRangesX[0][0],oRangesY[0],oRangesZ[0]),
                                 (sRangesX[0][1],oRangesY[1],oRangesZ[1])))
            splitedCubes.append(((sRangesX[1][0],oRangesY[0],oRangesZ[0]),
                                 (sRangesX[1][1],oRangesY[1],oRangesZ[1])))
        else:
            assert()
    # Case: 2, 3, 4 y-dim and z-dim
    elif not sRangesX and sRangesY and sRangesZ:
        if len(sRangesZ) == 1 and len(sRangesY) == 1:
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
        elif len(sRangesZ) == 2 and len(sRangesY) == 1:
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[1][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[1][1])))
        elif len(sRangesZ) == 1 and len(sRangesY) == 2:
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[1][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
        elif len(sRangesZ) == 2 and len(sRangesY) == 2:
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[1][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[1][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[1][1])))
        else:
            assert()
    # Case: 2, 3, 4 x-dim and z-dim
    elif sRangesX and not sRangesY and sRangesZ:
        if len(sRangesX) == 1 and len(sRangesZ) == 1:
            splitedCubes.append(((sRangesX[0][0],oRangesY[0],oldCube[0][2]),
                                 (sRangesX[0][1],oRangesY[1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
        elif len(sRangesX) == 2 and len(sRangesZ) == 1:
            splitedCubes.append(((sRangesX[0][0],oRangesY[0],oldCube[0][2]),
                                 (sRangesX[0][1],oRangesY[1],oldCube[1][2])))
            splitedCubes.append(((sRangesX[1][0],oRangesY[0],oldCube[0][2]),
                                 (sRangesX[1][1],oRangesY[1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
        elif len(sRangesX) == 1 and len(sRangesZ) == 2:
            splitedCubes.append(((sRangesX[0][0],oRangesY[0],oldCube[0][2]),
                                 (sRangesX[0][1],oRangesY[1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[1][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[1][1])))
        elif len(sRangesX) == 2 and len(sRangesZ) == 2:
            splitedCubes.append(((sRangesX[0][0],oRangesY[0],oldCube[0][2]),
                                 (sRangesX[0][1],oRangesY[1],oldCube[1][2])))
            splitedCubes.append(((sRangesX[1][0],oRangesY[0],oldCube[0][2]),
                                 (sRangesX[1][1],oRangesY[1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[1][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[1][1])))
        else:
            assert()
    # Case: 3, 4, 5, 6 x-dim and y-dim and z-dim
    elif sRangesX and sRangesY and sRangesZ:
        if len(sRangesX) == 1 and len(sRangesY) == 1 and len(sRangesZ) == 1:
            splitedCubes.append(((sRangesX[0][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[0][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
        # 4 splitted cubes needed
        elif len(sRangesX) == 2 and len(sRangesY) == 1 and len(sRangesZ) == 1:
            splitedCubes.append(((sRangesX[0][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[0][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((sRangesX[1][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[1][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
        elif len(sRangesX) == 1 and len(sRangesY) == 2 and len(sRangesZ) == 1:
            splitedCubes.append(((sRangesX[0][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[0][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[1][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
        elif len(sRangesX) == 1 and len(sRangesY) == 1 and len(sRangesZ) == 2:
            splitedCubes.append(((sRangesX[0][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[0][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[1][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[1][1])))
        # 5 splited cubes needed now
        elif len(sRangesX) == 2 and len(sRangesY) == 2 and len(sRangesZ) == 1:
            splitedCubes.append(((oldCube[0][0],sRangesY[0][0],oldCube[0][2]),
                                 (oldCube[1][0],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oldCube[0][0],sRangesY[1][0],oldCube[0][2]),
                                 (oldCube[1][0],sRangesY[1][1],oldCube[1][2])))
            splitedCubes.append(((sRangesX[0][0],oRangesY[0],oldCube[0][2]),
                                 (sRangesX[0][1],oRangesY[1],oldCube[1][2])))
            splitedCubes.append(((sRangesX[1][0],oRangesY[0],oldCube[0][2]),
                                 (sRangesX[1][1],oRangesY[1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
        elif len(sRangesX) == 1 and len(sRangesY) == 2 and len(sRangesZ) == 2:
            splitedCubes.append(((sRangesX[0][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[0][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[1][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[1][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[1][1])))
        elif len(sRangesX) == 2 and len(sRangesY) == 1 and len(sRangesZ) == 2:
            splitedCubes.append(((sRangesX[0][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[0][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((sRangesX[1][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[1][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[1][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[1][1])))
        # Maximum 6 cuboids split
        elif len(sRangesX) == 2 and len(sRangesY) == 2 and len(sRangesZ) == 2:
            splitedCubes.append(((sRangesX[0][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[0][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((sRangesX[1][0],oldCube[0][1],oldCube[0][2]),
                                 (sRangesX[1][1],oldCube[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[0][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[0][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],sRangesY[1][0],oldCube[0][2]),
                                 (oRangesX[1],sRangesY[1][1],oldCube[1][2])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[0][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[0][1])))
            splitedCubes.append(((oRangesX[0],oRangesY[0],sRangesZ[1][0]),
                                 (oRangesX[1],oRangesY[1],sRangesZ[1][1])))
        else:
            assert()  
    else:
        assert()
    
    # Add a volume check for debugging
    # always true is oldCube == overlap + n*splited
    oldVolume = calculateSmallCubes(oldCube)
    newVolume = calculateSmallCubes(((oRangesX[0],oRangesY[0],oRangesZ[0]),
                                     (oRangesX[1],oRangesY[1],oRangesZ[1])))
    for sc in splitedCubes:
        newVolume += calculateSmallCubes(sc)
    if oldVolume != newVolume:
        assert()
    
    return didOverlap, splitedCubes


def part2():
    global ANS_PART1
    print("Part2")
    cubes = []
    #cubes = set()
    row = input[0]
    lcbInit = (int(row[0][0]), int(row[1][0]), int(row[2][0]))
    hcbInit = (int(row[0][1]), int(row[1][1]), int(row[2][1]))
    # First is always an on
    cubes.append((lcbInit,hcbInit))
        
    for index,row in enumerate(input[1:len(input)]):
        lowerCornerBound = (int(row[0][0]), int(row[1][0]), int(row[2][0]))
        higherCornerBound = (int(row[0][1]), int(row[1][1]), int(row[2][1]))
        newCube = (lowerCornerBound, higherCornerBound)

        # Repeat until no overlaps with needed splits are found
        # Relying on previous state of no overlapps, thus unique overlaps if found, can utilize copy for read and manipulate once
        cubesCopy = cubes.copy()
        for oldCube in cubesCopy:
            overlaped, cubesToAdd = overlapHandling(newCube,oldCube)
            if overlaped:
                #print("Overlaped, do splitting!")
                cubes.remove(oldCube)
                for splitedCube in cubesToAdd:
                    cubes.append(splitedCube)

        # Always add an on, if off or splitted, already handled by replacing old cube(s) into multiple smaller versions
        if inputBoolean[index+1] == 'on':
            cubes.append(newCube)
        #print("Index:", index)
                    
    numOfCubes = 0
    for cube in cubes:
        numOfCubes += calculateSmallCubes(cube)
        #if VOLUMES_PART1[index+1] != numOfCubes:
        #    assert()
    
    #print("Part 1:",VOLUMES_PART1[-1])
    print("Part 2:",numOfCubes)
    print("end")


# 50**3=125 000 is possible max, doable with grid map... use set of tuples (x,y,z) for each 1x1x1 for now
# example 590784. Real inputs first 20 was only need, rest outside init area, 580810
part1()

# hmm, billions of 1x1x1 cuboids, grid map or set not doable, cant iterate that
# Could do cube splits, will be up to 6 splitted cuboids
# part 2 inner example is 474140
# real input 1265621119006734, 7 seconds execution time whit list
# cubes are unique so could switch to set?
part2()