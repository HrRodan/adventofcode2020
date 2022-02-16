import math
import re

import numpy as np
from scipy.ndimage import generic_filter

with open('input.txt') as file:
    tiles_raw = file.read().strip().split('\n\n')

tiles = {}
for tile_name in tiles_raw:
    name, *tile = tile_name.split('\n')
    tiles[int(re.search(r'\d+', name).group())] = np.where(np.array([list(x) for x in tile]) == '#', 1, 0)

edges = {}
for name, tile in tiles.items():
    edges[name] = (tuple(tile[0, :]), tuple(tile[:, -1]), tuple(tile[-1, :]), tuple(tile[:, 0]))

# get all possible tile connections
transformations = {}
possible_matches = {key: [] for key in tiles}
for start_name, start_edges in edges.items():
    for test_name, test_edges in edges.items():
        if start_name != test_name:
            for start_edge in start_edges:
                start_edge_reverse = start_edge[::-1]
                for test_edge in test_edges:
                    if start_edge == test_edge or start_edge_reverse == test_edge:
                        possible_matches[start_name].append(test_name)

# edges only have two possible neighbors
print(np.prod([x for x, edges in possible_matches.items() if len(edges) == 2]))

len2_tiles = set(x for x, edges in possible_matches.items() if len(edges) == 2)
len3_tiles = set(x for x, edges in possible_matches.items() if len(edges) == 3)
len4_tiles = set(x for x, edges in possible_matches.items() if len(edges) == 4)

dim = int(math.sqrt(len(edges)))

# calculate possible layout first by ignoring the actual orientation and only considering possible neighbors
image = [[0 for _ in range(dim)] for _ in range(dim)]
image_np = [[0 for _ in range(dim)] for _ in range(dim)]
for i in range(dim):
    for j in range(dim):
        # first row
        if i == 0:
            # very first tile
            if j == 0:
                image[i][j] = len2_tiles.pop()
            # only check left tile for first row
            elif j != dim - 1:
                for edge in possible_matches[image[i][j - 1]]:
                    if edge in len3_tiles:
                        image[i][j] = edge
                        len3_tiles.remove(edge)
                        break
            elif j == dim - 1:
                for edge in possible_matches[image[i][j - 1]]:
                    if edge in len2_tiles:
                        image[i][j] = edge
                        len2_tiles.remove(edge)
                        break
        elif i != dim - 1:
            if j == 0:
                for edge in possible_matches[image[i - 1][j]]:
                    if edge in len3_tiles:
                        image[i][j] = edge
                        len3_tiles.remove(edge)
                        break
            elif j != dim - 1:
                for edge1 in possible_matches[image[i - 1][j]]:
                    for edge2 in possible_matches[image[i][j - 1]]:
                        if edge1 == edge2:
                            if edge1 in len4_tiles:
                                image[i][j] = edge1
                                len4_tiles.remove(edge1)
                                break
            elif j == dim - 1:
                for edge1 in possible_matches[image[i - 1][j]]:
                    for edge2 in possible_matches[image[i][j - 1]]:
                        if edge1 == edge2:
                            if edge1 in len3_tiles:
                                image[i][j] = edge1
                                len3_tiles.remove(edge1)
                                break
        else:
            if j == 0:
                for edge in possible_matches[image[i - 1][j]]:
                    if edge in len2_tiles:
                        image[i][j] = edge
                        len2_tiles.remove(edge)
                        break
            elif j != dim - 1:
                for edge1 in possible_matches[image[i - 1][j]]:
                    for edge2 in possible_matches[image[i][j - 1]]:
                        if edge1 == edge2:
                            if edge1 in len3_tiles:
                                image[i][j] = edge1
                                len3_tiles.remove(edge1)
                                break
            elif j == dim - 1:
                for edge1 in possible_matches[image[i - 1][j]]:
                    for edge2 in possible_matches[image[i][j - 1]]:
                        if edge1 == edge2:
                            if edge1 in len2_tiles:
                                image[i][j] = edge1
                                len2_tiles.remove(edge1)
                                break


def get_possible_transforms(array_in: np.ndarray):
    for rot in range(4):
        yield np.rot90(array_in, k=rot)
        for ax in [0, 1]:
            yield np.flip(np.rot90(array_in, k=rot), axis=ax)


# repopulate image with actual tiles by transformating until matching edge is found
image_np = [[0 for _ in range(dim)] for _ in range(dim)]
for i in range(dim):
    for j in range(dim):
        if i == 0 and j == 0:
            for np1 in get_possible_transforms(tiles[image[i][j]]):
                for np2 in get_possible_transforms(tiles[image[i][j + 1]]):
                    for np3 in get_possible_transforms(tiles[image[i + 1][j]]):
                        if np.array_equal(np1[:, -1], np2[:, 0]):
                            if np.array_equal(np1[-1, :], np3[0, :]):
                                image_np[i][j] = np1
                                image_np[i][j + 1] = np2
                                image_np[i + 1][j] = np2
                                break
        elif i == 0:
            for np1 in get_possible_transforms(tiles[image[i][j]]):
                np_left = image_np[i][j - 1]
                if np.array_equal(np1[:, 0], np_left[:, -1]):
                    image_np[i][j] = np1
                    break
        else:
            for np1 in get_possible_transforms(tiles[image[i][j]]):
                np_top = image_np[i - 1][j]
                if np.array_equal(np1[0, :], np_top[-1, :]):
                    image_np[i][j] = np1
                    break

# remove edges
for i in range(dim):
    for j in range(dim):
        image_np[i][j] = image_np[i][j][1:-1, 1:-1]

# concat all tiles to one big tile
for i in range(dim):
    np_temp = np.concatenate(image_np[i], axis=1)
    if i == 0:
        np_full = np_temp
    else:
        np_full = np.concatenate((np_full, np_temp), axis=0)

with open('seamonster.txt') as file2:
    monster = file2.read()

# fp... footprint
monster_fp = np.array([list(line) for line in monster.split('\n') if line.strip()])
monster_fp = np.where(monster_fp == '#', 1, 0)
monster_size = monster_fp.sum()


def find_mosnters(test: np.ndarray):
    return 1 if test.sum() == monster_size else 0


count = []
for array in get_possible_transforms(np_full):
    monsters = generic_filter(array, function=find_mosnters, footprint=monster_fp, mode='constant', cval=0)
    count.append(monsters.sum())

print(np_full.sum() - max(count) * monster_size)
