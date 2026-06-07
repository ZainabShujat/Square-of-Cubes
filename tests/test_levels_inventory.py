from core.levels import LEARNING_LEVELS, get_deadzone_limit, inventory_total_area


def test_learning_levels_inventory_area():
    for lvl in LEARNING_LEVELS:
        inv = lvl.inventory
        assert inventory_total_area(inv) == lvl.board_size * lvl.board_size


def test_learning_level_deadzone_allowance_bands():
    expected = {
        1: 2,
        8: 2,
        9: 3,
        18: 3,
        19: 4,
        27: 4,
    }

    for level_number, allowance in expected.items():
        assert get_deadzone_limit(level_number) == allowance

    for lvl in LEARNING_LEVELS:
        assert lvl.deadzone_limit == get_deadzone_limit(lvl.number)

