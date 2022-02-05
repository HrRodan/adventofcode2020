import collections
import operator
from itertools import combinations, islice, accumulate
from typing import Sequence, Tuple

with open('input.txt') as file:
    data = [int(line.strip()) for line in file.readlines()]

PREAMBLE_LENGTH = 25


# from itertools receipts
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def number_in_sum_of_pair(int_list: Sequence[int], number_: int):
    return any(x + y == number_ for x, y in combinations(int_list, 2))


first_wrong_number = -1
data_iter = sliding_window(data, PREAMBLE_LENGTH)
for n in data[PREAMBLE_LENGTH:]:
    if not number_in_sum_of_pair(next(data_iter), n):
        first_wrong_number = n
        break

print(first_wrong_number)


# part 2
def get_contiguous_set(search_number=first_wrong_number) -> Tuple[int, int]:
    for i, _ in enumerate(data):
        for j, s in enumerate(accumulate(islice(data, i, None), operator.add)):
            if s > first_wrong_number:
                break
            elif first_wrong_number == s and j > 1:
                return (i, j)

start, length = get_contiguous_set()
elements = data[start: start+length+1]

print(f'{min(elements)+max(elements)}')
