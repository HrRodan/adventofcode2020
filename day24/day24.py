import functools
import math
import re
from typing import Tuple

import numpy as np
from numba import njit

with open('input.txt') as file:
    movements_raw = [line.strip() for line in file.readlines()]

SIN60 = round(math.sin(math.radians(60)),5)
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

final_position = np.array([np.round(np.sum(movement, axis=0), 5) for movement in movements])  #

unique, counts = np.unique(final_position, return_counts=True, axis=0)

sum_black = (counts % 2).sum()

print(sum_black)


# part 2

@functools.cache
def neighbour_tiles(tile_in: Tuple):
    return [(round(tile_in[0] + value_[0],5), round(tile_in[1] + value_[1], 5)) for value_ in move2d.values()]
    # for value_ in move2d.values():
    #     yield round(tile_in[0] + value_[0], 10), round(tile_in[1] + value_[1], 10)


tiles = {}
# initialize tiles
for tile in unique[counts % 2 == 1]:
    tiles[tuple(tile)] = True

NUMBER_DAYS = 100

#@njit
def answer(tiles_in : dict):
    for d in range(NUMBER_DAYS):
        #print(d)
        # pad hex array
        tiles_to_add = {
            new_tile
            for tile in tiles_in
            for new_tile in neighbour_tiles(tile)
            if new_tile not in tiles_in
        }

        for t in tiles_to_add:
            tiles_in[t] = False

        tiles_new = tiles_in.copy()
        tiles_get = tiles_in.get
        for t, value in tiles_in.items():
            count_black = sum(tiles_get(n_tile, False) for n_tile in neighbour_tiles(t))
            if (value == True and (count_black == 0 or count_black > 2)) or (value == False and count_black == 2):
                tiles_new[t] = not value
        print(d)

        tiles_in = tiles_new

    return tiles_in

r = answer(tiles)
print(sum(r.values()))
