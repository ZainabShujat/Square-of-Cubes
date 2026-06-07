from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PracticeLevel:

    number: int
    board_size: int
    inventory: dict
    deadzone_limit: int
    description: str
    score: int


def is_prime(number):

    if number < 2:
        return False

    for factor in range(2, int(number ** 0.5) + 1):

        if number % factor == 0:
            return False

    return True


def get_max_tile(board_size):

    if board_size < 10:
        max_tile = board_size // 2
    elif board_size < 20:
        max_tile = board_size // 3
    else:
        max_tile = board_size // 4

    return max(1, min(9, max_tile))


def get_deadzone_limit(level_number):

    if level_number < 9:
        return 2

    if level_number <= 18:
        return 3

    return 4


def inventory_total_area(inventory):

    return sum(
        size * size * count
        for size, count in inventory.items()
    )


def inventory_tile_count(inventory):

    return sum(inventory.values())


def inventory_largest_size(inventory):

    if not inventory:
        return 0

    return max(inventory)


def inventory_summary(inventory):

    parts = []

    for size in sorted(inventory.keys(), reverse=True):

        count = inventory[size]

        if count > 0:
            parts.append(f"{count}x{size}x{size}")

    return ", ".join(parts)


def score_inventory_candidate(board_size, max_tile, inventory, root_size):

    tile_count = inventory_tile_count(inventory)
    ones = inventory.get(1, 0)
    twos = inventory.get(2, 0)
    diversity = len(inventory)
    largest_count = inventory.get(max_tile, 0)
    largest_share = largest_count / max(1, tile_count)
    tiny_tiles = ones + twos
    mid_tiles = sum(
        count
        for size, count in inventory.items()
        if 3 <= size < max_tile
    )
    largest_only = len(inventory) == 1 and inventory.get(max_tile, 0) * max_tile * max_tile == board_size * board_size

    score = 0
    score = 0
    # favor diversity and mid-sized tiles
    score += diversity * 40
    score += mid_tiles * 25
    score += max(0, max_tile - root_size) * 22
    score += int((1.0 - largest_share) * 220)
    # slightly reduce tile_count penalty to prefer fewer tiny tiles
    score -= tile_count * 10
    # harsher penalties for tiny tiles
    score -= ones * 200
    score -= twos * 80
    score -= tiny_tiles * 12

    if ones == 0:
        score += 120

    if twos == 0:
        score += 60

    if diversity >= 5:
        score += 60
    elif diversity >= 4:
        score += 30
    elif diversity >= 3:
        score += 15

    if diversity == 1:
        score -= 1000

    if largest_only:
        score -= 1000

    return score

def score_inventory_structure(stats):

    score = 0

    score += stats.get("split_points", 0) * 130
    score += stats.get("branch_points", 0) * 55
    score += stats.get("distinct_sizes", 0) * 85
    score += stats.get("placements", 0) * 12
    score += stats.get("largest_gap", 0) * 14
    score -= stats.get("tiny_tiles", 0) * 300
    score -= stats.get("single_size_tiles", 0) * 200
    score -= stats.get("dominant_size_count", 0) * 40

    if stats.get("has_size_one"):
        score -= 500

    if stats.get("has_size_two"):
        score -= 200

    if stats.get("split_points", 0) >= 2:
        score += 120

    if stats.get("branch_points", 0) >= 2:
        score += 80

    if stats.get("distinct_sizes", 0) >= 3:
        score += 100


    if stats.get("placements", 0) >= 8:
        score += 60

    return score


def fill_area_greedy(area, max_tile):
    """Fill integer area exactly with square tiles using a greedy largest-first approach."""
    result = {}
    remaining = area
    while remaining > 0:
        s = min(max_tile, int(math.floor(math.sqrt(remaining))))
        if s <= 0:
            break
        count = remaining // (s * s)
        if count <= 0:
            s -= 1
            continue
        result[s] = result.get(s, 0) + count
        remaining -= count * s * s
    if remaining != 0:
        result[1] = result.get(1, 0) + remaining
        remaining = 0
    return result


