from core.levels import LEARNING_LEVELS, inventory_total_area


def test_learning_levels_inventory_area():
    for lvl in LEARNING_LEVELS:
        inv = lvl.inventory
        assert inventory_total_area(inv) == lvl.board_size * lvl.board_size

