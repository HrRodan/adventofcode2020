from typing import List, Tuple
from numba import njit

with open('input.txt') as file:
    starting_numbers = tuple([int(x) for x in file.readline().strip().split(',')])

@njit(fastmath = True)
def number_at_turn(number_turns: int, start_nums: Tuple[int]):
    last_turn_spoken = {x: i + 1 for i, x in enumerate(start_nums)}
    last_turn_spoken_get = last_turn_spoken.get
    number_spoken = start_nums[-1]
    for turn in range(len(start_nums) + 1, number_turns + 1):
        if number_spoken not in last_turn_spoken:
            next_number = 0
        else:
            next_number = turn - 1 - last_turn_spoken_get(number_spoken)
        last_turn_spoken[number_spoken] = turn - 1
        number_spoken = next_number
    return number_spoken


# part 1
print(number_at_turn(2020, starting_numbers))

# part 2
print(number_at_turn(30000000, starting_numbers))