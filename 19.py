from collections import Counter
from collections import defaultdict
from collections import deque

from scipy.spatial.transform import Rotation
import numpy as np
#from scipy.spatial import transform

fo = open("19in.txt", "r")

# 1. Get a list of scanners, each scanner has a list of its own coordinates [[x1,y1,z1],[x2,y2,z2],...]
# 2. For each scanner to scanner data comparison:
# 2.1 Check each possible transformation (translate and rotation) if it overlapps, then valid transform (min 12 overlapps)
# 2.2 combine the matching beacon to reference comparison data set
# 3. Count number of unique beacons

scanners = []
scannerId = 0
for line in fo.readlines():
    split = line.strip().split()
    if split:
        if split[0] == "---":
            coordinates = []
            scanners.append(coordinates)
        else:
            coordinates = [int(v) for v in line.strip().split(",")]                
            scanners[scannerId].append(coordinates)
    else:
        scannerId += 1
#print(scanners)

# Find out possible rotations that keeps a x,y,z orhtogonality
# Attempted to find rotaions matrixes (def np.eye(3)) to perform 'cBase @ R; 1.3 x 3.3
# R = Rotation.from_euler("XYZ",[90, 180, 0]], degrees=True).as_matrix()
# But... didnt get the combinations, ended with right hand rule with pic aid
# https://imgur.com/4fM44ew

ROTATE_TRANSFORMS = [i for i in range(24)]

def rotateCordinate(cBase, R):
    x = cBase[0]
    y = cBase[1]
    z = cBase[2]
    # Face 1 (x,.,.)
    if R == 0:
        return [x, y, z]
    elif R == 1:
        return [x, z,-y]
    elif R == 2:
        return [x,-y,-z]
    elif R == 3:
        return [x,-z, y]
    # Face 2 (.,x,.)
    elif R == 4:
        return [-y, x, z]
    elif R == 5:
        return [-z, x,-y]
    elif R == 6:
        return [ y, x,-z]
    elif R == 7:
        return [ z, x, y]
    # Face 3 (-x,.,.)
    elif R == 8:
        return [-x,-y, z]
    elif R == 9:
        return [-x,-z,-y]
    elif R == 10:
        return [-x, y,-z]
    elif R == 11:
        return [-x, z, y]
    # Face 4 (.,-x,.)
    elif R == 12:
        return [ y,-x, z]
    elif R == 13:
        return [ z,-x,-y]
    elif R == 14:
        return [-y,-x,-z]
    elif R == 15:
        return [-z,-x, y]
    # Face 5 (.,.,x)
    elif R == 16:
        return [-z, y, x]
    elif R == 17:
        return [ y, z, x]
    elif R == 18:
        return [ z,-y, x]
    elif R == 19:
        return [-y,-z, x]
    # Face 6 (.,.,-x)
    elif R == 20:
        return [ z, y,-x]
    elif R == 21:
        return [-y, z,-x]
    elif R == 22:
        return [-z,-y,-x]
    elif R == 23:
        return [ y,-z,-x]      
    else:
        assert()


def translateCordinate(cBase, T):
    cTransformed = []
    for i,t in enumerate(T):
        cTransformed.append(cBase[i] + t)
    return cTransformed

def myTransformT(T, cToTransorm):
    translatedCordinates = []
    for c in cToTransorm:
        c = translateCordinate(c, T)
        translatedCordinates.append(c)
    return translatedCordinates

def myTransformR(R, cToTransorm):
    rotatedCordinates = []
    for c in cToTransorm:
        c = rotateCordinate(c, R)
        c = [int(c[:3][0]), int(c[:3][1]), int(c[:3][2])]
        rotatedCordinates.append(c)
    return rotatedCordinates

