from collections import Counter
from collections import defaultdict
from collections import deque
from scipy.spatial.transform import Rotation
import numpy as np

# Example
PLAYER_POS = [4, 8]
# My input
#PLAYER_POS = [6, 3]

BOARD = [10,1,2,3,4,5,6,7,8,9]
# range 1-100
DICE_ROLLS = 0

def rollDice(d):
    global DICE_ROLLS
    ret = 0
    for i in range(3):
        d = (d+1) % 101
        if d == 0:
            d = 1
        ret += d
        #print("DICE",d)
        DICE_ROLLS += 1
    return ret,d

def part1():
    print("Part1")
    global PLAYER_POS
    DICE = 0
    PLAYER_SCORE = [0, 0]
    
    turn = 0
    player1Turn = True
    while PLAYER_SCORE[0] < 1000 and PLAYER_SCORE[1] < 1000:
        value, DICE = rollDice(DICE)
        boardIndex = (PLAYER_POS[turn] + value) % len(BOARD)
        PLAYER_POS[turn] = boardIndex
        boardValue = BOARD[boardIndex]
        PLAYER_SCORE[turn] += boardValue
        
        if PLAYER_SCORE[turn] > 980:
            if player1Turn:
                print("Player1 turn")
            else:
                print("Player2 turn")
            print(f"dsum {value} bv {boardValue} ps {PLAYER_SCORE[turn]}")

        player1Turn = not player1Turn
        if player1Turn:
            turn = 0
        else:
            turn = 1
    
    result = 0
    if PLAYER_SCORE[0] >= 1000:
        result = PLAYER_SCORE[1] * DICE_ROLLS
    else:
        result = PLAYER_SCORE[0] * DICE_ROLLS
    print(result)

def part2():
    print("Part2")
    # First players turn only
    # First roll -> 3 universe copies with 1,2,3 dice values
    # Second rolls, each universes gets 3 more -> 9 universes with 1+1,1+2,1+3 and 2+1,2+2,2+3 and 3+1,3+2,3+3
    # Third rolls -> 27 universes... it goes fast, 3*num_rolls!
    # Game ends at any players score >= 21... how many uniquly events can provide that, permutations time
    
    # Example fastest win, several variations possible
    # start(7) => 7->8->9->*10->3->6->*9->2->5->*8 => scores 10->19->27 done in 3 turns
    # Example slowest win, several variations possible
    # start(7) => 7->9->10->*1->2->3->*4->7->10->*1->2->3->*4->7->10->*1...  => scores 1+4+1+4+1+4+1+4+1 done in 9 turns
    # Conclusion, player 2 has some room to catch up
    
    # Possible variations of 3 dice throws... values         3 4 5 6 7 8 9
    #                       27 outcomes from 3 throws as     1 3 6 7 6 3 1
    print("end")

dicesSum = defaultdict(int)
for d1 in [1,2,3]:
    for d2 in [1,2,3]:
        for d3 in [1,2,3]:
            sum = d1+d2+d3
            dicesSum[sum] += 1
print(dicesSum)

# dynamic programming!
# brute force + memoization.
# how many possible game states are there?
# 10 options for p1, 10 options for p2, 21 options for s1, 21 options for s2 -> 10*10*21*21 ~ 40,000
# total running time ~ state space * non-recursive time for one call ~ 40e3 * 27 ~ 120e4 = ~1M
p1 = PLAYER_POS[0]-1
p2 = PLAYER_POS[1]-1
DP = {} # game state -> answer for that game state
def count_win(p1, p2, s1, s2):
  # Given that A is at position p1 with score s1, and B is at position p2 with score s2, and A is to move,
  # return (# of universes where player A wins, # of universes where player B wins)
  if s1 >= 21:
    return (1,0)
  if s2 >= 21:
    return (0, 1)
  if (p1, p2, s1, s2) in DP:
    return DP[(p1, p2, s1, s2)]
  ans = (0,0)
  for d1 in [1,2,3]:
    for d2 in [1,2,3]:
      for d3 in [1,2,3]:
        new_p1 = (p1+d1+d2+d3)%10
        new_s1 = s1 + new_p1 + 1

        x1, y1 = count_win(p2, new_p1, s2, new_s1)
        ans = (ans[0]+y1, ans[1]+x1)
  DP[(p1, p2, s1, s2)] = ans
  return ans

result = count_win(p1, p2, 0, 0)
print(max(result))
print("end")

# 752745
#part1()
# omg, thats alot of universes. 
# Example Player 1 (start 4) wins 444 356 092 776 315
#      vs Player 2 (start 8) wins 341 960 390 180 808
# 17512 for DP len, 309196008717909
#part2()