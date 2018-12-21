import pdb
import math
import sys

from collections import defaultdict

steps =[(1, 0), (0, -1), (0, 1), (-1, 0)]

def find_paths(start, dest, free_spots, trail=None, explored=None):
    if explored is None:
        explored = defaultdict(lambda :math.inf)
    if trail is None:
        trail = []
    explored[start] = len(trail)
    trail = trail + [start]
    x, y = start
    neighbors = []
    for (dx, dy) in steps:
        n = (x + dx, y + dy)
        if n == dest:
            return [trail]
        if (n in free_spots) and (n not in trail) and (len(trail) < explored[n]):
            neighbors.append(n)
    res = []
    for n in neighbors:
        for p in find_paths(n, dest, free_spots, trail, explored):
            res.append(p)
    return res

def parse_map(fileobj):
    free_spots = set()
    goblins = set()
    elfs = set()
    for (y, line) in enumerate([l.strip() for l in fileobj if l.strip()]):
        for (x, c) in enumerate(line):
            loc = (x, y)
            if c == '.':
                free_spots.add(loc)
            elif c == 'E':
                elfs.add(loc)
            elif c == 'G':
                goblins.add(loc)
    return elfs, goblins, free_spots

def parse_map_array(fileobj):
    return [list(l.strip()) for l in fileobj if l.strip()]

def map_to_str(map_arr):
    return '\n'.join(''.join(l) for l in map_arr)

def print_map(map_arr, stdout=sys.stdout):
    stdout.write(map_to_str(map_arr))

def print_path(path, map_arr):
    m = [l[:] for l in map_arr]
    for (x, y) in paths:
        m[y][x] = '+'
    print_map(m)
        
    
    
if __name__ == '__main__':
    import pdb
    import test_day15 as t
    import io
    elfs, gobs, free = parse_map(t.fm2)
    pts = find_paths((1,1), (7,3), free)
    print('\n'.join('->'.join(str(t) for t in p) for p in pts))
