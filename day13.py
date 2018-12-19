from collections import deque


def _left(i, j):
  return j, -i

def _right(i, j):
  return -j, i

def _straight(i, j):
  return (i, j)

SYMBOL_TO_SPEED = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1)
}

SPEED_TO_SYMBOL = dict((v, s) for (s, v) in SYMBOL_TO_SPEED.items())

CURVE_TRANSITIONS = {
    ('>', '/'): '^',
    ('>', '\\'): 'v',
    ('^', '/'): '>',
    ('^', '\\'): '<',
    ('<', '/'): 'v',
    ('<', '\\'): '^',
    ('v', '/'): '<',
    ('v', '\\'): '>'
}

BOLD_GREEN = "\x1B[1m\x1B[32m{}\x1B[30m\x1B[0m"
BOLD_RED =  "\x1B[1m\x1B[31m{}\x1B[30m\x1B[0m"
CLEAR_SCREEN = "\x1B[3J\x1B[H"
SAVE_CURSOR = "\x1B7"
RESTORE_CURSOR = "\x1B8"
class Cart:
  
  def __init__(self, x, y, symbol):
    self.x = x
    self.y = y
    self.v = SYMBOL_TO_SPEED[symbol]
    self.next_turn = deque([_left, _straight, _right])

  def move(self, track):
    self.x += self.v[0]
    self.y += self.v[1]
    new_loc = track[self.y][self.x]
    if new_loc in ('\\', '/'):
      self.handle_curve(new_loc)
    elif new_loc == '+':
      self.handle_intersect()

  def handle_intersect(self):
    self.v = self.next_turn[0](*self.v)
    self.next_turn.rotate(-1)
  
  def handle_curve(self, curve):
    s = SPEED_TO_SYMBOL[self.v]
    self.v = SYMBOL_TO_SPEED[CURVE_TRANSITIONS[(s, curve)]]

  def __repr__(self):
    return f"({self.x}, {self.y}) {SPEED_TO_SYMBOL[self.v]}"

  def __str__(self):
    return BOLD_GREEN.format(SPEED_TO_SYMBOL[self.v])

INPUT_FILE = 'data/day13.txt'

def parse_input(fileobj):
  track = []
  carts = []
  for y, line in enumerate(l for l in fileobj.readlines() if l.strip()):
    if not line.strip(): continue
    row = list(line[:-1])
    for (x, s) in enumerate(row):
      if s in '<>^v':
        carts.append(Cart(x, y, s))
        row[x] = '-' if s in '<>' else '|'
    track.append(row)
  return carts, track

def detect_collision(carts):
  current = None
  for c in carts:
    if current == (c.x, c.y):
      return current
    current = (c.x, c.y)
  return None

def run_until_collision(carts, track):
  collision = detect_collision(carts)
  while not collision:
    for c in carts:
      c.move(track)
    carts = sorted(carts, key=lambda c: (c.y, c.x))
    collision = detect_collision(carts)
  return collision


def snapshot(carts, tracks):
  grid = [t[:] for t in tracks]
  for c in carts:
    try:
      current = grid[c.y][c.x]
      grid[c.y][c.x] = str(c) if current in '|-/\\+' else BOLD_RED.format('X')
    except IndexError:
      pass
  return '\n'.join(''.join(r) for r in grid)

from time import sleep
import sys
def run_animation(carts, tracks):
  collision = None
  while not collision:
    print(SAVE_CURSOR + snapshot(carts, tracks))
    print(RESTORE_CURSOR, end='')
    for c in carts:
      c.move(tracks)
    carts = sorted(carts, key=lambda c: (c.y, c.x))
    collision = detect_collision(carts)
    sleep(0.1)
  print(snapshot(carts, tracks))
  print(BOLD_RED.format(f'Collision at ({collision[0]}, {collision[1]})'))

def step_1(filename=INPUT_FILE):
  with open(filename) as f:
    carts, track = parse_input(f)
    return run_until_collision(carts, track)
  
if __name__ == '__main__':
  from io import StringIO
  from test_day13 import TEST_INPUT
  run_animation(*parse_input(StringIO(TEST_INPUT)))
  
  
        
        
    
    
