from collections import defaultdict
serial_no = 5153
def power_level(x, y, serial_no):
    rid = x + 10
    n = (rid * y + serial_no) * rid
    d = (n - 1000 * (n // 1000)) // 100
    return d - 5

def power_map(serial_no):
    return [[power_level(x + 1, y + 1, serial_no) for x in range(300)] for y in range(300)]


def area_power_map(pm, size=3):
    m = {}
    r1 = range(300 - size + 1)
    r2 = range(size)
    for x in r1:
        for y in r1:
            m[(x + 1, y + 1)] = sum(pm[y + k][x + l] for k in r2 for l in r2)
    return m

def area_power_computer(serial_no=serial_no):
    _cache = defaultdict(dict)
    pm = power_map(serial_no)
    def area_power(corner, size):
        cached = _cache[size].get(corner, None)
        if cached is not None:
            return cached
        x, y = corner
        if size == 1:
            p = pm[y - 1][x - 1]
        elif size % 2 == 0:
            d = size // 2
            subcorners = [(x, y), (x + d, y), (x, y + d), (x + d, y + d)]
            p = sum(area_power(s, d) for s in subcorners)
        else:
            p = area_power(corner, size - 1)
            p += sum(area_power((x + size -1, y + k), 1) for k in range(size))
            p += sum(area_power((x + k, y + size - 1), 1) for k in range(size - 1))
        _cache[size][corner] = p
        return p
    area_power._cache = _cache
    area_power._pm = pm
    return area_power    

def max_area_power(pc, size):
    return max((pc((x, y), size), (x, y))
               for x in range(1, 300 - size + 2)
               for y in range(1, 300 - size + 2))
        
def level_1(serial_no=serial_no):
    area_power = area_power_computer(serial_no)
    return max_area_power(area_power, 3)

def level_2(serial_no=serial_no):
    pc = area_power_computer(serial_no)
    max_areas = [(max_area_power(pc, size), size) for size in range(1, 301)]
    return max(max_areas)

if __name__ == '__main__':
    print(f'Result: {level_2()}')
