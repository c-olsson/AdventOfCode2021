from collections import Counter
from collections import deque

fo = open("10in.txt", "r")

input = []
for line in fo.readlines():
    line = line.strip()
    input.append(line)
#print(input)

LEFT_CHAR = {'(': ')', '[': ']', '{': '}', '<': '>'}
RIGHT_CHAR = {')', ']', '}', '>'}
ERROR_SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}

def part1():
    finds = []
    for line in input:
        expects = deque()
        for c in line:
            if c in LEFT_CHAR:
                expects.append(LEFT_CHAR[c])
            else:
                currentExpect = expects.pop()
                if c != currentExpect:
                    print("Expected", currentExpect, "but found", c, "instead")
                    finds.append(c)
                    break
    
    res = 0
    for f in finds:
        res += ERROR_SCORE[f]
    print(res)

INC_SCORE = {')': 1, ']': 2, '}': 3, '>': 4}

def part2():
    completions = []
    for line in input:
        expects = deque()
        breaked = False
        for c in line:
            if c in LEFT_CHAR:
                expects.append(LEFT_CHAR[c])
            else:
                currentExpect = expects.pop()
                if c != currentExpect:
                    #print("Expected", currentExpect, "but found", c, "instead")
                    breaked = True
                    expects.append(currentExpect)
                    break
        completion = []
        if not breaked:
            while expects:
                completion.append(expects.pop())
            completions.append(completion)
    
    scores = []
    for completion in completions:
        score = 0
        for c in completion:
            score = score*5
            score += INC_SCORE[c]
        scores.append(score)
        
    scores.sort()
    print(scores[int(len(scores)/2)])

#271245
#part1()
#1685293086
part2()