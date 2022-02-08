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


def find_earliest_departure(lines_in: List[Tuple[int, int]], start: int = 0, increment: int = 1):
    '''
    Calculates the initial departure for the lines pairwise and interates through all lines. Each subsequent
    pairwise calculation inherits the start and increment of the previous pair to ensure that the new departure time
    is also valid for all previous lines.
    '''
    if len(lines_in) <= 1:
        return start
    i = start
    pair = lines_in[:2]
    while True:
        i += increment
        if all(((i + enum) % line) == 0 for enum, line in pair):
            # use least common multiple on old and new increment to obtain the smallest next increment which still
            # ensures that the already matched lines are still being valid in the next calculated departure time
            return find_earliest_departure(lines_in=lines_in[1:], start=i,
                                           increment=math.lcm(pair[0][1] * pair[1][1], increment))


print(find_earliest_departure(lines_enum))
