"""Layar Tentang: informasi aplikasi dan atribusi.

Tampilan didefinisikan di kv/about.kv (layar ini statis, tidak ada logika
interaktif). Class Python hanya menyediakan teks yang perlu dihitung
(deskripsi, versi, jumlah game) untuk dibaca oleh KV.
"""
import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from kartupedia.config import APP_VERSION
from kartupedia.core.database import GAME_OBJECTS

_KV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kv", "about.kv")

_DESC_TEXT = (
    "KartuPedia adalah ensiklopedia dan panduan permainan kartu offline. "
    "Aplikasi ini membantu kamu menemukan permainan kartu baru, memahami "
    "aturan mainnya secara lengkap, dan memilih permainan yang sesuai "
    "dengan jumlah pemain, waktu, serta gaya bermainmu. KartuPedia bukan "
    "aplikasi untuk memainkan game secara langsung, melainkan panduan "
    "referensi yang bisa diakses kapan saja tanpa koneksi internet."
)


class AboutScreen(Screen):
    """Layar statis: logo, nama app, tagline, deskripsi, info versi. Tampilan: kv/about.kv."""

    @property
    def desc_text(self):
        return _DESC_TEXT

    @property
    def version_text(self):
        return "Versi Aplikasi: " + APP_VERSION

    @property
    def total_games_text(self):
        return "Total Permainan: " + str(len(GAME_OBJECTS)) + " game"


Builder.load_file(_KV_PATH)
