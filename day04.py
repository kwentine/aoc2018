#!/usr/local/bin/python3.7
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from itertools import groupby
import re

line_regex = re.compile(r'^\[(.{16})\] (.+)')

def parse_line(l):
    try: 
        datestr, event = line_regex.match(l).groups()
    except AttributeError:
        print(f"Bad line: {l}")
    dt = datetime.strptime(datestr, "%Y-%m-%d %H:%M")
    if event.startswith("Guard"):
        # guard ID
        event = int(event.split()[1][1:])
    else:
        # True if falls asleep
        event = event[0] == 'f'
    return (dt, event)


def night_watch_events(fileobj):
    current_guard = None
    for l in fileobj:
        if not l.strip(): continue
        dt, event = parse_line(l)
        if isinstance(event, bool):
            yield (dt.date(), dt.minute, current_guard, event)
        else:
            current_guard = event

            
def minutes_asleep_byguard(events):
    guards = defaultdict(list)
    it = iter(events)
    for evt in it:
        _, asleep_at, gid, asleep_true = evt
        _, awake_at, same_gid, asleep_false = next(it)
        guards[gid].extend(range(asleep_at, awake_at))
    return guards

    
def most_sleepy_guard(mins_byguard):
    return max(mins_byguard, key=lambda gid: len(mins_byguard[gid]))


def most_slept_min(mins):
    return Counter(mins).most_common()[0]    

def most_freq_asleep_same_min(mins_byguard):
    l = [(g, most_slept_min(mins)) for (g, mins) in mins_byguard.items() ]
    g, (minute, _) = max(l, key=lambda x: x[1][1])
    return g, minute


def parse_events_from_file(filename):
    with open(filename) as f:
        return list(night_watch_events(sorted(f)))

def solve_level_1(evts):
    d = minutes_asleep_byguard(evts)
    g = most_sleepy_guard(d)
    m = most_slept_min(d[g])[0]
    return g, m

def solve_level_2(evts):
    d = minutes_asleep_byguard(evts)
    return most_freq_asleep_same_min(d)


if __name__ == "__main__":
    import sys
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'data/day04.txt'
    events = parse_events_from_file(filename)
    g, m = solve_level_1(events)
    print('* Level 1')
    print(f'Guard: {g}\nMinute: {m}\nResult: {g * m}')
    g, m = solve_level_2(events)
    print(f'* Level 2')
    print(f'Guard: {g}\nMinute: {m}\nResult: {g * m}')    
