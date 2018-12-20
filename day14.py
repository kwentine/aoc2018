from collections import deque
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

def board_until(n):
    board = [3, 7]
    board_len = 2
    i = 0
    j = 1
    history = [(i, j, board_len)]
    #import pdb; pdb.set_trace()
    while len(board) < n:
        b_i = board[i]
        b_j = board[j]
        d = digits(b_i + b_j)
        board.extend(d)
        board_len += len(d)
        i = (i + b_i + 1) % board_len
        j = (j + b_j + 1) % board_len
        history.append((i, j, board_len))
    return history, board

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