def enforce_min_sizes(inventory, max_tile, board_area):
    """Force at least one tile of each size 1..max_tile.

    This implementation is simpler and more deterministic: it first adds
    one of each missing size, then removes whole tiles (largest-first)
    to restore the total area, and finally fills any small remainder
    using the greedy filler. This guarantees presence of each size while
    keeping total area equal to board_area.
    """
    inv = dict(inventory)

    # identify missing sizes and add one of each
    missing = [s for s in range(1, max_tile + 1) if inv.get(s, 0) == 0]
    if not missing:
        return inv

    for s in missing:
        inv[s] = inv.get(s, 0) + 1

    # compute area delta after adding missing tiles
    current = inventory_total_area(inv)
    delta = current - board_area

    # if we've increased area, remove whole tiles largest-first while
    # keeping at least one of the newly added sizes
    if delta > 0:
        # first pass: try to preserve at least one of each forced size
        forced_set = set(missing)
        for t in sorted(inv.keys(), reverse=True):
            while delta > 0 and inv.get(t, 0) > (1 if t in forced_set else 0):
                inv[t] -= 1
                if inv[t] == 0:
                    del inv[t]
                delta -= t * t
            if delta <= 0:
                break

        # second pass: if still delta>0, remove any remaining tiles
        if delta > 0:
            for t in sorted(inv.keys(), reverse=True):
                while delta > 0 and inv.get(t, 0) > 0:
                    inv[t] -= 1
                    if inv[t] == 0:
                        del inv[t]
                    delta -= t * t
                if delta <= 0:
                    break

    # if we've removed too much (delta < 0), fill the remainder greedily
    if delta < 0:
        filler = fill_area_greedy(-delta, max_tile)
        for fs, fc in filler.items():
            inv[fs] = inv.get(fs, 0) + fc

    # final normalization: remove zero/negative entries
    for kx in list(inv.keys()):
        if inv[kx] <= 0:
            del inv[kx]

    # ensure total area equals board_area (final safeguard)
    total = inventory_total_area(inv)
    if total != board_area:
        # try greedy fill or trim 1x1s to match exactly
        if total < board_area:
            filler = fill_area_greedy(board_area - total, max_tile)
            for fs, fc in filler.items():
                inv[fs] = inv.get(fs, 0) + fc
        elif total > board_area:
            # remove excess by trimming 1x1s, then 2x2s, etc.
            excess = total - board_area
            for t in sorted(inv.keys(), reverse=True):
                while excess > 0 and inv.get(t, 0) > 0:
                    inv[t] -= 1
                    if inv[t] == 0:
                        del inv[t]
                    excess -= t * t
                if excess <= 0:
                    break

    return inv


def ensure_min_sizes_present(inventory, max_tile):
    """Ensure at least one tile of each size 1..max_tile is present."""
    inv = dict(inventory)
    for s in range(1, max_tile + 1):
        if inv.get(s, 0) == 0:
            inv[s] = 1
    return inv


