"""
Pure exhaustive backtracking for Level 2 (6x6) with inventory {1:2,2:4,3:2}.
No heuristics, no pruning, no node limits. Anchor each placement at the first
empty cell (row-major), try every remaining tile size, recurse.

Usage:
    python bruteforce_level2.py
"""
import sys
from time import time

N = 6
TARGET_INV = {1:2, 2:4, 3:2}

# board as list of bools

def find_first_empty(board):
    for i, v in enumerate(board):
        if not v:
            return i
    return None


def can_place(board, r, c, s):
    if r + s > N or c + s > N:
        return False
    for i in range(r, r + s):
        base = i * N
        for j in range(c, c + s):
            if board[base + j]:
                return False
    return True


def place(board, r, c, s, val):
    for i in range(r, r + s):
        base = i * N
        for j in range(c, c + s):
            board[base + j] = val


found_solution = False
nodes = 0
start_time = None


def dfs(board, inv):
    global found_solution, nodes
    if found_solution:
        return True
    idx = find_first_empty(board)
    if idx is None:
        found_solution = True
        return True
    nodes += 1
    r = idx // N
    c = idx % N
    # try each remaining tile size (1..3)
    for s in sorted(inv.keys()):
        if inv[s] <= 0:
            continue
        if not can_place(board, r, c, s):
            continue
        # place
        place(board, r, c, s, True)
        inv[s] -= 1
        dfs(board, inv)
        if found_solution:
            return True
        # backtrack
        inv[s] += 1
        place(board, r, c, s, False)
    return False


def main():
    global found_solution, nodes, start_time
    sys.setrecursionlimit(10000)
    board = [False] * (N * N)
    inv = {k: v for k, v in TARGET_INV.items()}
    start_time = time()
    res = dfs(board, inv)
    duration = time() - start_time
    if found_solution:
        print('FOUND SOLUTION')
    else:
        print('PROVEN UNSOLVABLE')
    print(f'Nodes visited: {nodes}, Time: {duration:.2f}s')

if __name__ == '__main__':
    main()
