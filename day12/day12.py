import math
import re
from typing import Tuple

with open('input.txt') as file:
    commands = [(c[0], int(c[1])) for line in file.readlines()
                for c in [re.match(r'^([A-Z]+)(\d+)$', line.strip()).groups()]]

POSITION_TYPE = Tuple[Tuple[int, int], int]

# North = 0°, clockwise
rotation = {0: 'N', 90: 'E', 180: 'S', 270: 'W'}


def move(p: POSITION_TYPE, command: Tuple[str, int]) -> POSITION_TYPE:
    c, amount = command
    (x, y), rot = p
    if c == 'N':
        return (x, y + amount), rot
    if c == 'S':
        return (x, y - amount), rot
    if c == 'E':
        return (x + amount, y), rot
    if c == 'W':
        return (x - amount, y), rot
    if c == 'L':
        return (x, y), (rot - amount) % 360
    if c == 'R':
        return (x, y), (rot + amount) % 360
    if c == 'F':
        return move(p, (rotation[rot], amount))


START = ((0, 0), 90)

position = START
for c in commands:
    position = move(position, c)

print(sum(map(abs, position[0])))


# Part2

def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(-angle) * (px - ox) - math.sin(-angle) * (py - oy)
    qy = oy + math.sin(-angle) * (px - ox) + math.cos(-angle) * (py - oy)
    return int(round(qx, 0)), int(round(qy, 0))


WAYPOINT_START = ((10, 1), 0)

waypoint = WAYPOINT_START
position = START
for com in commands:
    c, a = com
    if c in ['N', 'S', 'E', 'W']:
        waypoint = move(waypoint, com)
    elif c == 'L':
        waypoint = (rotate(position[0], waypoint[0], -math.radians(a)), 0)
    elif c == 'R':
        waypoint = (rotate(position[0], waypoint[0], math.radians(a)), 0)
    elif c == 'F':
        dx = waypoint[0][0] - position[0][0]
        dy = waypoint[0][1] - position[0][1]
        position = move(position, ('E', dx * a))
        position = move(position, ('N', dy * a))
        waypoint = ((position[0][0] + dx, position[0][1] + dy), 0)

print(sum(map(abs, position[0])))
