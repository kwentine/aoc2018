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

def step(coords, n_steps=1):
    for i in range(len(coords['x'])):
        coords['x'][i] += n_steps * coords['vx'][i]
        coords['y'][i] += n_steps * coords['vy'][i]
    return coords

def get_grid_dimensions(coords):
    xx = coords['x']
    yy = coords['y']
    mx, Mx = min(xx), max(xx)
    my, My = min(yy), max(yy)
    return (mx, my, Mx - mx, My - my)

import sys
import math
def animate_grid(stdscr):
    y, x = stdscr.getmaxyx()
    height, width = y - 5, x - 5
    coords = parse_input()
    stdscr.clear()
    prev_h = prev_w = math.inf
    idx = 9000
    step(coords, n_steps=idx)
    while(1):
        x0,y0,w,h = get_grid_dimensions(coords)
        if w >= prev_w or w >= prev_w:
            break
        prev_h, prev_w = h, w
        sw = min(width, w)
        sh = min(height, h)
        grid = [['.' for _ in range(sw + 1)] for _ in range(sh + 1)]
        for (x, y) in zip(coords['x'], coords['y']):
            j = round((y - y0) * sh / h)
            i = round((x - x0) * sw / w)
            grid[j][i] = '*'
        stdscr.clear()
        stdscr.addstr(0,0,f'iteration: {idx} width: {w} height: {h} scrren w: {sw} screen h: {sh}        ')
        for (j, line) in enumerate(grid):
            stdscr.addstr(j + 1, 0, ''.join(line))
        stdscr.refresh()
        step(coords)
        idx += 1
    sys.stdin.read()

if __name__ == '__main__':
    import curses
    curses.wrapper(animate_grid)
