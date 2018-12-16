import re
import os
from time import sleep
INPUT_FILENAME = 'data/day10.txt'
INPUT_COORD = r'([- ]\d+)'
INPUT_PATTERN = re.compile(r'position=<{}, {}> velocity=<{}, {}>'.format(*(INPUT_COORD,)*4))

def parse_input(filename=INPUT_FILENAME):
    xx = []
    yy = []
    vxx = []
    vyy = []
    with open(filename) as f:
        for line in f:
            if not line.strip(): continue
            x, y, vx, vy = (int(n) for n in INPUT_PATTERN.match(line).groups())
            xx.append(x)
            yy.append(y)
            vxx.append(vx)
            vyy.append(vy)
    return dict(x=xx, y=yy, vx=vxx, vy=vyy)

def step(coords):
    for i in range(len(coords['x'])):
        coords['x'][i] += coords['vx'][i]
        coords['y'][i] += coords['vy'][i]
    return coords

def get_grid_dimensions(coords):
    xx = coords['x']
    yy = coords['y']
    mx, Mx = min(xx), max(xx)
    my, My = min(yy), max(yy)
    return (mx, my, Mx - mx, My - my)

def scaled(coords, width=100, height=60):
    x0, y0, w, h = get_grid_dimensions(coords)
    s_x = float(width) / w
    s_y = float(height) / h
    s_coords = {}
    s_coords['x'] = [(x - x0) * s_x for x in coords['x']]
    s_coords['vx'] = [ vx * s_x for vx in coords['vx']]
    s_coords['y'] = [(y - y0) * s_y for y in coords['y']]
    s_coords['vy'] = [ vy * s_y for vy in coords['vy']]
    return s_coords

def std(coords):
    mx = sum(coords['x'])/float(len(coords['x']))
    my = sum(coords['y'])/float(len(coords['y']))
    sx = sum((x - mx)**2 for x in coords['x'])
    sy = sum((y - my)**2 for y in coords['y'])
    return sx + sy

    
def draw_grid(coords, width=100, height=50):
    grid = [['.' for _ in range(width + 1)] for _ in range(height + 2)]
    for (x, y) in zip(coords['x'], coords['y']):
        grid[round(x)][round(y)] = '*'
    print('#' * width)
    for line in grid:
        print(''.join(line))

import sys
import math
from random import random
def animate_grid(stdscr):
    coords = parse_input()
    stdscr.clear()
    prev_dims = math.inf
    idx = 1
    while(1):
        s_coords = scaled(coords)
        _,_,h,w = get_grid_dimensions(coords)
        if h + w >= prev_dims:
            break
        prev_dims = h + w 
        grid = [['.' for _ in range(101)] for _ in range(61)]
        for (x, y) in zip(s_coords['x'], s_coords['y']):
            grid[round(y)][round(x)] = '*'
        stdscr.addstr(0,0,f'{prev_dims} it={idx}')
        for (j, line) in enumerate(grid):
            stdscr.addstr(j + 1, 0, ''.join(line))
        stdscr.refresh()
        step(coords)
        idx += 1
    sys.stdin.read()

if __name__ == '__main__':
    from curses import wrapper
    wrapper(animate_grid)

    # 10408611
