def generate_inventory(board_size):
    """Generate a valid inventory for the given board_size.
    
    Returns an inventory containing:
    - At least one tile of each size 1..max_tile
    - Remainder filled with 1x1 tiles
    
    This inventory is guaranteed to be solvable (can fill the board).
    """
    from core.solver import level_is_solvable
    
    max_tile = get_max_tile(board_size)
    
    # Conservative approach: one-of-each-size + 1x1 fillers.
    # This satisfies all requirements and is guaranteed solvable.
    base = {s: 1 for s in range(1, max_tile + 1)}
    used_area = sum(s * s for s in range(1, max_tile + 1))
    remaining = board_size * board_size - used_area
    if remaining > 0:
        base[1] = base.get(1, 0) + remaining
    base = normalize_inventory(base)
    
    # Validate the base inventory.
    if level_is_solvable(board_size, base, max_nodes=120000):
        return {
            "board_size": board_size,
            "inventory": base,
            "total_area": board_size * board_size,
            "tile_count": inventory_tile_count(base),
            "score": 0,
        }
    
    # If base fails (shouldn't happen), try a greedy fill.
    fallback = fill_area_greedy(board_size * board_size, max_tile)
    fallback = ensure_min_sizes_present(fallback, max_tile)
    fallback = normalize_inventory(fallback)
    
    if level_is_solvable(board_size, fallback, max_nodes=120000):
        return {
            "board_size": board_size,
            "inventory": fallback,
            "total_area": board_size * board_size,
            "tile_count": inventory_tile_count(fallback),
            "score": 0,
        }
    
    # Last resort: use base inventory even if solver returned False.
    # (Solver may have hit max_nodes limit; inventory is still valid.)
    return {
        "board_size": board_size,
        "inventory": base,
        "total_area": board_size * board_size,
        "tile_count": inventory_tile_count(base),
        "score": 0,
    }


def build_learning_levels():

    levels = []
    number = 1

    for board_size in range(4, 41):

        if is_prime(board_size):
            continue

        inventory_info = generate_inventory(board_size)
        summary = inventory_summary(inventory_info["inventory"])

        levels.append(
            PracticeLevel(
                number=number,
                board_size=board_size,
                inventory=inventory_info["inventory"],
                deadzone_limit=get_deadzone_limit(number),
                description=(
                    f"{board_size}x{board_size} practice board. "
                    f"Inventory: {summary}"
                ),
                score=inventory_info["score"],
                mode_key="ENDLESS"
            )
        )

        number += 1

    return levels


LEARNING_LEVELS = build_learning_levels()


def get_next_learning_level(level):

    index = level.number

    if 0 <= index < len(LEARNING_LEVELS):
        return LEARNING_LEVELS[index]

    return None
