#!/usr/bin/python3

fo = open("1/input.txt", "r")
input = []
for line in fo.readlines():
    line = line.strip()
    input.append(int(line))

def part1():
    #init
    prev = input[0]
    counter = 0
    #calc
    for line in input[1:]:
        if line > prev:
            counter += 1
        prev = line
    print(counter)

def part2():
    #init
    measures = input[0:3]
    counter = 0
    #calc
    for next in input[3:]:
        measures.append(next)
        sumNewWindow = measures[-1] + measures[-2] + measures[-3]
        sumOldWindow = measures[-2] + measures[-3] + measures[-4]
        if sumNewWindow > sumOldWindow:
            counter += 1        
    print(f"{counter} from {len(measures)} measures")

#1390
part1()
#1457
part2()