# https://www.reddit.com/r/adventofcode/comments/keqsfa/2020_day_17_solutions/gg6xjyo/

import numpy as np
from scipy.ndimage import convolve


def answers(raw):
    init = np.array([list(r) for r in raw.split("\n")]) == "#"
    N = 6
    for D in (3, 4):
        active = np.pad(init[(None,) * (D - init.ndim)], N)
        for _ in range(N):
            nbs = convolve(active, np.ones((3,) * D), int, mode="constant")
            active[:] = active & (nbs == 4) | (nbs == 3)
        yield np.sum(active)
