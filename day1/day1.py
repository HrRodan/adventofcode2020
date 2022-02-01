from itertools import combinations

with open('input.txt') as file:
    exp = [int(x) for x in file.readlines() if x.strip()]

# part 1

res = [x * y for x, y in combinations(exp, 2) if x + y == 2020]

print(res)

# part 2

res2 = [x * y * z for x, y, z in combinations(exp, 3) if x + y + z == 2020]

print(res2)
