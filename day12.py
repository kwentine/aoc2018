INPUT_FILE = 'data/day12.txt'


def get_input(filename=INPUT_FILE):
    with open(filename) as f:
        return parse_input_file(f)
    
def parse_input_file(fileobj):
    l = fileobj.readline().strip()
    while not l:
        l = fileobj.readline().strip()
    _, initial_state = l.rsplit(' ', 1)
    fileobj.readline()
    rules = {}
    for line in fileobj:
        cond, _, res = line.strip().split()
        rules[cond] = res
    return initial_state, rules

def next_gen(state, initial_offset, rules):
    next_gen = []
    state = f'.....{state}.....'
    for i in range(2, len(state) - 2):
        patt = state[i-2:i+3]
        next_gen.append(rules.get(patt, '.'))

    i = 0
    initial_offset += 3
    while initial_offset > 0 and next_gen[i] == '.':
        initial_offset -= 1
        i += 1
    return ''.join(next_gen[i:]).rstrip('.'), initial_offset


def step_1(state, rules):
    offset = 0
    for i in range(20):
        state, offset = next_gen(state, offset, rules)
    total = 0
    for i, p in enumerate(state):
        if p == '#':
            total += i - offset
    return total

# Used to see at which point the pattern starts repeating and solve step 2
def evolve_and_trace(state, rules, niter):
    offset = 0
    for i in range(niter):
        state, offset = next_gen(state, offset, rules)
        total = 0
        for j, p in enumerate(state):
            if p == '#':
                total += j - offset
        print(f'[{i + 1}] {state.strip(".")} {total}')
    return total

from tqdm import tqdm
def find_period(state, rules, niter=100000):
    seen = set()
    offset = 0
    for i in tqdm(range(niter)):
        seen.add(state.strip())
        state, offset = next_gen(state, offset, rules)
        if state.strip() in seen:
            break
    else:
        return -1
    return i

if __name__ == '__main__':
    (state, rules) = get_input()
    evolve_and_trace(state, rules, 150)
