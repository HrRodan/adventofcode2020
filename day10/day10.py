import functools
import itertools as it
from typing import Tuple

import numpy as np

with open('input.txt') as file:
    adapters = [int(line.strip()) for line in file.readlines()]

adapters.sort()

# add end
adapters.append(adapters[-1] + 3)
# add start
adapters.insert(0, 0)

diff = np.diff(adapters)
bins = np.bincount(diff)

print(bins[1] * bins[3])

# part 2

# only 1 and 3 as jolt difference exist
# the only possibility for skipping adapters from the ordered list is where the jolt difference is 1
# Consecutive number of x "1" differences lead to possibilities 2**(x-2)

# gett all indizes of jolt differences of three
diff_3_indices = (diff == 3).nonzero()

# get differences of the indices which equals the number of consecutive "1" differences
consecutive_1s = np.diff(diff_3_indices, prepend=-1)

# two adapters are always "frozen" due to the maximum jolt difference of three
consecutive_1s_unfrozen = np.where(consecutive_1s > 2, consecutive_1s - 2, 0)

# maximum number of consecutive unfrozen 1s is 3 -> in this case there 7 possibilites (instead of 2*8)
# in this case removing all adapters is not possible
possibilites = np.prod(2 ** consecutive_1s_unfrozen - np.where(consecutive_1s_unfrozen == 3, 1, 0))
print(possibilites)


@functools.cache
def number_arrangements(number_1s: int):
    return sum(1 for c in it.product([0, 1], repeat = number_1s) if
               np.max(np.diff(np.diff(c, append=1, prepend=1).nonzero()), initial=0) < 3)

for i in it.product([0, 1], repeat = 5):
    if np.max(np.diff(np.diff(i, append=1, prepend=1).nonzero()), initial=0) >= 3:
        print(i)

def count_consecutive_zeros(tup : Tuple[int]):
    pass
