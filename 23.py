from collections import Counter
from collections import defaultdict
from collections import deque
from scipy.spatial.transform import Rotation
import numpy as np

fo = open("23ins.txt", "r")

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
print(input)



def part1():
    print("Part1")
    # Initially 7 possible moves for each 4 amphi, always 4 top amphi to be choosen
    # second step depends on first, example has b 2, c 5, c 0, d 4 valid moves
    
    print("end")


def part2():
    print("Part2")
 
    print("end")


# By hand, pen and paper, 13495
#part1()

# semi by hand, https://amphipod.net/
# 47787 is to low, tried out some ghost to get initial guess
# 53767, need to move both D to left, empying the third colum first, getting C and B done
#part2()