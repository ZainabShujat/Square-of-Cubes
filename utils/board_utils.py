# utils/board_utils.py

from utils.constants import BOARD_SIZE


# =====================================================
# BOUNDS
# =====================================================

def is_in_bounds(x, y):

    return (
        0 <= x < BOARD_SIZE
        and
        0 <= y < BOARD_SIZE
    )


# =====================================================
# NEIGHBORS
# =====================================================

def get_neighbors(x, y):

    neighbors = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1)
    ]

    valid = []

    for nx, ny in neighbors:

        if is_in_bounds(nx, ny):

            valid.append((nx, ny))

    return valid


# =====================================================
# 8-DIRECTIONAL NEIGHBORS
# =====================================================

def get_all_neighbors(x, y):

    directions = [

        (-1, -1),
        (0, -1),
        (1, -1),

        (-1, 0),
        (1, 0),

        (-1, 1),
        (0, 1),
        (1, 1)
    ]

    valid = []

    for dx, dy in directions:

        nx = x + dx
        ny = y + dy

        if is_in_bounds(nx, ny):

            valid.append((nx, ny))

    return valid


# =====================================================
# MANHATTAN DISTANCE
# =====================================================

def manhattan_distance(x1, y1, x2, y2):

    return abs(x1 - x2) + abs(y1 - y2)