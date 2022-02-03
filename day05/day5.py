from itertools import product
from typing import Tuple

with open('input.txt', newline='\n') as file:
    passes = [line.strip() for line in file.readlines()]

LOW_HIGH_MAP = {
    'B':'h',
    'F':'l',
    'L':'l',
    'R':'h'
}

ROWS = (0,127)
COLUMS = (0,7)

def find_seat(range: Tuple[int, int], low_high: str):
    low, high = range
    diff = int((high - low + 1) / 2)
    if low_high == 'h':
        return low + diff, high
    elif low_high == 'l':
        return low, high - diff
    else:
        raise ValueError

def find_final_position(seat : str):
    row = ROWS
    column = COLUMS
    for letter in seat[0:7]:
        row = find_seat(row, LOW_HIGH_MAP[letter])
    for letter in seat[7:]:
        column = find_seat(column, LOW_HIGH_MAP[letter])
    return row[0], column[0]

def get_uid(position : Tuple[int, int]):
    return position[0]*8 + position[1]

result = max(get_uid(find_final_position(p)) for p in passes)

print(result)

#part 2

possible_seats = set(product(range(128), range(8)))
id_occupied = set()
for p in passes:
    final_position = find_final_position(p)
    id_occupied.add(get_uid(final_position))
    possible_seats.remove(find_final_position(p))

for s in possible_seats:
    uid = get_uid(s)
    if uid-1 in id_occupied and uid+1 in id_occupied:
        print(uid)
