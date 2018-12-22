import pdb
import math
import sys

from collections import defaultdict

steps =[(1, 0), (0, -1), (0, 1), (-1, 0)]

def find_paths(start, dest, free_spots, trail=None, explored=None):
    if explored is None:
        explored = defaultdict(lambda : math.inf)
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

def find_shortest_path(start, dest, free_spots):
    visited = set()
    explored = defaultdict(lambda : (math.inf, None, None))
    explored[start] = (0, None, None)
    todo = {start}
    while todo:
        if dest in visited:
            break
        x, y  = min(todo, key=lambda x: (explored[x][0], x[1], x[0]))
        d, _, _ = explored[(x, y)]
        for (dx, dy) in steps:
            n = (x + dx, y + dy)
            if n not in free_spots - visited | {dest} :
                continue
            if d + 1 < explored[n][0]:
                explored[n] = (d + 1, x, y)
            todo.add(n)
        todo.remove((x, y))
        visited.add((x, y))
    if dest not in visited:
        return None
    path = []
    while dest != (None, None):
        path.append(dest)
        _, x, y  = explored[dest]
        dest = x, y
    return path

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

def print_map(map_arr, stdout=sys.stdout, end='\n'):
    stdout.write(map_to_str(map_arr) + end)

def print_path(path, map_arr):
    m = [l[:] for l in map_arr]
    (x, y), *rest = path
    m[y][x] = 'X'
    for (x, y) in rest:
        m[y][x] = '+'
    print_map(m)
        
    
    
if __name__ == '__main__':
    import pdb
    import test_day15 as t
    import io
    elfs, gobs, free = parse_map(t.fm1)
    p = find_shortest_path((1, 1), (7,3), free)
    t.fm1.seek(0)
    map_arr = parse_map_array(t.fm1)
    print_path(p, map_arr)
