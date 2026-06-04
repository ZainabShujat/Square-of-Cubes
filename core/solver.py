from core.board import Board
from core.fitmap import FitMap
from core.placements import PlacementGenerator
from core.piece import Piece
from core.state import GameState


def board_signature(board, state):
    occupied = tuple(sorted(board.get_occupied_cells(state)))
    inventory = tuple(sorted((size, count) for size, count in state.remaining_tiles.items() if count > 0))
    return occupied, inventory


class Solver:

    def __init__(self, board, placement_generator, max_nodes=250000):
        self.board = board
        self.placement_generator = placement_generator
        self.max_nodes = max_nodes
        self.visited = set()
        self.nodes = 0

    def _quick_prune(self, state):
        remaining_areas = [size * size for size, count in state.remaining_tiles.items() if count > 0]
        if not remaining_areas:
            return False

        smallest = min(remaining_areas)
        for region in self.board.get_regions(state):
            if len(region) < smallest:
                return True

        return False

    def can_solve(self, state):
        self.visited.clear()
        self.nodes = 0
        return self._dfs(state)

    def _dfs(self, state):
        if self.board.is_full(state):
            return True

        if self.nodes >= self.max_nodes:
            return False

        key = board_signature(self.board, state)
        if key in self.visited:
            return False
        self.visited.add(key)

        placements = self.placement_generator.generate_all(state)
        sizes = [size for size, count in state.remaining_tiles.items() if count > 0]

        if not sizes:
            return self.board.is_full(state)

        # If any remaining size has no legal placements right now, no later move can create space for it.
        for size in sizes:
            if not placements.get(size):
                return False

        # Most constrained first, tie-break by larger size.
        sizes.sort(key=lambda size: (len(placements.get(size, [])), -size))
        size = sizes[0]

        for x, y in placements[size]:
            self.nodes += 1
            if self.nodes >= self.max_nodes:
                return False

            if not self.board.can_place(state, size, x, y):
                continue

            piece = Piece(size, x, y)
            state.add_piece(piece)
            state.take_tile(size)

            blocked = self._quick_prune(state)
            solved = (not blocked) and self._dfs(state)

            state.remove_piece(piece)
            state.return_tile(size)

            if solved:
                return True

        return False


def level_is_solvable(board_size, inventory, max_nodes=250000):
    total_area = sum(size * size * count for size, count in inventory.items())
    # Do not require inventory area to exactly equal board area.
    # Inventory may contain extra (unused) tiles; only fail when
    # the total available area is insufficient to fill the board.
    if total_area < board_size * board_size:
        return False

    board = Board(board_size)
    fitmap = FitMap(board)
    placement_generator = PlacementGenerator(board, fitmap)
    state = GameState(initial_tile_counts=inventory)

    solver = Solver(board, placement_generator, max_nodes=max_nodes)
    return solver.can_solve(state)
