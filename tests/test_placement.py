from core.board import Board
from core.state import GameState
from core.piece import Piece
from core.fitmap import FitMap
from core.placements import PlacementGenerator


state = GameState()

board = Board()

# blockers
state.add_piece(Piece(4, 0, 0))
state.add_piece(Piece(3, 8, 8))
state.add_piece(Piece(2, 15, 15))

fitmap = FitMap(board)

generator = PlacementGenerator(
    board,
    fitmap
)

placements = generator.generate_all(state)

# =====================================================
# PRINT RESULTS
# =====================================================

for size in sorted(placements.keys()):

    print(f"\nSIZE {size}x{size}")
    print(f"COUNT: {len(placements[size])}")

    print(
        placements[size][:10]
    )

print()

print("TOTAL MOVES:")
print(generator.total_moves(state))