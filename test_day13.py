import pytest
import day13 as d13
from io import StringIO

def test_run_until_collision():
  track_map = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""
  carts, tracks = d13.parse_input(StringIO(track_map))
  assert d13.run_until_collision(carts, tracks) == (7, 3)
  track_map = r"""
/><\
|  |
\--/
"""
  carts, tracks = d13.parse_input(StringIO(track_map))
  assert d13.run_until_collision(carts, tracks) == (2, 0)

def test_run_until_last_collision():
  track_map = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""
  carts, tracks = d13.parse_input(StringIO(track_map))
  assert d13.run_until_last_collision(carts, tracks) == (6, 4)
