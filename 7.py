
fo = open("7in.txt", "r")

inputString = []
for line in fo.readlines():
    inputString = line.split(",")
input = []
for i in inputString:
    input.append(int(i))
#print(input)

MIN = min(input)
MAX = max(input)
print(MIN,MAX)

def part1():    
    fuels = []
    for r in range(MIN,1+MAX):
        fuel = 0
        for c in input:
            fuel += abs(r-c)
        #print("Step", r, fuel)
        fuels.append(fuel)
    print(min(fuels))

def part2():
    fuels = []
    currentMin = 1e9
    for r in range(MIN,1+MAX):
        fuel = 0
        #print("Step", r, fuel)
        for c in input:
            delta = abs(r-c)
            # Aritmetic sum formula for 1+2+3..n where n=delta. Always looping 1 to n is much slower, ~n/2 more operations disreg mult.
            fuel += int(delta*(1+delta)/2)
            #print("delta", delta, fuel)
        fuels.append(fuel)
        if currentMin > min(fuels):
            currentMin = min(fuels)
        else:
            print("local min reached", currentMin)
            break

#349357
part1()
#96708205
part2()