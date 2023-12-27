from collections import defaultdict

fo = open("6in.txt", "r")


inputString = []
for line in fo.readlines():
    inputString = line.split(",")
input = []
for i in range(len(inputString)):
    input.append(int(inputString[i]))
print(input)

RESET_DAY = 6
NEW_DAY = 8

def part1():
    fishes = input.copy()
    for d in range(1,81):
        addNumFishes = 0
        for i in range(len(fishes)):
            fishes[i] -= 1
            if fishes[i] == -1:
                fishes[i] = RESET_DAY
                addNumFishes += 1
                
        for a in range(addNumFishes):
            fishes.append(NEW_DAY)
        print("Day", d, fishes)
    print(len(fishes))

def part2():
    #init
    fishes = [0,0,0,0,0,0,0,0,0]
    for fish in input:
        fishes[fish] += 1
    #based on day batches of fishes (way to long list other wise), decrease age as well reborn and birth
    for d in range(1,257):
        amountOfNewFishes = fishes[0]
        for i in range(len(fishes)):
            if i != 0:
                fishes[i-1] = fishes[i]
        # new babies sets to max day
        fishes[NEW_DAY] = amountOfNewFishes
        # but reborn fishes accumalate on reset day with young once
        fishes[RESET_DAY] += amountOfNewFishes
        acc = 0
        for count in fishes:
            acc += count
        print("Day", d, fishes, "Sum of fishes", acc)
#395627
#part1()
#1767323539209
part2()