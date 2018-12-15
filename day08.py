def parse_tree(spec, offset):
    n_children = spec[offset]
    n_meta = spec[offset + 1]
    total_meta = 0
    offset += 2
    for _ in range(n_children):
        meta, offset = parse_tree(spec, offset)
        total_meta += meta
    new_offset = offset + n_meta
    return total_meta + sum(spec[offset:new_offset]), new_offset

def parse_input():
    with open('data/day08.txt') as f:
        return [int(n) for n in f.read().split()]

def step_1():
    return parse_tree(parse_input(), 0)
    
