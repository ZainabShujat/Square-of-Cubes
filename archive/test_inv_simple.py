# Simulate just the inventory generation logic without importing core.levels

# get_max_tile formula
def get_max_tile(board_size):
    if board_size < 10:
        return board_size // 2
    elif board_size < 20:
        return board_size // 3
    else:
        return board_size // 4

# Test for board_size 4
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

print(f"Final inventory: {base}")
print(f"Total area: {sum(s*s * c for s, c in base.items())}")

# Test for all board sizes
print("\nInventory generation for all board sizes:")
for board_size in [4, 6, 8, 9, 10, 12]:
    max_tile = get_max_tile(board_size)
    base = {s: 1 for s in range(1, max_tile + 1)}
    used_area = sum(s * s for s in range(1, max_tile + 1))
    remaining = board_size * board_size - used_area
    if remaining > 0:
        base[1] = base.get(1, 0) + remaining
    total_area = sum(s*s * c for s, c in base.items())
    print(f"  Board {board_size}x{board_size}: max_tile={max_tile}, inventory={base}, area={total_area}")
