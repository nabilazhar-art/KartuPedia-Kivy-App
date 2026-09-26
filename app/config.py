"""Konfigurasi aplikasi KartuPedia: identitas dan path data."""
import os

APP_NAME = "KartuPedia"
APP_TAGLINE = "Temukan permainan. Pahami aturannya. Mulai bermain."
APP_VERSION = "2.0.0"  # dinaikkan: versi Flet, desain baru

# Root proyek = satu tingkat di atas folder paket "app".
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
GAMES_FILE = os.path.join(DATA_DIR, "games.json")

# Ukuran jendela default saat aplikasi dijalankan di desktop.
WINDOW_WIDTH = 420
WINDOW_HEIGHT = 860
