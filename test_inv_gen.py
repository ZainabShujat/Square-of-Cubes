from core.levels import get_max_tile, normalize_inventory, inventory_tile_count

# Test inventory generation for board_size 4
board_size = 4
max_tile = get_max_tile(board_size)
print(f"Board size: {board_size}, max_tile: {max_tile}")

# Create base inventory (one-of-each + 1x1 fillers)
base = {s: 1 for s in range(1, max_tile + 1)}
used_area = sum(s * s for s in range(1, max_tile + 1))
remaining = board_size * board_size - used_area

print(f"Base inventory (before 1x1 fill): {base}")
print(f"Used area from sizes 1..{max_tile}: {used_area}")
print(f"Board area: {board_size * board_size}")
print(f"Remaining area for 1x1 fillers: {remaining}")

if remaining > 0:
    base[1] = base.get(1, 0) + remaining
base = normalize_inventory(base)

print(f"Final inventory: {base}")
print(f"Total area: {sum(s*s * c for s, c in base.items())}")
print(f"Tile count: {inventory_tile_count(base)}")
