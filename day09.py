from collections import defaultdict
N_PLAYERS = 478
N_MARBLES = 71240

class Marble:
    def __init__(self, points):
        self.points = points
        self.prev = self.next = self
    def insert(self, points):
        new_marble = Marble(points)
        new_marble.prev = self.next
        new_marble.next = self.next.next
        self.next.next.prev = new_marble
        self.next.next = new_marble
        return new_marble
    def remove(self):
        current = self
        for _ in range(7):
            current = current.prev
        current.prev.next = current.next
        current.next.prev = current.prev
        # print(f'removed {current.points}')
        return current

def marble_game(n_players=N_PLAYERS, n_marbles=N_MARBLES):
    player = 1
    turn = 1
    current_marble = zero_marble = Marble(0)
    scores = defaultdict(int)
    while turn <= n_marbles:
        #print(f'[{player}]', end=' ')
        #print_marbles(zero_marble, current_marble)
        if turn % 23 == 0:
            removed = current_marble.remove()
            scores[player] += (turn + removed.points)
            # print(f"player {player} scores {turn} + {removed.points}")
            current_marble = removed.next
        else:
            current_marble = current_marble.insert(turn)
        player = player + 1 if player < n_players else 1
        turn += 1
    return max(scores.values())

def print_marbles(start, current):
    mp = start
    while 1:
        fmt = f"({mp.points})" if mp is current else f"{mp.points}"
        print(fmt, end=' ')
        if mp.next == start:
            break
        else:
            mp = mp.next
    print('')

def step_1():
    return marble_game()
