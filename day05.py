import re

def reduced_polymer(s):
    stack = ['']
    for c in s:
        prev = stack[-1]
        if prev.lower() == c.lower() and prev + c != c + prev:
                stack.pop()
        else:
            stack.append(c)
    return stack
        

def find_sortest(s):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    regexes = [f'[{c}{c.upper()}]' for c in letters]
    return min(len(reduced_polymer(re.sub(r, '', s))) for r in regexes) - 1
