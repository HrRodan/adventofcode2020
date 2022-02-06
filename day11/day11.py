import functools
from itertools import product
from typing import List, Tuple

import numpy as np
from scipy import ndimage

with open('test_part2.txt') as file:
    data = file.read()

data = data.translate({ord('L'): '0', ord('#'): '1', ord('.'): '3'})
data = [[int(x) for x in list(line.strip())] for line in data.split('\n')]

hall_start = np.array(data, dtype=np.ubyte)


def change_seat(adjacent_seats: List[int]):
    return change_seat_memo(tuple(adjacent_seats))


@functools.cache
def change_seat_memo(adjacent_seats_tuple: Tuple[int]):
    this_seat = adjacent_seats_tuple[4]
    if this_seat == 3:
        return this_seat
    # subtract this seat (0 for unoccupied, 1 for occupied)
    occupied_seats = adjacent_seats_tuple.count(1) - this_seat
    if occupied_seats == 0:
        return 1
    elif occupied_seats >= 4:
        return 0
    else:
        return this_seat


hall = hall_start.copy()
for i in range(5000):
    hall_before = hall.copy()
    hall = ndimage.generic_filter(hall, size=(3, 3), function=change_seat,
                                  mode='constant', cval=3)
    if np.array_equal(hall_before, hall):
        print(np.count_nonzero(hall == 1))
        break


# part2

def point_add(point1: Tuple, point2: Tuple):
    return point1[0] + point2[0], point1[1] + point2[1]


list_of_points = set(np.ndindex(hall_start.shape))

next_seats = {point: [] for point in list_of_points if hall_start[point] in [0, 1]}
directions = list(product([1, -1, 0], repeat=2))
directions.remove((0, 0))

# calculate all next visible seats per seat
for point in next_seats:
    for d in directions:
        p = point_add(point, d)
        while p in list_of_points:
            if hall_start[p] in [0, 1]:
                next_seats[point].append(p)
                break
            p = point_add(p, d)

#next_seats = {point: np.transpose(seats) for point, seats in next_seats.items()}


def get_occupied_next_seats(seat: Tuple[int, int], hall_to_test: np.array):
    return sum(hall_to_test[seat_] for seat_ in next_seats[seat])


hall = hall_start.copy()
for i in range(5000):
    hall_before = hall.copy()
    for s in next_seats:
        occupied = get_occupied_next_seats(s, hall_before)
        if occupied == 0:
            hall[s] = 1
        elif occupied > 4:
            hall[s] = 0
    if np.array_equal(hall_before, hall):
        print(np.count_nonzero(hall == 1))
        break