def part1():
    print("Part1")
    
    coordinateReference = scanners[0]
    foundBeacons = set()
    for c in coordinateReference:
        foundBeacons.add(tuple(c))

    # Find a match for next scanner ref (12 or more matching beacons in any valid rotation or translate)
    foundScanners = [[0,0,0]]
    foundScannersOrder = [0]
    
    extractedOrder = [0,38,17,15,10,6,4,36,35,33,31,29,28,23,22,21,20,13,9,8,5,3,2,1,37,30]
    knownId = 1
    
    currentReference = coordinateReference
    while len(foundScannersOrder) < len(scanners):
        #for scannerId in [1,4,2,3]:#range(len(scanners)):
        for scannerId in range(len(scanners)-1,0,-1):
            if scannerId not in extractedOrder and knownId < len(extractedOrder):
                scannerId = extractedOrder[knownId]
                knownId += 1
              
            if scannerId in foundScannersOrder:
                print(f'Skip already used scanner {scannerId}')
                continue
            
            # Each scanner should find at least one other scanner it overlapps 12+ beacons on
            matchedT = 0
            matchedR = 0
            for R in ROTATE_TRANSFORMS:
                toTransformCordinates = scanners[scannerId]
                rotadedCordinates = myTransformR(R, toTransformCordinates)
                okOffsetFor12Match = 10
                for i in range(len(currentReference)-okOffsetFor12Match):
                    for j in range(len(rotadedCordinates)):#-okOffsetFor12Match
                        xCompare = rotadedCordinates[j][0]
                        yCompare = rotadedCordinates[j][1]
                        zCompare = rotadedCordinates[j][2]
                        T = [currentReference[i][0]-xCompare,
                            currentReference[i][1]-yCompare,
                            currentReference[i][2]-zCompare]
                        transformedCordinates = myTransformT(T, rotadedCordinates)
            
                        matches = 0
                        matchedCordsTransformed = []
                        matchedCordsOriginal = []
                        for index,c in enumerate(transformedCordinates):
                            if c in currentReference:
                                #print("MATCH FOUND", c)
                                matches += 1
                                #matchedCordsTransformed.append(c)
                                #matchedCordsOriginal.append(toTransformCordinates[index])
                    
                        # Check if enough overlaps to be a true transform
                        if matches >= 12:
                            print("MATCHING TRANSFORM")
                            #for t in range(len(matchedCordsTransformed)):
                                #print("Pair:")
                                #print(matchedCordsTransformed[t])
                                #print(matchedCordsOriginal[t])
                            matchedT = T
                            matchedR = R
                            origoTransformed = [foundScanners[0][0],
                                                foundScanners[0][1],
                                                foundScanners[0][2]]
                            origoTransformed = translateCordinate(origoTransformed, matchedT)
                            foundScanners.append(origoTransformed)
                            foundScannersOrder.append(scannerId)
                            #print(f"Its compared start is at {origoTransformed}")
                            
                            # Combine the newly transfered into the reference
                            for c in transformedCordinates:
                                if c not in matchedCordsTransformed:
                                    currentReference.append(c)
                                # For simpler count remove duplicates via set
                                foundBeacons.add(tuple(c))
                            #currentReference = transformedCordinates
                            #print(f"Found new match with scannerId {scannerId}")
                            print(f"Number of found scanners {len(foundScannersOrder)}")
                                
                            break
                    if matchedT:
                        break
                if matchedT:
                    break
            print(f"Done with {scannerId} after {foundScannersOrder[-1]}")
            if matchedT:
                break
            
    print(foundScanners)      
    print(len(foundBeacons))
    print("The end!")

def part2():
    print("Part2")
    
# Answer should be ans < scanner_i_len_cordinates * scanners_len , inputs is ~25*40=1000
# matchorder [0,38,17,15,10,6,4,36,35,33,31,29,28,23,22,21,20,13,9,8,5,3,2,1,37
# 483
#            [0,38,17,15,10,6,4,36,35,33,31,29,28,23,22,21,20,13,9,8,5,3,2,1,37,30,26,34,25,18,14,19,32,39,27,24,16,12,11,7]
#part1()
# Changing all the lists into set will probably speed up alot
# Secondly there was a distance rule I did not utilize, can be applied as ignore filter after rotation but before translate


#part2()
extractedScanners = [[0, 0, 0],
                    [147, 155, -1150],
                    [84, -12, -2408],
                    [-1111, -15, -1172],
                    [140, 1336, -2439],
                    [73, 2415, -2429],
                    [152, 57, -3678],
                    [25, -1081, -3562],
                    [-1069, 1334, -1335],
                    [91, 1367, -3627],
                    [-1172, 1211, -2375],
                    [130, 2535, -3661],
                    [61, 1318, -4788],
                    [-7, 2465, -4812],
                    [40, -2227, -3679],
                    [1189, 1325, -4821],
                    [43, -2315, -2539],
                    [-1133, -2226, -3620],
                    [-2428, -2405, -3634],
                    [-1166, 2471, -3551],
                    [-1125, 2470, -1239],
                    [-1230, 1218, -4909],
                    [-2296, 1210, -2351],
                    [39, -3432, -3735],
                    [30, 2407, -5973],
                    [1182, 2551, -6086],
                    [-1061, 3690, -1300],
                    [37, 3619, -1177],
                    [1176, 1237, -5981],
                    [-2300, 2420, -1172],
                    [86, 4852, -1290],
                    [51, 6081, -1202],
                    [4, 6024, -123],
                    [-1091, 4964, -52],
                    [-1201, 6159, -1249],
                    [139, 7342, -1144],
                    [-1168, 4811, -2507],
                    [10, 4959, 1],
                    [-2393, 4828, -81],
                    [-1041, 3750, -2376]]

maxManhattan = 0
for lScanner in extractedScanners:
    for rScanner in extractedScanners:
        currentManhattan = lScanner[0]-rScanner[0] + lScanner[1]-rScanner[1] + lScanner[2]-rScanner[2]
        print(currentManhattan)
        if currentManhattan > maxManhattan:
            maxManhattan = currentManhattan
print(maxManhattan)

