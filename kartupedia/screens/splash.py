"""Layar pembuka (splash) yang tampil singkat lalu berpindah ke tampilan utama.

Tampilan (background, logo, judul, tagline) didefinisikan di kv/splash.kv.
Class ini hanya menjalankan animasi fade-in dan menjadwalkan perpindahan
otomatis ke Home setelah beberapa detik — persis seperti versi sebelumnya.
"""
import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation

_KV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kv", "splash.kv")


class SplashScreen(Screen):
    """Tampilan: kv/splash.kv. Fade-in logo/judul/tagline, lalu pindah ke Home."""

    def on_kv_post(self, base_widget):
        Animation(opacity=1, duration=0.35).start(self.ids.logo_wrap)
        Animation(opacity=1, duration=0.35).start(self.ids.title_label)
        Animation(opacity=1, duration=0.35).start(self.ids.subtitle_label)
        Clock.schedule_once(self._go_home, 7.0)

    def _go_home(self, dt):
        app = App.get_running_app()
        app.show_main_shell()


Builder.load_file(_KV_PATH)
