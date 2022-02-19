import math
import re
from typing import Tuple

import numpy as np

with open('input_test.txt') as file:
    movements_raw = [line.strip() for line in file.readlines()]

SIN60 = math.sin(math.radians(60))
SIN30 = 0.5

move2d = {
    'e': (1, 0),
    'w': (-1, 0),
    'ne': (SIN30, SIN60),
    'se': (SIN30, -SIN60),
    'sw': (-SIN30, -SIN60),
    'nw': (-SIN30, SIN60)
}

movements = [[move2d[d] for d in re.findall(r'(e|w|ne|nw|se|sw)', line)] for line in movements_raw]

final_position = np.array([np.round(np.sum(movement, axis=0), 10) for movement in movements])  #

unique, counts = np.unique(final_position, return_counts=True, axis=0)

sum_black = (counts % 2).sum()

print(sum_black)


# part 2
def neighbour_tiles(tile_in: Tuple):
    for value in move2d.values():
        yield round(tile_in[0] + value[0], 10), round(tile_in[1] + value[1], 10)


tiles = {}
# initialize tiles
for tile in unique[counts % 2 == 1]:
    tiles[tuple(tile)] = 1
