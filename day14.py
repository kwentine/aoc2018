def scoreboard(n):
    board = [3, 7]
    l = 2
    elf1 = 0
    elf2 = 1
    history = []
    for _ in range(n):
        history.append((elf1, elf2, l))
        board.extend(int(i) for i in list(str(board[elf1] + board[elf2])))
        l = len(board)
        elf1 = board[(board[elf1] + 1) % l]
        elf2 = board[(board[elf2] + 1) % l]
    print()
