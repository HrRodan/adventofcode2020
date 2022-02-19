#https://www.reddit.com/r/adventofcode/comments/kimluc/2020_day_23_solutions/hixpd8s/
#also https://github.com/bsamseth/advent-of-code/blob/master/aoc-2020/day-23/day_23.py
# successor list
# looping list -> successor list

def fast_dic(cups, steps):  # non-rotated dictionary:  {cup: nextcup, ... }
    current = cups[0]
    mn, mx = min(cups), max(cups)
    carousel = dict(zip(cups, cups[1:] + [cups[0]]))

    for _ in range(steps):
        xyz = [carousel[current]]
        xyz.append(carousel[xyz[0]])
        xyz.append(carousel[xyz[-1]])
        dest = current - 1
        while dest < mn or dest in xyz:
            dest -= 1
            if dest < mn:
                dest = mx
        carousel[current] = carousel[xyz[-1]]
        carousel[xyz[-1]] = carousel[dest]
        carousel[dest] = xyz[0]
        current = carousel[current]
    return carousel

cups = fast_dic(list(map(int, (list("624397158")))), 100)
labels = [cups[1]]
while labels[-1] != 1:
    labels.append(cups[labels[-1]])
print('Part One:', "".join([str(c) for c in labels[:-1]]))

cups = fast_dic(list(map(int, (list("624397158")))) + list(range(9+1, 1_000_001)), 10_000_000)
c1 = cups[1]
c2 = cups[c1]
print('Part Two:', c1 * c2)
