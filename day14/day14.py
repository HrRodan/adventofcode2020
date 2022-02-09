import re
from collections import defaultdict
from itertools import product

with open('input.txt') as file:
    input_ = file.read().split('\nmask')

mask_program = []
for element in input_:
    line_iter = iter(element.split('\n'))
    mask_raw = re.search(r'[10X]+', next(line_iter)).group()
    program = {int(x): int(y) for line in line_iter
               for x, y in [re.match(r'^mem\[(\d+)] = (\d+)$', line.strip()).groups()]}
    mask_program.append((mask_raw, program))

# part1

memory = defaultdict(lambda: 0)
for mask, program in mask_program:
    and_mask = int(re.sub(r'[^0]', '1', mask), base=2)
    or_mask = int(re.sub(r'[^1]', '0', mask), base=2)

    for memory_postion, value in program.items():
        memory[memory_postion] = value & and_mask | or_mask

print(sum(memory.values()))

# part2

memory = defaultdict(lambda: 0)
for mask, program in mask_program:
    # and mask not necessary
    or_mask = int(mask.replace('X', '0'), base=2)
    # translate mask for floating bits
    x_mask_raw = mask.translate({ord('0'): '_', ord('1'): '_', ord('X'): '{}'})
    for p in product('10', repeat=x_mask_raw.count('{}')):
        x_mask_str = x_mask_raw.format(*p)
        # looping with replace is faster than sub with lambda and iterator
        # for n in p:
        #     #replace only one 'X' per loop
        #     x_mask_str = x_mask_str.replace('X', n, 1)
        x_mask_and = int(x_mask_str.replace('_', '1'), base=2)
        x_mask_or = int(x_mask_str.replace('_', '0'), base=2)
        for memory_postion, value in program.items():
            position = ((memory_postion | or_mask) & x_mask_and) | x_mask_or
            memory[position] = value

print(sum(memory.values()))
