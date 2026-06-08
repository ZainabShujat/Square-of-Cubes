from core.player_store import PlayerStore


def test_player_store_creates_default_profile(tmp_path):
    store = PlayerStore(tmp_path / "players.json")

    player = store.active_player()

    assert player is not None
    assert player["name"] == "Player 1"
    assert player["stats"]["games_played"] == 0


def test_player_store_records_level_result(tmp_path):
    store = PlayerStore(tmp_path / "players.json")

    store.record_level_result(
        {
            "outcome": "win",
            "level_number": 3,
            "board_size": 6,
            "deadzone_count": 0,
            "deadzone_limit": 2,
            "gap_count": 0,
            "gap_cells": 0,
            "score": 1200,
            "moves": 9,
            "stars": 3,
        }
    )

    player = store.active_player()

    assert player["stats"]["games_played"] == 1
    assert player["stats"]["wins"] == 1
    assert player["stats"]["best_level"] == 3
    assert player["stats"]["total_stars"] == 3
    assert player["levels"]["3"]["stars"] == 3
    assert len(player["history"]) == 1


def test_player_store_switches_between_profiles(tmp_path):
    store = PlayerStore(tmp_path / "players.json")
    first_id = store.active_player()["id"]

    second = store.create_player("Player 2")
    store.set_active_player(first_id)

    assert store.active_player()["id"] == first_id

    store.set_active_player(second["id"])

    assert store.active_player()["name"] == "Player 2"
