import math
from collections import defaultdict
from itertools import combinations, product

INPUT_FILE = "data/day06.txt"

_cache = {}
_infinite = set()
def coords_from_file(filename):
    with open(filename) as f:
        return set(eval(l) for l in f)
    
def find_closest(point, seeds):
    """Find the seed closest to a given point
    
    Maintain a cache of points for which the closest seed is known.
    Return stricly closest seed, or None if it is a tie.
    """
    if point in _cache:
        return _cache[point]
    min_dist = math.inf
    closest = None
    x0, y0 = point
    for (x, y) in seeds:
        dist = abs(x - x0) + abs(y - y0)
        if dist == min_dist:
            closest = None
        elif dist < min_dist:
            min_dist = dist
            closest = (x, y)
    _cache[point] = closest
    return closest


def assign_to_cell(point, cells):
    seed = find_closest(point, cells)
    if seed:
        cells[seed].add(point)
    return seed

# TODO Implement only a find_min
def find_linear_extrema(form, seeds):
    x0, y0 = form
    min_val = +math.inf
    min_seeds = []
    max_val = -math.inf
    max_seeds = []
    for s in seeds:
        x, y = s
        val = x0 * x + y0 * y
        if val == max_val:
            max_seeds.append(s)
        elif val > max_val:
            max_val = val
            max_seeds = [s]
        if val == min_val:
            min_seeds.append(s)
        elif val < min_val:
            min_val = val
            min_seeds = [s]
    return set(min_seeds) | set(max_seeds)


def convex_hull(seeds):
    forms = set()
    for (p, q) in combinations(seeds, 2):
        # TODO Normalize and check for colinearity
        x0, y0 = p
        x1, y1 = q
        x3, y3 = (x1 - x0, y1 - y0)
        forms.add((-y3, x3))
    hull = set()
    for f in forms:
        hull |= find_linear_extrema(f, seeds)
    return hull
        
def claim_cell(seed, cells):
    r = 0
    while claim_at_distance(seed, r, cells):
        # Infinite
        # if r >= 200:
        #     _infinite.add(seed)
        #     break
        r += 1
    return len(cells[seed])


def claim_at_distance(seed, r, cells):
    claimed = 0
    for p in square_edge(seed, r):
        which = assign_to_cell(p, cells)
        if which == seed:
            claimed += 1
    return claimed


def square_edge(p, r):
    x0, y0 = p
    rx = range(x0 - r, x0 + r + 1)
    ry = range(y0 - r, y0 + r + 1)
    if r == 0:
        yield p
    else:
        yield from ((i, y0 + r) for i in rx)
        yield from ((i, y0 - r) for i in rx)
        yield from ((x0 + r, j) for j in ry)
        yield from ((x0 - r, j) for j in ry)
        

def level_1(filename=INPUT_FILE):
    coords = coords_from_file(filename)
    candidates = [s for s in coords if is_bounded(s, coords)]
    cells = {s: set() for s in coords}
    print(f"Total candidate seeds: {len(candidates)}")
    for seed in candidates:
        n = claim_cell(seed, cells)
        print(f"\tSeed {seed}: {n}")
    return max(len(cells[seed]) for seed in candidates)

def is_bounded(seed, others):
    return (_bounded_right(seed, others) and
            _bounded_left(seed, others) and
            _bounded_up(seed, others) and
            _bounded_down(seed, others))

def _bounded_right(seed, others):
    x0, y0 = seed
    return any(x > x0 and abs(x - x0) >= abs(y - y0) for x, y in others)

def _bounded_left(seed, others):
    x0, y0 = seed
    return any(x < x0 and abs(x - x0) >= abs(y - y0) for x, y in others)

def _bounded_up(seed, others):
    x0, y0 = seed
    return any(y > y0 and abs(x - x0) <= abs(y - y0) for x, y in others)

def _bounded_down(seed, others):
    x0, y0 = seed
    return any(y < y0 and abs(x - x0) <= abs(y - y0) for x, y in others)

def integral_centroid(coords):
    n = len(coords)
    x = sum(x for (x, _) in coords)/n
    y = sum(y for (_, y) in coords)/n
    return (int(x), int(y))

def is_safe(p, coords):
    x0, y0 = p
    return sum(abs(x - x0) + abs(y - y0) for (x, y) in coords) < 10000

def count_safe_at_distance(p, r, coords):
    return sum(is_safe(q, coords) for q in set(square_edge(p, r)))

def count_safe(coords):
    g = integral_centroid(coords)
    count = 0
    r = 0
    while 1:
        n_safe = count_safe_at_distance(g, r, coords)
        if not n_safe:
            break
        count += n_safe
        r += 1
    return count

def level_2(filename=INPUT_FILE):
    return count_safe(coords_from_file(filename))
    

if __name__ == "__main__":
    res = level_2()
    print(f'Safe area: {res}')
             
