def reduced_polymer(s):
    stack = ['']
    for c in s:
        prev = stack[-1]
        if prev == c.upper() or prev == c.lower():
            stack.pop()
        else:
            stack.append(c)
    print(stack[:10])
    return len(stack) - 1
        
