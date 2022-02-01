import numpy as np

with open('input.txt') as file:
    forest = np.array([list(line.strip()) for line in file.readlines()])

forest = forest == '#'

START = (0, 0)


def move(x: tuple, move_diff: tuple, vdim: int):
    return x[0] + move_diff[0], (x[1] + move_diff[1]) % vdim


def traverse_slope(move_diff: tuple):
    pos = START
    count_trees = 0
    while pos[0] < forest.shape[0]:
        if forest[pos]:
            count_trees += 1
        pos = move(pos, move_diff, forest.shape[1])

    return count_trees


# part 1
print(traverse_slope((1,3)))

# part 2

move_dirs = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
counts_tree = [traverse_slope(x) for x in move_dirs]
print(np.prod(counts_tree))
