from collections import Counter
from collections import deque

fo = open("12in.txt", "r")

paths = {}#dict will contain sets of popssible paths
allRoutes = []#all permutations possible
for line in fo.readlines():
    line = line.strip()
    split = line.split("-")
    l = split[0]
    r = split[1]
    # add both directions to paths
    if l not in paths:
        children = set()
        children.add(r)
        paths[l] = children
    else:
        if r not in paths[l]:
            paths[l].add(r)
    if r not in paths:
        children = set()
        children.add(l)
        paths[r] = children
    else:
        if l not in paths[r]:
            paths[r].add(l)
for p in paths["start"]:
    #filter away start as possible connection to go back to
    paths[p].remove("start")
#filter away paths back from end
paths["end"] = set()
#print(paths)

      
def rec(currentCave, route):
    #create new copy routes for children and pass along
    #go deep until end leafs (allowing BIG "return" children)
    route.append(currentCave)
    children = paths[currentCave]
    for c in children:
        newRoute = route.copy()
        if c == "end":
            newRoute.append(c)
            allRoutes.append(newRoute)
        elif c.isupper():
            rec(c, newRoute)
        elif c.islower() and c not in route:
            rec(c, newRoute)
        elif c.islower() and c in route:
            #ignore dead-end
            continue
        else:
            assert()

def rec2(currentCave, route):
    #one small cave can be visited twice, but only one -> more permutations
    route.append(currentCave)
    children = paths[currentCave]
    for c in children:
        newRoute = route.copy()
        if c == "end":
            newRoute.append(c)
            allRoutes.append(newRoute)
            #print("Found end #", len(allRoutes))
        elif c.isupper():
            rec2(c, newRoute)
        elif c.islower() and c not in route:
            rec2(c, newRoute)
        elif c.islower():#always true
            #if only uniqly lowers, allow one last more small cave visit
            uniqueLower = set()
            lower = []
            for sIndex in range(1, len(route)):
                s = route[sIndex]
                if s.islower():
                    uniqueLower.add(s)
                    lower.append(s)
            if len(uniqueLower) == len(lower):
                rec2(c, newRoute)
   

def part1():
    #find all permutations of all starts
    route = []
    firstCave = "start"
    rec(firstCave, route)

    countEnds = 0
    for finalRoute in allRoutes:
        if finalRoute[-1] == "end":
            print(finalRoute)
            countEnds += 1
    print(countEnds)

def part2():
    route = []
    firstCave = "start"
    rec2(firstCave, route)

    countEnds = 0
    for finalRoute in allRoutes:
        if finalRoute[-1] == "end":
            #print(finalRoute)
            countEnds += 1
    print(countEnds)

#3497
#part1()
#93686
part2()