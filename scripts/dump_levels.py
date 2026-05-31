import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.levels import LEARNING_LEVELS, get_max_tile, inventory_summary, inventory_tile_count, inventory_total_area

print('Level | Board | MaxTile | Inventory Summary | Tiles | Score | 1x1 | 2x2 | %tiny | AllSizes1..k')
for lvl in LEARNING_LEVELS:
    board = lvl.board_size
    inv = lvl.inventory
    max_tile = get_max_tile(board)
    ones = inv.get(1, 0)
    twos = inv.get(2, 0)
    tiny = ones + twos
    tile_count = inventory_tile_count(inv)
    pct_tiny = (tiny / tile_count * 100) if tile_count else 0
    # check presence of sizes 1..max_tile
    has_all = all(inv.get(s, 0) > 0 for s in range(1, max_tile + 1))
    print(f"{lvl.number:3d} | {board:5d} | {max_tile:7d} | {inventory_summary(inv):30s} | {tile_count:5d} | {lvl.score:5d} | {ones:3d} | {twos:3d} | {pct_tiny:5.1f}% | {has_all}")
