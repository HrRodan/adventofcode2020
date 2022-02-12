# https://www.reddit.com/r/adventofcode/comments/keqsfa/2020_day_17_solutions/gg63k9o/

#!/usr/bin/env python3

import sys
import numpy as np

def rule(old, count): return count == 3 or old and count == 2
def step(grid):
    grow = np.zeros(tuple(i+2 for i in grid.shape), dtype=np.int8)
    new  = np.zeros(tuple(i+2 for i in grid.shape), dtype=np.int8)
    grow[tuple(slice(1,-1) for _ in grow.shape)] = grid
    for idx, x in np.ndenumerate(grow):
        n = grow[tuple(slice(max(0, i-1),(i+2)) for i in idx)]
        count = np.count_nonzero(n) - grow[idx]
        new[idx] = rule(grow[idx], count)
    return new

def solve(start, dim, every=slice(None, None)):
    pre, yx = tuple(1 for _ in range(dim-2)), (len(start), len(start[0]))
    grid = np.zeros(pre + yx, dtype=np.int8)
    grid[tuple(0 for _ in pre) + (every, every)] = start
    for x in range(6): grid = step(grid)
    return np.count_nonzero(grid)

if __name__ == '__main__':
    start = [[c == '#' for c in l[:-1]] for l in open(sys.argv[1])]
    print(solve(start, 3))
    print(solve(start, 4))
