import copy

from core.piece import Piece


class HistoryManager:

    def __init__(self):

        self.undo_stack = []

    # =====================================================
    # SAVE
    # =====================================================

    def save_state(self, state):

        snapshot = {

            "placed_pieces": [
                Piece(
                    piece.size,
                    piece.grid_x,
                    piece.grid_y
                )
                for piece in state.placed_pieces
            ],

            "remaining_tiles": copy.deepcopy(
                state.remaining_tiles
            ),

            "score": state.score,

            "dead_regions": copy.deepcopy(
                state.dead_regions
            )
        }

        self.undo_stack.append(snapshot)

    # =====================================================
    # UNDO
    # =====================================================

    def undo(self, state):

        if not self.undo_stack:
            return

        snapshot = self.undo_stack.pop()

        state.placed_pieces = snapshot[
            "placed_pieces"
        ]

        state.remaining_tiles = snapshot[
            "remaining_tiles"
        ]

        state.score = snapshot[
            "score"
        ]

        state.dead_regions = snapshot[
            "dead_regions"
        ]

        state.analysis_dirty = True