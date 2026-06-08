from core.board import Board
from core.state import GameState
from core.piece import Piece
from core.fitmap import FitMap
from core.deadzones import DeadzoneDetector


state = GameState()

board = Board()

# =====================================================
# CREATE TEST GEOMETRY
# =====================================================

# create thin corridor traps

for x in range(10, 20):

    state.add_piece(
        Piece(1, x, 10)
    )

    state.add_piece(
        Piece(1, x, 12)
    )

# =====================================================
# REMOVE 1x1 TILES
# =====================================================

state.remaining_tiles[1] = 0

# =====================================================
# RUN DETECTOR
# =====================================================

fitmap = FitMap(board)

detector = DeadzoneDetector(
    board,
    fitmap
)

dead_cells = detector.find_dead_cells(state)

dead_regions = detector.find_dead_regions(state)

# =====================================================
# RESULTS
# =====================================================

print()

print("DEAD CELL COUNT:")
print(len(dead_cells))

print()

print("DEAD REGION COUNT:")
print(len(dead_regions))

print()

print("SAMPLE DEAD CELLS:")
print(list(dead_cells)[:20])