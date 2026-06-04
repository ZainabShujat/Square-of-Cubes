"""
Developer tool: validate_levels.py

Usage:
    python validate_levels.py

This script imports practice levels (LEARNING_LEVELS) and validates each level
using core.solver.level_is_solvable. It prints PASS/FAIL per level and a final
list of failing level numbers.

This script is intentionally standalone and must not run during the game startup.
"""

import sys
from core.levels import LEARNING_LEVELS, inventory_total_area
from core.solver import level_is_solvable


def main():
    # Increase recursion limit for deep backtracking in the solver.
    sys.setrecursionlimit(10000)

    failing = []

    for lvl in LEARNING_LEVELS:
        number = lvl.number
        board_size = lvl.board_size
        inventory = lvl.inventory
        inv_area = inventory_total_area(inventory)
        board_area = board_size * board_size

        try:
            solvable = level_is_solvable(board_size, inventory)
            status = "PASS" if solvable else "FAIL"
        except RecursionError:
            solvable = False
            status = "FAIL (RecursionError)"
        except Exception as e:
            solvable = False
            status = f"FAIL ({type(e).__name__})"

        print(f"Level {number} | {board_size}x{board_size} | {status}")
        print(f"Inventory area: {inv_area} | Board area: {board_area}")
        print(f"Inventory: {inventory}")
        print()

        if not solvable:
            failing.append(number)

    print("Failing Levels:")
    print(failing)


if __name__ == "__main__":
    main()
