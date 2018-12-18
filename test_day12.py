import pytest
import day12 as d12
from io import StringIO

TEST_INPUT = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""

TEST_OUTPUT = """
 0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##.
"""

def parse_test_output(f):
    gens = []
    for l in f:
        if not l.strip(): continue
        _, gen = l.strip().rsplit(' ')
        gens.append(gen)
    return gens


def test_next_gen():
    state, rules = d12.parse_input_file(StringIO(TEST_INPUT))
    results = parse_test_output(StringIO(TEST_OUTPUT))
    offset = 0
    state, offset = d12.next_gen(state, offset, rules)
    assert state == results[1].strip('.')
    assert offset == 0

    state, offset = d12.next_gen(state, offset, rules)
    assert state == results[2].strip('.')
    assert offset == 0
    
    state, offset = d12.next_gen(state, offset, rules)
    assert state == results[3].strip('.')
    assert offset == 1
        

def test_step_1():
    state, rules = d12.parse_input_file(StringIO(TEST_INPUT))
    assert d12.step_1(state, rules) == 325

    
def test_padding():
    _, rules = d12.parse_input_file(StringIO(TEST_INPUT))
    state, offset = '...#.#..#...#.#...#..#..##..##.........', 3
    new_state, offset = d12.next_gen(state, offset, rules)
    expected = '.#...##...#.#..#..#...#...#'
    assert new_state == expected
    assert offset == 0
