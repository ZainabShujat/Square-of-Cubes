import json
import os
from datetime import datetime, timezone
from pathlib import Path


APP_DIR_NAME = "SumOfCubes"
STORE_FILE_NAME = "players.json"


def default_store_path():

    base_dir = os.environ.get("APPDATA")

    if not base_dir:
        base_dir = os.environ.get("LOCALAPPDATA")

    if not base_dir:
        base_dir = str(Path.home())

    return Path(base_dir) / APP_DIR_NAME / STORE_FILE_NAME


class PlayerStore:

    def __init__(self, path=None):

        self.path = Path(path) if path else default_store_path()
        self.data = self._load()
        self.ensure_active_player()

    def _empty_data(self):

        return {
            "active_player_id": None,
            "players": []
        }

    def _load(self):

        if not self.path.exists():
            return self._empty_data()

        try:
            with self.path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return self._empty_data()

        if not isinstance(data, dict):
            return self._empty_data()

        data.setdefault("active_player_id", None)
        data.setdefault("players", [])

        return data

    def save(self):

        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(self.data, handle, indent=2)

    def ensure_active_player(self):

        if not self.data["players"]:
            self.create_player("Player 1")
            return

        active_id = self.data.get("active_player_id")

        if self.get_player(active_id) is None:
            self.data["active_player_id"] = self.data["players"][0]["id"]
            self.save()

    def create_player(self, name=None):

        existing_numbers = [
            int(player["id"].replace("player_", ""))
            for player in self.data["players"]
            if player.get("id", "").startswith("player_")
            and player["id"].replace("player_", "").isdigit()
        ]

        next_number = max(existing_numbers, default=0) + 1
        player_id = f"player_{next_number}"
        now = self._timestamp()

        player = {
            "id": player_id,
            "name": name or f"Player {next_number}",
            "created_at": now,
            "last_seen_at": now,
            "stats": {
                "games_played": 0,
                "wins": 0,
                "best_level": 0,
                "total_stars": 0
            },
            "levels": {},
            "history": []
        }

        self.data["players"].append(player)
        self.data["active_player_id"] = player_id
        self.save()

        return player

    def players(self):

        return list(self.data["players"])

    def get_player(self, player_id):

        for player in self.data["players"]:
            if player.get("id") == player_id:
                return player

        return None

    def active_player(self):

        return self.get_player(self.data.get("active_player_id"))

    def set_active_player(self, player_id):

        player = self.get_player(player_id)

        if player is None:
            return None

        player["last_seen_at"] = self._timestamp()
        self.data["active_player_id"] = player_id
        self.save()

        return player

    def record_level_result(self, result):

        player = self.active_player()

        if player is None:
            player = self.create_player("Player 1")

        now = self._timestamp()
        level_number = result.get("level_number")
        stars = int(result.get("stars", 0))
        won = result.get("outcome") == "win"

        entry = {
            "played_at": now,
            "outcome": result.get("outcome"),
            "level_number": level_number,
            "board_size": result.get("board_size"),
            "deadzone_count": result.get("deadzone_count", 0),
            "deadzone_limit": result.get("deadzone_limit", 0),
            "gap_count": result.get("gap_count", 0),
            "gap_cells": result.get("gap_cells", 0),
            "score": result.get("score", 0),
            "moves": result.get("moves", 0),
            "stars": stars
        }

        player["history"].append(entry)
        player["history"] = player["history"][-100:]

        stats = player["stats"]
        stats["games_played"] = stats.get("games_played", 0) + 1

        if won:
            stats["wins"] = stats.get("wins", 0) + 1
            stats["best_level"] = max(stats.get("best_level", 0), level_number or 0)

        if level_number is not None:
            level_key = str(level_number)
            previous = player["levels"].get(level_key, {})
            previous_stars = int(previous.get("stars", 0))

            if stars >= previous_stars:
                player["levels"][level_key] = entry

            stats["total_stars"] = sum(
                int(level.get("stars", 0))
                for level in player["levels"].values()
            )

        player["last_seen_at"] = now
        self.save()

        return entry

    def _timestamp(self):

        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
