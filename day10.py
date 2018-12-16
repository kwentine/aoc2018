import re
import os
from time import sleep
INPUT_FILENAME = 'data/day10.txt'
INPUT_COORD = r'([- ]\d+)'
INPUT_PATTERN = re.compile(r'position=<{}, {}> velocity=<{}, {}>'.format(*(INPUT_COORD,)*4))

class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def step(self):
        self.x += self.vx
        self.y += self.vy

    def scale(self, sx, sy):
        
        x = self.x * sx
        y = self.y * sy
        vx = self.vx * sx
        vy = self.vy * sy
        return Point(x, y, vx, vy)

    def translate(self, x0, y0):
        x = self.x + x0
        y = self.y + y0
        return Point(x, y, self.vx, self.vy)

    @property
    def ix(self):
        return round(self.x)

    @property
    def iy(self):
        return round(self.y)
        

def parse_input(filename=INPUT_FILENAME):
    points = set()
    with open(filename) as f:
        for line in f:
            if not line.strip(): continue
            try:
                p = Point(*(int(n) for n in INPUT_PATTERN.match(line).groups()))
                points.add(p)
            except (AttributeError, ValueError):
                print(f'Bad line: {line}')
    return points

def get_grid_dimensions(pts):
    xx = tuple(p.x for p in pts)
    yy = tuple(p.y for p in pts)
    mx, Mx = min(xx), max(xx)
    my, My = min(yy), max(yy)
    return (mx, my, Mx - mx, My - my)

def scale(pts, width=100, height=100):
    x0, y0, w, h = get_grid_dimensions(pts)
    return [p.translate(-x0, -y0).scale(100.0 / w, 100.0 / h) for p in pts]
    


def draw_grid(pts, width=100, height=100):
    grid = [['.' for _ in range(width + 1)] for _ in range(height + 1)]
    for p in pts:
        grid[p.ix][p.iy] = '#'
    for line in grid:
        print(''.join(line))


def animate_grid(pts, width=100, height=100):
    while(1):
        scaled = scale(pts)
        draw_grid(scaled)
        for p in pts:
            p.step()

