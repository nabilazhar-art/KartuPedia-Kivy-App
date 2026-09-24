"""Konfigurasi aplikasi KartuPedia: identitas, ukuran dasar, path proyek, dan setup Window."""
import os

APP_NAME = "KartuPedia"
APP_TAGLINE = "Temukan permainan. Pahami aturannya. Mulai bermain."
APP_VERSION = "1.0.0"

BASE_WIDTH = 390
BASE_HEIGHT = 844

# Root proyek = satu tingkat di atas folder paket "kartupedia".
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
GAMES_FILE = os.path.join(DATA_DIR, "games.json")


def configure_window():
    """Terapkan pengaturan Window.

    WAJIB dipanggil dari main.py SEBELUM mengimpor modul UI/tema
    (kartupedia.core.theme, kartupedia.app, dst.), karena dp()/sp() di tema
    dihitung saat modul diimpor.
    """
    from kivy.core.window import Window
    from kivy.utils import platform

    Window.softinput_mode = "below_target"

    if platform not in ("android", "ios"):
        try:
            Window.size = (BASE_WIDTH, BASE_HEIGHT)
        except Exception:
            pass
