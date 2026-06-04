from core.levels import LEARNING_LEVELS
from core.solver import level_is_solvable


def test_level_is_solvable_area_mismatch():
    assert level_is_solvable(4, {3: 1, 1: 1}) is False


def test_level_is_solvable_simple_full_tile():
    assert level_is_solvable(4, {4: 1}) is True


def test_first_learning_level_is_solvable():
    level = LEARNING_LEVELS[0]
    assert level_is_solvable(level.board_size, level.inventory, max_nodes=60000) is True
