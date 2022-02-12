import numpy as np
from scipy import ndimage

with open('input.txt') as file:
    start_cubes = np.array([list(line.strip()) for line in file.readlines()])

start_cubes: np.ndarray = start_cubes == '#'

ROUNDS = 6

cubes = np.full(shape=(1, start_cubes.shape[0], start_cubes.shape[1]), fill_value=False)
cubes[0] = start_cubes


def nice_view(a: np.ndarray):
    view = np.full(shape=a.shape, fill_value='.')
    view[a] = '#'
    return view


def switch_cubes(current_cubes: np.ndarray):
    # 13 is centre due  index to starting at 0
    this_cube = current_cubes[13]
    count_active_cubes = current_cubes.sum() - this_cube
    if this_cube == 1:
        if count_active_cubes in (2, 3):
            return True
        else:
            return False
    else:
        if count_active_cubes == 3:
            return True
        else:
            return False


for _ in range(ROUNDS):
    cubes = np.pad(cubes, pad_width=1, mode='constant', constant_values=False)
    cubes = ndimage.generic_filter(cubes, size=(3, 3, 3), function=switch_cubes, mode='constant', cval=False)

print(cubes.sum())


# part 2

def switch_cubes_4d(current_cubes: np.ndarray):
    # 40 is centre due  index to starting at 0
    this_cube = current_cubes[40]
    count_active_cubes = current_cubes.sum() - this_cube
    if this_cube == 1:
        if count_active_cubes in (2, 3):
            return True
        else:
            return False
    else:
        if count_active_cubes == 3:
            return True
        else:
            return False


cubes_4d = np.full(shape=(1, 1, start_cubes.shape[0], start_cubes.shape[1]), fill_value=False)
cubes_4d[0] = start_cubes

for _ in range(ROUNDS):
    cubes_4d = np.pad(cubes_4d, pad_width=1, mode='constant', constant_values=False)
    cubes_4d = ndimage.generic_filter(cubes_4d, size=(3, 3, 3, 3), function=switch_cubes_4d, mode='constant',
                                      cval=False)

print(cubes_4d.sum())
