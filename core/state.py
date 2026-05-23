from core.piece import Piece
from utils.constants import INITIAL_TILE_COUNTS


class GameState:

    def __init__(self):
        self.solvable = True

        # =========================
        # board pieces
        # =========================

        self.placed_pieces = []

        # =========================
        # inventory
        # =========================

        self.remaining_tiles = INITIAL_TILE_COUNTS.copy()

        # =========================
        # selected tile size
        # =========================

        self.selected_size = None

        # =========================
        # dragging state
        # =========================

        self.dragging_piece = None

        # =========================
        # preview
        # =========================

        self.preview_x = None
        self.preview_y = None

        self.preview_valid = False

        # =========================
        # analysis
        # =========================

        self.dead_regions = []

        self.score = 0

        self.analysis_dirty = True

    # =====================================================
    # INVENTORY
    # =====================================================

    def can_take_tile(self, size):

        return self.remaining_tiles[size] > 0

    def take_tile(self, size):

        if self.can_take_tile(size):

            self.remaining_tiles[size] -= 1
            self.analysis_dirty = True

            return True

        return False

    def return_tile(self, size):

        self.remaining_tiles[size] += 1
        self.analysis_dirty = True

    # =====================================================
    # PIECES
    # =====================================================

    def add_piece(self, piece):

        self.placed_pieces.append(piece)
        self.analysis_dirty = True

    def remove_piece(self, piece):

        if piece in self.placed_pieces:
            self.placed_pieces.remove(piece)
            self.analysis_dirty = True

    # =====================================================
    # BOARD LOOKUP
    # =====================================================

    def get_piece_at(self, grid_x, grid_y):

        for piece in reversed(self.placed_pieces):

            if piece.contains(grid_x, grid_y):
                return piece

        return None