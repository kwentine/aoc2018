from collections import deque
from array import array

def digits(n):
    r = n % 10
    q = n // 10
    if n == 0:
        return [0]
    d = deque()
    while n:
        d.appendleft(n % 10)
        n = n // 10
    return list(d)

def match(patt, board, start):
    patt_len = len(patt)
    max_len = len(board) - patt_len
    for idx in range(start, max_len + 1):
        for i in range(len(patt)):
            if patt[i] != board[idx + i]: break
        else:
            return idx
    return -1

def board_until(n):
    board = [3, 7]
    i = 0
    j = 1
    history = [(0, 1, 2)]
    while len(board) < n:
        i, j = board_step(i, j, board)
        history.append((i, j, len(board)))
    return history, board

def board_extend(i, j, board):
    b_i = board[i]
    b_j = board[j]
    d = digits(b_i + b_j)
    board.extend(d)
    l = len(board)
    i = (i + b_i + 1) % l
    j = (j + b_j + 1) % l
    return (i, j)

def board_until_patt(patt):
    patt = array('B', [int(i) for i in patt])
    board = array('B', [3, 7])
    i = 0
    j = 1
    match_idx = -1
    l = len(patt)
    while match_idx < 0:
        i, j = board_extend(i, j, board)
        if board[-l:] == patt:
            match_idx = len(board) - l
        elif board[-l - 1: -1] == patt:
            match_idx = len(board) - l - 1
    return match_idx
    

def board_lines(history, board):
    lines = []
    for (i, j, l) in history:
        line = [f'{d:^3}'for d in board[:l]]
        line[i] = f'({line[i][1]})'
        line[j] = f'[{line[j][1]}]'
        lines.append(line)
    return lines

def board_to_str(history, board):
    return '\n'.join(''.join(l) for l in board_lines(history, board))

def step_1(n):
    _, board = board_until(n + 10)
    return ''.join(str(i) for i in board[n:n+10])



if __name__ == '__main__':
    import sys
    try:
        n = int(sys.argv[1])
    except (ValueError, IndexError):
        n = 9
    #print(board_to_str(*board_until(n)))
    print(step_1(n))
