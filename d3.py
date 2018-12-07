#!/usr/local/bin/python3.7
import re
import itertools as it
from collections import defaultdict


INPUT_FILE='data/d3.txt'

input_regex = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

def parse_line(line):
    """ Parse a line of input in a 4-tuple of (x, y, width, height)
    
    Input line format: 
      #1 @ 16,576: 17x14
    """
    try:
        return tuple(int(d) for d in input_regex.search(line).groups()) 
    except (AttributeError, ValueError):
        print(f'Bad line: {line}')

def get_span(line):
    rid, x, y, w, h = parse_line(line)
    return it.product([x + i for i in range(w)], [y + j for j in range(h)])

        
def find_claimed_multiple(fileobj):
    claimed_inches = defaultdict(int)
    for line in fileobj:
        line = line.strip()
        if not line:
            continue
        rect = get_span(line)
        for coords in rect:
            claimed_inches[coords] += 1
    return len([c for c in claimed_inches if claimed_inches[c] >= 2])


def find_non_overlapping(fileobj):
    rects = [parse_line(l) for l in fileobj if l.strip()]
    candidates = set(rects)
    for r in rects:
        for c in list(candidates):
            if c[0] != r[0] and overlap(c, r):
                candidates.remove(c)
    return tuple(c[0] for c in candidates)

def overlap(rect1, rect2):
    _, x1, y1, w1, h1 = rect1
    _, x2, y2, w2, h2 = rect2
    return overlap1d(x1, w1, x2, w2) and  overlap1d(y1, h1, y2, h2)

def overlap1d(x, dx, y, dy):
    return (x <= y and x + dx > y) or (y <= x and y + dy > x) 

if __name__ == "__main__":
    import sys
    try: 
        level = int(sys.argv[1])
    except(KeyError, ValueError):
        level = 1
    with open(INPUT_FILE) as f:
        if level == 1:
            result = find_claimed_multiple(f)
            print(f'Number of inches claimed at least twice: {result}')
        elif level == 2:
            result = (str(rid) for rid in find_non_overlapping(f))
            print(f'IDs of intact rectangles: {" ".join(result)}')
        else:
            print(f"Usage: {sys.argv[0]} [1 | 2]")
            
        
        
