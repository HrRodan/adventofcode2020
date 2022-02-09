import math
from typing import Tuple, List

with open('input.txt') as file:
    dep, lines_raw = file.read().split('\n')

lines = [int(line.strip()) for line in lines_raw.split(',') if line != 'x']
dep = int(dep)

next_departure = {line: math.ceil(dep / line) * line for line in lines}

result = min(next_departure.items(), key=lambda x: x[1])
print(result[0] * (result[1] - dep))

# part 2

lines_enum = [(enum, int(line)) for enum, line in enumerate(lines_raw.split(',')) if line != 'x']


def find_earliest_departure(lines_in: List[Tuple[int, int]], start: int = 0, increment: int = None):
    '''
    Calculates the initial departure for the lines pairwise and interates through all lines. Each subsequent
    pairwise calculation inherits the start and increment of the previous pair to ensure that the new departure time
    is also valid for all previous lines.
    '''
    if len(lines_in) <= 1:
        return start

    pair = lines_in[:2]
    if not increment:
        increment = pair[0][1]
    i = start
    while True:
        i += increment
        if all(((i + enum) % line) == 0 for enum, line in pair):
            return find_earliest_departure(lines_in=lines_in[1:], start=i, increment=increment*pair[1][1])


print(find_earliest_departure(lines_enum))