def compute_stats_from_inventory(board_size, inventory):
    stats = {}
    distinct = len([s for s, c in inventory.items() if c > 0])
    stats["distinct_sizes"] = distinct
    stats["tiny_tiles"] = inventory.get(1, 0) + inventory.get(2, 0)
    stats["has_size_one"] = inventory.get(1, 0) > 0
    stats["has_size_two"] = inventory.get(2, 0) > 0
    stats["single_size_tiles"] = 1 if distinct == 1 else 0
    stats["dominant_size_count"] = max(inventory.values()) if inventory else 0
    placements = 0
    for s, c in inventory.items():
        placements += max(0, (board_size - s + 1)) ** 2
    stats["placements"] = placements
    stats["split_points"] = max(0, distinct // 2)
    stats["branch_points"] = max(0, distinct // 3)
    stats["largest_gap"] = board_size - max(inventory.keys()) if inventory else 0
    # placement graph using PlacementGenerator
    try:
        from core.board import Board
        from core.fitmap import FitMap
        from core.placements import PlacementGenerator
        from core.state import GameState

        board = Board(board_size)
        fitmap = FitMap(board)
        state = GameState(initial_tile_counts=inventory)
        placement_gen = PlacementGenerator(board, fitmap)
        placements = placement_gen.generate_all(state)
        total_placements = sum(len(v) for v in placements.values())
        branching_sizes = sum(1 for v in placements.values() if len(v) > 1)
        stats["placements"] = total_placements
        stats["branching_sizes"] = branching_sizes
    except Exception:
        stats["placements"] = stats.get("placements", 0)
        stats["branching_sizes"] = 0
    return stats


def find_best_composition_for_small_board(board_size, max_tile, enforce_all_sizes=True):
    """Brute-force search for small boards to find a composition that minimizes tiny tiles.
    Returns inventory dict or None.
    """
    area = board_size * board_size
    sizes = list(range(max_tile, 0, -1))

    # if enforcing all sizes, check minimal area
    if enforce_all_sizes:
        min_area = sum(s * s for s in range(1, max_tile + 1))
        if min_area > area:
            return None

    best = None

    def score_candidate(inv):
        tiny = inv.get(1, 0) + inv.get(2, 0)
        total = sum(inv.values())
        # lower is better
        return (tiny, total)

    def dfs(idx, remaining, inv):
        nonlocal best
        if remaining < 0:
            return
        if idx == len(sizes):
            if remaining == 0:
                # check enforce_all_sizes
                if enforce_all_sizes:
                    ok = all(inv.get(s, 0) > 0 for s in range(1, max_tile + 1))
                    if not ok:
                        return
                sc = score_candidate(inv)
                if best is None or sc < best[0]:
                    best = (sc, dict(inv))
            return

        s = sizes[idx]
        max_count = remaining // (s * s)
        min_count = 1 if (enforce_all_sizes and s <= max_tile) else 0
        # cap search to reasonable numbers
        for cnt in range(min_count, max_count + 1):
            if cnt > 0:
                inv[s] = inv.get(s, 0) + cnt
            dfs(idx + 1, remaining - cnt * s * s, inv)
            if cnt > 0:
                inv[s] -= cnt
                if inv[s] <= 0:
                    del inv[s]

    dfs(0, area, {})

    return best[1] if best else None

    return score


def choose_root_sizes(board_size, max_tile):

    sizes = []

    preferred = [
        max(1, max_tile - 1),
        max(1, max_tile - 2),
        max(1, max_tile - 3),
        max(2, max_tile // 2),
    ]

    for size in preferred:
        if size <= max_tile and size not in sizes:
            sizes.append(size)

    return sizes


def choose_square_size(width, height, max_tile, style_name, depth, root_size):

    short = min(width, height)

    if short <= 1:
        return 1

    if depth == 0:
        return max(1, min(short, root_size))

    # Bias toward larger squares to avoid many 1x1 tiles
    base = min(max_tile, short)
    if style_name == "corridor":
        target = base
    elif style_name == "fragmented":
        target = base
        if depth % 2 == 1 and target > 2:
            target -= 1
    elif style_name == "balanced":
        # balanced favors medium sizes
        target = max(2, base - (depth // 2))
    else:
        target = base

    # when depth increases, slightly prefer larger tiles to avoid fragmentation
    if depth >= 3:
        target = max(target, min(base, short))

    # avoid returning 1 unless short==1
    if target <= 1 and short > 1:
        target = min(base, 2)

    return max(1, target)


def tile_rectangle(width, height, max_tile, style_name, root_size, depth=0):

    inventory = {}

    def add_square(size, count=1):
        inventory[size] = inventory.get(size, 0) + count

    if width <= 0 or height <= 0:
        return inventory

    if width == 1 and height == 1:
        add_square(1)
        return inventory

    if width == height and width <= 2:
        add_square(width)
        return inventory

    square_size = choose_square_size(
        width,
        height,
        max_tile,
        style_name,
        depth,
        root_size
    )

    if square_size > min(width, height):
        square_size = min(width, height)

    add_square(square_size)

    right_width = width - square_size
    bottom_height = height - square_size

    if right_width > 0:
        right_inventory = tile_rectangle(
            right_width,
            square_size,
            max_tile,
            style_name,
            root_size,
            depth + 1
        )
        for size, count in right_inventory.items():
            add_square(size, count)

    if bottom_height > 0:
        bottom_inventory = tile_rectangle(
            width,
            bottom_height,
            max_tile,
            style_name,
            root_size,
            depth + 1
        )
        for size, count in bottom_inventory.items():
            add_square(size, count)

    return inventory


def normalize_inventory(inventory):

    return {
        size: count
        for size, count in sorted(inventory.items())
        if count > 0
    }


def merge_small_tiles(inventory, max_tile):
    """Greedily merge groups of small tiles into larger squares to reduce 1x1/2x2 counts."""
    inv = dict(inventory)
    # try merging small tiles aggressively
    inv = dict(inv)
    # total small area (sizes 1 and 2 prioritized)
    small_threshold = 2
    small_area = sum(sz * sz * cnt for sz, cnt in inv.items() if sz <= small_threshold)
    # attempt to create as many large squares as possible from small_area
    if small_area >= 4:
        # prefer largest target up to max_tile that fits into small_area
        while small_area >= 4:
            target = min(max_tile, int(math.floor(math.sqrt(small_area))))
            if target <= small_threshold:
                break
            area = target * target
            # consume tiles to free 'area'
            need_area = area
            for s in sorted([sz for sz in inv.keys() if sz <= small_threshold], reverse=True):
                while inv.get(s, 0) > 0 and need_area > 0:
                    take_cells = min(inv[s], need_area // (s * s))
                    if take_cells <= 0:
                        break
                    inv[s] -= take_cells
                    if inv[s] == 0:
                        del inv[s]
                    need_area -= take_cells * s * s
            if need_area == 0:
                inv[target] = inv.get(target, 0) + 1
                small_area -= area
            else:
                # cannot form this target from small-only; stop
                break

    # fallback: previous merging logic to combine various small tiles into larger ones
    for target in range(min(max_tile, 9), 2, -1):
        area = target * target
        made_progress = True
        while made_progress:
            made_progress = False
            total_small_area = sum(sz * sz * cnt for sz, cnt in inv.items() if sz < target)
            if total_small_area < area:
                break
            need_area = area
            # consume largest small tiles first
            for s in sorted([sz for sz in inv.keys() if sz < target], reverse=True):
                while inv.get(s, 0) > 0 and need_area > 0:
                    take = min(inv[s], need_area // (s * s))
                    if take <= 0:
                        break
                    inv[s] -= take
                    if inv[s] == 0:
                        del inv[s]
                    need_area -= take * s * s
            if need_area == 0:
                inv[target] = inv.get(target, 0) + 1
                made_progress = True

    # for any remaining small area, try to compose with fill_area_greedy
    remaining_area = sum(sz * sz * cnt for sz, cnt in inv.items())
    total_area = sum(sz * sz * cnt for sz, cnt in inventory.items())
    leftover = total_area - remaining_area
    if leftover > 0:
        filler = fill_area_greedy(leftover, max_tile)
        for fs, fc in filler.items():
            inv[fs] = inv.get(fs, 0) + fc

    # clean zeros
    for kx in list(inv.keys()):
        if inv[kx] <= 0:
            del inv[kx]
    return inv


def inventory_is_trivial(board_size, max_tile, inventory):

    if len(inventory) != 1:
        return False

    size = next(iter(inventory.keys()))

    return board_size % size == 0

def inventory_is_structurally_rich(board_size, inventory, stats):

    tile_count = inventory_tile_count(inventory)

    # Allow inventory area to exceed board area (extra tiles permitted).
    # Only reject when insufficient area to fill the board.
    if inventory_total_area(inventory) < board_size * board_size:
        return False

    if inventory_is_trivial(board_size, get_max_tile(board_size), inventory):
        return False

    if tile_count < 2:
        return False

    if len(inventory) < 2 and board_size >= 6:
        return False

    if stats.get("split_points", 0) <= 0:
        return False

    if board_size >= 8 and stats.get("split_points", 0) < 2:
        return False

    if stats.get("placements", 0) < 4 and board_size >= 6:
        return False

    # require some branching (multiple placement possibilities) for larger boards
    if board_size >= 6 and stats.get("branching_sizes", 0) < max(2, stats.get("distinct_sizes", 0) // 2):
        return False

    # require a minimum number of placements proportional to board size
    if stats.get("placements", 0) < max(6, board_size // 3):
        return False

    if stats.get("dominant_size_count", 0) > max(3, tile_count - 1):
        return False

    if stats.get("has_size_one", 0) and board_size >= 10:
        return False

    if stats.get("has_size_two", 0) and board_size >= 14 and len(inventory) == 2:
        return False

    if stats.get("small_tiles", 0) > max(2, tile_count // 2):
        return False

    return True


def generate_inventory(board_size):

    """Generate a valid inventory for the given board_size.
    
    Conservative approach: one-of-each-size (1..max_tile) + 1x1 fillers.
    """
    max_tile = get_max_tile(board_size)

    def max_ones_allowed(board_size):
        if board_size <= 10:
            return 2
        if board_size <= 20:
            return 4
        if board_size <= 30:
            return 6
        return 8

    # Start with one of each size (1..max_tile)
    base = {s: 1 for s in range(1, max_tile + 1)}
    used_area = sum(s * s for s in range(1, max_tile + 1))
    remaining = board_size * board_size - used_area

    # Bounded fill: try to fill remaining area using sizes from large->small
    # while ensuring total 1x1 count does not exceed allowed limit.
    allowed_ones = max_ones_allowed(board_size)
    # we already have one 1x1 in base
    remaining_ones_allowed = max(0, allowed_ones - base.get(1, 0))

    sizes_desc = list(range(max_tile, 0, -1))

    # recursive bounded fill that prefers larger tiles (tries larger counts first)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def try_fill(idx, rem, ones_left):
        if rem == 0:
            return ()
        if idx >= len(sizes_desc):
            return None
        s = sizes_desc[idx]
        area = s * s
        if s == 1:
            max_cnt = min(ones_left, rem)
        else:
            max_cnt = rem // area

        for cnt in range(max_cnt, -1, -1):
            next_rem = rem - cnt * area
            next_ones = ones_left - cnt if s == 1 else ones_left
            if next_ones < 0:
                continue
            res = try_fill(idx + 1, next_rem, next_ones)
            if res is not None:
                return (cnt,) + res
        return None

    extra_counts = try_fill(0, remaining, remaining_ones_allowed)

    if extra_counts is None:
        # As a conservative fallback, fill greedily but cap ones to allowed_ones
        extra = {}
        rem = remaining
        for s in sizes_desc:
            if s == 1:
                cnt = min(remaining_ones_allowed, rem)
            else:
                cnt = rem // (s * s)
            extra[s] = cnt
            rem -= cnt * s * s

        # If still leftover, reduce larger tiles to try to fit exact area by replacing
        # with smaller tiles; simplest fallback: allow ones to fill any leftover (may exceed cap)
        if rem > 0:
            extra[1] = extra.get(1, 0) + rem

        for s, cnt in extra.items():
            base[s] = base.get(s, 0) + cnt

        base = normalize_inventory(base)
        return {
            "board_size": board_size,
            "inventory": base,
            "total_area": board_size * board_size,
            "tile_count": inventory_tile_count(base),
            "score": 0,
        }

    # apply extra_counts to base
    for s, add_cnt in zip(sizes_desc, extra_counts):
        if add_cnt:
            base[s] = base.get(s, 0) + add_cnt

    base = normalize_inventory(base)
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
                score=inventory_info["score"]
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
