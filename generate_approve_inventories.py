"""
Developer tool: generate_approve_inventories.py

Searches candidate inventories for failing practice levels, validates with
core.solver.level_is_solvable, scores successful inventories, and saves the
best inventory per level to `approved_inventories.json`.

This script is developer-only and must not run during game startup.

Usage:
    python generate_approve_inventories.py [--candidates N] [--max_nodes M]

Defaults: N=1000, M=120000
"""

import argparse
import json
import random
import time
from collections import defaultdict

from core.levels import LEARNING_LEVELS, get_max_tile, inventory_total_area, inventory_tile_count, score_inventory_candidate
from core.solver import level_is_solvable

OUTFILE = "approved_inventories.json"


def max_ones_allowed(board_size):
    if board_size <= 10:
        return 2
    if board_size <= 20:
        return 4
    if board_size <= 30:
        return 6
    return 8


def generate_candidate(board_size, max_tile, ones_cap):
    # Start with one of each size to satisfy the "all sizes present" requirement
    inv = {s: 1 for s in range(1, max_tile + 1)}
    board_area = board_size * board_size
    used = sum(s * s for s in range(1, max_tile + 1))
    remaining = board_area - used

    # If no remaining area, return base (may be overspecified)
    if remaining <= 0:
        # In this case base already equals or exceeds area; may include extra that make it solvable
        return normalize(inv)

    # Try to add larger tiles first with some randomness; do not exceed ones_cap for 1x1.
    sizes = list(range(max_tile, 1, -1))  # exclude 1 for now
    for s in sizes:
        area = s * s
        # choose up to remaining//area tiles, but keep small cap to limit tile counts
        max_possible = remaining // area
        if max_possible <= 0:
            continue
        # bias toward adding fewer larger tiles (avoid bloated counts)
        cnt = random.choices(
            population=list(range(0, max_possible + 1)),
            weights=[(max_possible - i + 1) for i in range(0, max_possible + 1)],
            k=1
        )[0]
        if cnt:
            inv[s] = inv.get(s, 0) + cnt
            remaining -= cnt * area

    # Fill remaining with 2x2 and then 1x1 bounded
    if remaining > 0:
        # try 2x2
        s = 2
        area = 4
        cnt = remaining // area
        if cnt:
            inv[2] = inv.get(2, 0) + cnt
            remaining -= cnt * area

    if remaining > 0:
        # use 1x1 up to ones_cap
        existing_ones = inv.get(1, 0)
        can_add = max(0, ones_cap - existing_ones)
        add = min(can_add, remaining)
        inv[1] = inv.get(1, 0) + add
        remaining -= add

    # If still remaining (couldn't fill due to ones cap), randomly add a medium tile to exceed area
    if remaining > 0:
        s = random.randint(2, max_tile)
        inv[s] = inv.get(s, 0) + 1

    return normalize(inv)


# small helper to ensure no zero-counts and dict keys sorted
def normalize(inv):
    return {int(k): int(v) for k, v in sorted(inv.items()) if v and k > 0}


def score_inv(board_size, max_tile, inventory):
    # Use existing scoring helper if available; try to pass a reasonable root_size
    try:
        root_size = max(inventory.keys())
        return score_inventory_candidate(board_size, max_tile, inventory, root_size)
    except Exception:
        # fallback scoring: fewer tiles, fewer ones, prefer mid sizes
        tile_count = inventory_tile_count(inventory)
        ones = inventory.get(1, 0)
        mid = sum(count for size, count in inventory.items() if 3 <= size < max_tile)
        return mid * 30 - tile_count * 10 - ones * 100


def find_best_for_level(lvl, candidates=1000, max_nodes=120000, seed=None):
    random.seed(seed)
    board_size = lvl.board_size
    max_tile = get_max_tile(board_size)
    ones_cap = max_ones_allowed(board_size)

    best = None
    best_score = float('-inf')
    found = 0
    start = time.time()
    for i in range(candidates):
        cand = generate_candidate(board_size, max_tile, ones_cap)
        # allow extra inventory area, ensure non-empty
        if inventory_total_area(cand) < board_size * board_size:
            continue
        # validate with solver
        solvable = level_is_solvable(board_size, cand, max_nodes=max_nodes)
        if not solvable:
            continue
        found += 1
        s = score_inv(board_size, max_tile, cand)
        if s > best_score:
            best_score = s
            best = {
                'inventory': cand,
                'score': s,
                'tile_count': inventory_tile_count(cand),
                'area': inventory_total_area(cand)
            }
    elapsed = time.time() - start
    return best, found, elapsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidates', type=int, default=800, help='Candidates per failing level')
    parser.add_argument('--max_nodes', type=int, default=120000, help='Solver max nodes')
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()

    # Find failing levels first
    failing = []
    for lvl in LEARNING_LEVELS:
        solvable = level_is_solvable(lvl.board_size, lvl.inventory, max_nodes=args.max_nodes)
        if not solvable:
            failing.append(lvl)

    if not failing:
        print('No failing levels found. Nothing to do.')
        return

    print(f'Found {len(failing)} failing levels: {[l.number for l in failing]}')

    approved = {}
    stats = {}
    for lvl in failing:
        print(f'Processing Level {lvl.number} ({lvl.board_size}x{lvl.board_size})...')
        best, found, elapsed = find_best_for_level(lvl, candidates=args.candidates, max_nodes=args.max_nodes, seed=args.seed)
        if best:
            approved[str(lvl.number)] = best
            print(f'  Found {found} valid candidates, best score {best["score"]}, tile_count {best["tile_count"]}, area {best["area"]} (took {elapsed:.1f}s)')
        else:
            print(f'  No valid candidates found (searched {args.candidates} candidates, {elapsed:.1f}s)')

    # merge approved with existing file if present
    try:
        current = {}
        with open(OUTFILE, 'r', encoding='utf-8') as f:
            current = json.load(f)
    except FileNotFoundError:
        current = {}

    for k, v in approved.items():
        current[k] = v

    with open(OUTFILE, 'w', encoding='utf-8') as f:
        json.dump(current, f, indent=2)

    print(f'Wrote {len(approved)} approved inventories to {OUTFILE}')


if __name__ == '__main__':
    main()
