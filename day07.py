import itertools as it
import heapq
from collections import defaultdict

INPUT_FILE = "data/day07.txt"
def parse_input(filename=INPUT_FILE):
  directed_edges = []
  with open(filename) as f:
      for line in f:
          if not line.strip(): continue
          parts = line.split()
          directed_edges.append((parts[1], parts[-3]))
  return directed_edges
        
def get_dependency_maps(edges):
  parents = defaultdict(set)
  children = defaultdict(set)
  for (s, d) in edges:
    children[s].add(d)
    parents[d].add(s)
  return parents, children

def sorted_steps(edges):
  parents, children = get_dependency_maps(edges)
  todo = set(parents) | set(children)
  ready = []
  while todo:
    for step in todo:
      if not parents[step]:
        heapq.heappush(ready, step)
    todo -= set(ready)
    done = heapq.heappop(ready)
    for step in children[done]:
      parents[step].remove(done)
    yield done

def parallel_time(edges):
  parents, children = get_dependency_maps(edges)
  todo = set(parents) | set(children)
  timer = 0
  doing = []
  while todo:
    for step in todo:
      if len(doing) == 5: break
      if not parents[step]:
        heapq.heappush(doing, (60 + ord(step) - ord('A') + 1, step))
    todo -= set([s for (_, s) in doing])
    time_ellapsed, done = heapq.heappop(doing)
    for step in children[done]:
      parents[step].remove(done)
    timer += time_ellapsed
    doing = [(t - time_ellapsed, step) for (t, step) in doing]
  return timer
      
    
def step_1(filename=INPUT_FILE):
  return ''.join(sorted_steps(parse_input(filename)))
  
def step_2(filename=INPUT_FILE):
  return parallel_time(parse_input(filename))
