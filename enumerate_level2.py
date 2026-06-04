"""
Developer diagnostic: enumerate_level2.py

Exhaustively enumerates all inventories for a 6x6 board satisfying:
- at least one tile of each size 1..3
- max 2 tiles of size 1x1
- total area exactly 36

For each inventory it runs core.solver.level_is_solvable and prints PASS/FAIL.
Finally prints all passing inventories sorted by:
  1) fewest 1x1 tiles
  2) fewest total tiles
  3) largest average tile size

Run:
    python enumerate_level2.py
"""

import sys
from core.solver import level_is_solvable

BOARD_SIZE = 6
MAX_ONES = 2


def main():
    # increase recursion limit for solver
    sys.setrecursionlimit(10000)

    passing = []
    checked = 0

    for c1 in range(1, MAX_ONES + 1):
        # c2 at least 1
        for c2 in range(1, 36 // 4 + 1):
            rem = 36 - (1 * c1 + 4 * c2)
            if rem <= 0:
                continue
            if rem % 9 != 0:
                continue
            c3 = rem // 9
            if c3 < 1:
                continue

            inv = {1: c1, 2: c2, 3: c3}
            checked += 1
            try:
                solvable = level_is_solvable(BOARD_SIZE, inv)
            except RecursionError:
                solvable = False
            except Exception:
                solvable = False

            status = 'PASS' if solvable else 'FAIL'
            print(f"Inventory {inv} -> {status}")

            if solvable:
                tile_count = sum(inv.values())
                avg_tile_size = sum(size * count for size, count in inv.items()) / tile_count
                passing.append((inv, c1, tile_count, avg_tile_size))

    print('\nChecked inventories:', checked)

    if not passing:
        print('No passing inventories found under the constraints.')
        return

    # sort by (fewest ones, fewest tiles, largest avg tile size)
    passing.sort(key=lambda item: (item[1], item[2], -item[3]))

    print('\nPassing inventories (sorted):')
    for inv, ones, tile_count, avg in passing:
        print(f"Ones={ones} | Tiles={tile_count} | AvgSize={avg:.2f} | Inv={inv}")


if __name__ == '__main__':
    main()
