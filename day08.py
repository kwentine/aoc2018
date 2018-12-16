def get_meta_sum(spec, offset):
    n_children = spec[offset]
    n_meta = spec[offset + 1]
    total_meta = 0
    offset += 2
    for _ in range(n_children):
        meta, offset = get_meta_sum(spec, offset)
        total_meta += meta
    new_offset = offset + n_meta
    return total_meta + sum(spec[offset:new_offset]), new_offset

def get_value(spec, offset):
    n_children = spec[offset]
    n_meta = spec[offset + 1]
    cache = {}
    offset += 2
    for i in range(n_children):
        child_value, offset = get_value(spec, offset)
        cache[i + 1] = child_value
    new_offset = offset + n_meta
    # Now compute this node's value
    meta = spec[offset:new_offset]
    if not n_children:
        value = sum(meta)
    else:
        value = 0
        for n in meta:
            try:
                value += cache[n]
            except KeyError:
                pass
    return value, new_offset
    
def parse_input():
    with open('data/day08.txt') as f:
        return [int(n) for n in f.read().split()]

def step_1():
    return get_meta_sum(parse_input(), 0)


def step_2():
    return get_value(parse_input(), 0)
