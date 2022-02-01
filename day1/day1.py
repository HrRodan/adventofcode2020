from itertools import combinations
from numpy import prod

with open('input.txt') as file:
    exp = [int(x) for x in file.readlines() if x.strip()]

# part 1

res = [x * y for x, y in combinations(exp, 2) if x + y == 2020]

print(res)

# part 2

res2 = [prod(e) for e in combinations(exp, 3) if sum(e) == 2020]

print(res2)
