from core.board import Board
from core.state import GameState
from core.piece import Piece
from core.fitmap import FitMap
from core.placements import PlacementGenerator


def test_placement_generator_returns_moves():
    state = GameState()
    board = Board(size=10)
    # add a blocker
    state.add_piece(Piece(3, 4, 4))
    fitmap = FitMap(board)
    gen = PlacementGenerator(board, fitmap)
    placements = gen.generate_all(state)
    assert isinstance(placements, dict)
    total = sum(len(v) for v in placements.values())
    assert total > 0
    assert gen.total_moves(state) == total
