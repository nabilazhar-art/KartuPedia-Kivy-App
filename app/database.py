"""Database permainan: memuat data/games.json menjadi objek Game."""
import json

from app.config import GAMES_FILE
from app.models import Game


def load_game_data(path=GAMES_FILE):
    """Baca daftar game (list of dict) dari file JSON."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"File data game tidak ditemukan: {path}. "
            "Pastikan folder 'data/' (berisi games.json) ada di root proyek."
        ) from exc


GAME_DATABASE = load_game_data()
GAME_OBJECTS = [Game(d) for d in GAME_DATABASE]
CATEGORIES = ["Poker", "Casino", "Trick-Taking", "Rummy", "Solitaire", "Party", "Classic", "Family"]


def get_game_by_id(game_id: str):
    for g in GAME_OBJECTS:
        if g.id == game_id:
            return g
    return None
