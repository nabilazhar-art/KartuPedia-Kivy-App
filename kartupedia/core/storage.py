"""Penyimpanan lokal sederhana berbasis JSON untuk favorit & recently viewed."""
import os
import json

from kivy.utils import platform

from kartupedia.config import PROJECT_ROOT


def get_storage_directory():
    if platform == "android":
        try:
            from android.storage import app_storage_path  # type: ignore
            return app_storage_path()
        except ImportError:
            return os.path.expanduser("~")

    return PROJECT_ROOT


STORAGE_DIR = get_storage_directory()
STORAGE_FILE = os.path.join(STORAGE_DIR, "kartupedia_data.json")


class LocalStorage:
    """Penyimpanan lokal sederhana berbasis JSON untuk favorit & recently viewed."""

    def __init__(self, path=STORAGE_FILE):
        self.path = path
        self.data = {"favorites": [], "recently_viewed": []}
        self.load()

    def load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        self.data["favorites"] = loaded.get("favorites", []) or []
                        self.data["recently_viewed"] = loaded.get("recently_viewed", []) or []
        except Exception:
            self.data = {"favorites": [], "recently_viewed": []}

    def save(self):
        try:
            parent = os.path.dirname(self.path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            tmp_path = self.path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.path)
        except Exception:
            try:
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

    def get_favorites(self):
        return list(self.data.get("favorites", []))

    def is_favorite(self, game_id):
        return game_id in self.data.get("favorites", [])

    def toggle_favorite(self, game_id):
        favs = self.data.setdefault("favorites", [])
        if game_id in favs:
            favs.remove(game_id)
            result = False
        else:
            favs.append(game_id)
            result = True
        self.save()
        return result

    def get_recently_viewed(self):
        return list(self.data.get("recently_viewed", []))

    def add_recently_viewed(self, game_id):
        recent = self.data.setdefault("recently_viewed", [])
        if game_id in recent:
            recent.remove(game_id)
        recent.insert(0, game_id)
        del recent[10:]
        self.save()


STORAGE = LocalStorage()
