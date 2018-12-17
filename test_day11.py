import pytest
import day11 as d


def test_power_level():
    assert d.power_level(3, 5, 8) == 4
    assert d.power_level(122, 79, 57) == -5
    assert d.power_level(217, 196, 39) == 0
    assert d.power_level(101, 153, 71) == 4


def test_level_1():
    p, (x, y) = d.level_1(18)
    assert (x, y) == (33, 45) and p == 29
    p, (x, y) = d.level_1(42)
    assert (x, y) == (21, 61) and p == 30 


def test_area_power_computer():
    area_power = d.area_power_computer(18)
    corner = (33, 45)
    size = 1
    assert area_power(corner, size) == 4
    size = 2
    assert area_power(corner, size) == 14
    size = 3
    assert area_power(corner, size) == 29

