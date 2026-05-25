from core.board import Board
from core.state import GameState
from core.piece import Piece
from core.fitmap import FitMap
from core.placements import PlacementGenerator


# =====================================================
# PRETTY PRINT
# =====================================================

def print_map(grid):

    for row in grid:

        print(
            " ".join(f"{cell:2}" for cell in row)
        )

    print()


# =====================================================
# CREATE TEST STATE
# =====================================================

state = GameState()

board = Board()

# =====================================================
# ADD TEST PIECES
# =====================================================

# obstacle 1
state.add_piece(
    Piece(4, 5, 5)
)

# obstacle 2
state.add_piece(
    Piece(3, 15, 10)
)

# obstacle 3
state.add_piece(
    Piece(2, 25, 25)
)

# =====================================================
# COMPUTE FITMAP
# =====================================================

fitmap = FitMap(board)

fitmap.compute(state)

# =====================================================
# PRINT FITMAP
# =====================================================

print("\nFITMAP:\n")

print_map(
    fitmap.get_map()
)

# =====================================================
# TEST PLACEMENTS
# =====================================================

generator = PlacementGenerator(
    board,
    fitmap
)

placements = generator.generate_all(state)

print("\nPLACEMENTS:\n")

for size in sorted(placements.keys()):

    print(
        f"{size}x{size}: "
        f"{len(placements[size])}"
    )

# =====================================================
# SAMPLE QUERIES
# =====================================================

print("\nSAMPLE FIT VALUES:\n")

print(
    "(0,0):",
    fitmap.largest_square_at(0, 0)
)

print(
    "(5,5):",
    fitmap.largest_square_at(5, 5)
)

print(
    "(10,10):",
    fitmap.largest_square_at(10, 10)
)