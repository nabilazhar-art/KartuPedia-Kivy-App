"""Fungsi utilitas: bucket durasi/pemain dan filter daftar game.

Dipindah dari versi Kivy (kartupedia/core/utils.py) tanpa perubahan -- murni
Python, tidak pernah bergantung pada Kivy.
"""
from app.models import Game


def duration_bucket(minutes: int) -> str:
    if minutes < 15:
        return "< 15 menit"
    if minutes <= 30:
        return "15-30 menit"
    if minutes <= 60:
        return "30-60 menit"
    return "> 60 menit"


def player_bucket_matches(game: Game, bucket: str) -> bool:
    lo, hi = game.players_min, game.players_max
    if bucket == "1":
        return lo <= 1 <= hi
    if bucket == "2":
        return lo <= 2 <= hi
    if bucket == "3-4":
        return not (hi < 3 or lo > 4)
    if bucket == "5+":
        return hi >= 5
    return True


def filter_games(games, query="", categories=None, player_buckets=None,
                  duration_buckets=None, difficulties=None):
    result = []
    for g in games:
        if query and not g.matches_query(query):
            continue
        if categories and g.category not in categories:
            continue
        if player_buckets and not any(player_bucket_matches(g, b) for b in player_buckets):
            continue
        if duration_buckets and duration_bucket(g.duration_minutes) not in duration_buckets:
            continue
        if difficulties and g.difficulty not in difficulties:
            continue
        result.append(g)
    return result


def safe_get(lst, idx, default=None):
    try:
        return lst[idx]
    except Exception:
        return default
