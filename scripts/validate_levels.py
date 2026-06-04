import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.levels import LEARNING_LEVELS, inventory_total_area
from core.solver import level_is_solvable


def main():
    failing = []

    for level in LEARNING_LEVELS:
        board_size = level.board_size
        inventory = level.inventory
        inv_area = inventory_total_area(inventory)
        board_area = board_size * board_size

        ok = level_is_solvable(board_size, inventory, max_nodes=120000)

        if not ok:
            failing.append(level.number)
            print(f"Level: {level.number}")
            print(f"Board size: {board_size}x{board_size}")
            print(f"Inventory: {inventory}")
            print(f"Total inventory area: {inv_area}")
            print(f"Board area: {board_area}")
            print("-" * 60)

    if not failing:
        print("All levels are solvable.")
    else:
        print(f"Failing levels: {failing}")


if __name__ == '__main__':
    main()
