from collections import Counter
from collections import defaultdict

fo = open("14in.txt", "r")

polymMatcher = {}
startPolym = fo.readline()
startPolym = startPolym.strip()
polym = []
for p in startPolym:
    polym.append(p)
fo.readline()

for line in fo.readlines():
    line = line.strip()
    l,r = line.split(" -> ")
    polymMatcher[l] = r
#print(polym)
#print(polymMatcher)

def part1():
    print("Part1")
    for iteration in range(10):
        index = 0
        for _ in range(len(polym)-1):
            key = polym[index] + polym[index+1]
            toInsert = polymMatcher[key]
            polym.insert(index+1, toInsert)
            index += 2
        
    charCounter = Counter()
    charCounter.update(polym)
    sortByCount = charCounter.most_common()
    maxChar = sortByCount[0]
    minChar = sortByCount[-1]
    res = maxChar[1] - minChar[1]
    print(res)
        

MAXDEPTH = 10
#worked as bad as list apparently
def goDeep(c, currentDepth, currentKey):        
    if currentDepth < MAXDEPTH:
        #each depth and key will generate to new once with its neighbour
        newChar = polymMatcher[currentKey]
        c.update([newChar])
        newKey1 = currentKey[0] + newChar
        newKey2 = newChar + currentKey[1]
        goDeep(c, currentDepth+1, newKey1)
        goDeep(c, currentDepth+1, newKey2)
    else:
        return

def part2Bad():
    print("Part2Bad")
    # With 40 iterations a list of polym is not duable
    # lets do recursive to given depth and keep count directly
    # ...it also didnt cut it, will be soo many threads created
    charCounter = Counter()
    charCounter.update(polym)
    depth = 0
    for i in range(len(polym)-1):
        key = polym[i] + polym[i+1]
        goDeep(charCounter, depth, key)
        print("Polym", i+1, "of", len(polym)-1, "done")
        
    sortByCount = charCounter.most_common()
    maxChar = sortByCount[0]
    minChar = sortByCount[-1]
    res = maxChar.value() - minChar.value()
    print(res)

def part2():
    print("Part2")
    
    #init dict of keys, not poly! Wont afford keeping track of order
    keyCounter = Counter()
    for i in range(len(polym)-1):
        key = polym[i]+polym[i+1]
        keyCounter.update([key])
    
    #each key will trigger two new keys each iteration, then order is not important
    #like a bfs, breadth search first due to all combinations before going deeper
    for iteration in range(40):
        # fresh one due to parentKey wont exist anymore
        # also the values will be big, but the size of dict wont
        newKeyCounter = Counter()
        for key in keyCounter:
            newPoly = polymMatcher[key]
            newKey1 = key[0] + newPoly
            newKey2 = newPoly + key[1]
            #multiple entries, as many as occurence of key
            amountOfParentKey = keyCounter[key]
            newKeyCounter[newKey1] += amountOfParentKey
            newKeyCounter[newKey2] += amountOfParentKey
        # init for next iteration
        keyCounter = newKeyCounter
        print(iteration)
                     
    # count from result dict the max-min
    charCount = Counter()
    # add last due to checking just firstKey and dont know order 
    charCount.update(polym[-1])
    for key in keyCounter:
        firstPolyInKey = key[0]
        charCount[firstPolyInKey] += keyCounter[key]
        
    sortByCount = charCount.most_common()
    res = sortByCount[0][1]-sortByCount[-1][1]
    print(res)

# 2587
#part1()
# 3318837563123
part2()