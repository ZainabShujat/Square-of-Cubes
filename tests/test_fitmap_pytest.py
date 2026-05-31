from core.board import Board
from core.fitmap import FitMap
from core.state import GameState


def test_fitmap_largest_square_on_empty_board():
    board = Board(size=10)
    state = GameState()
    fitmap = FitMap(board)
    fitmap.compute(state)
    # on an empty board, top-left should be able to fit a square of size 10
    assert fitmap.largest_square_at(0, 0) == 10
    m = fitmap.get_map()
    assert len(m) == 10
    assert len(m[0]) == 10
