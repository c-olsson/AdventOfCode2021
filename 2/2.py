
fo = open("2/input.txt", "r")
instructions = []
values = []
for line in fo.readlines():
    line = line.strip()
    inst, value = line.split()
    instructions.append(inst)
    values.append(int(value))

def part1():
    depth = 0
    forward = 0

    for i in range(0,len(instructions)):
        inst = instructions[i]
        value = values[i]
        if inst == "forward":
            forward += value
        elif inst == "down":
            depth += value
        else:
            depth -= value
    print(forward*depth, "for", forward, depth)

def part2():
    depth = 0
    forward = 0
    aim = 0

    for i in range(0,len(instructions)):
        inst = instructions[i]
        value = values[i]
        if inst == "forward":
            forward += value
            depth += aim*value
        elif inst == "down":
            aim += value
        elif inst == "up":
            aim -= value
    print(forward*depth, "for", forward, depth, aim)


#1962940
part1()
#1813664422
part2()