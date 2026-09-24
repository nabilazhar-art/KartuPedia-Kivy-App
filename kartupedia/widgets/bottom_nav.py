"""Navigasi bawah (bottom navigation) dengan indikator aktif berbentuk pill.

Struktur layout (BottomNavigation & _NavBtn) didefinisikan di
kv/bottom_nav.kv. Warna aktif/nonaktif (background pill, warna ikon, warna &
bold teks) tetap diatur di sini lewat Python, karena VectorIcon menggambar
warnanya langsung di canvas dan tidak reaktif terhadap Kivy Property.
"""
import os

from kivy.metrics import dp, sp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.graphics import Color, Line

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.icons import VectorIcon

_KV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kv", "bottom_nav.kv")


class _NavBtn(ButtonBehavior, BoxLayout, RoundedBG):
    """Satu tombol pada BottomNavigation. Struktur: kv/bottom_nav.kv.

    Sebelumnya class ini didefinisikan ulang di dalam setiap pemanggilan
    _make_button() (4 class terpisah, satu per tombol) — sekarang jadi satu
    class di level modul, dipakai bersama oleh keempat tombol. Perilakunya
    sama persis, ini murni kerapian struktur.
    """
    pass


class BottomNavigation(BoxLayout, RoundedBG):
    """Bottom navigation modern dengan indikator aktif berbentuk pill. Layout: kv/bottom_nav.kv."""

    ITEMS = [
        ("home", "Beranda", "home"),
        ("explore", "Jelajah", "explore"),
        ("favorite", "Favorit", "heart"),
        ("about", "Tentang", "info"),
    ]

    def __init__(self, on_navigate=None, **kwargs):
        super().__init__(**kwargs)
        self.on_navigate = on_navigate
        self.active = "home"
        self.init_rounded_bg(color=AppColors.SURFACE, radius=0, border_color=None)
        self._buttons = {}
        for key, label, icon in self.ITEMS:
            btn = self._make_button(key, label, icon)
            self._buttons[key] = btn
            self.add_widget(btn)
        with self.canvas.before:
            Color(*AppColors.BORDER_SOFT)
            self._top_line = Line(points=[self.x, self.top, self.right, self.top], width=1)
        self.bind(pos=self._update_line, size=self._update_line)

    def _update_line(self, *args):
        self._top_line.points = [self.x, self.top, self.right, self.top]

    def _make_button(self, key, label, icon):
        active = key == self.active
        btn = _NavBtn()
        btn.init_rounded_bg(color=(AppColors.PRIMARY[0], AppColors.PRIMARY[1], AppColors.PRIMARY[2], .14)
                           if active else AppColors.TRANSPARENT, radius=dp(15))
        icon_lbl = VectorIcon(name=icon,
                              color=AppColors.PRIMARY_LIGHT if active else AppColors.TEXT_MUTED,
                              size_hint=(1, .58))
        text_lbl = Label(text=label, font_size=sp(10.5),
                         color=AppColors.PRIMARY_LIGHT if active else AppColors.TEXT_MUTED,
                         bold=active, size_hint_y=.42)
        btn.add_widget(icon_lbl)
        btn.add_widget(text_lbl)
        btn._icon_lbl = icon_lbl
        btn._text_lbl = text_lbl
        btn.bind(on_release=lambda *_: self._select(key))
        return btn

    def _select(self, key):
        self.set_active(key)
        if self.on_navigate:
            self.on_navigate(key)

    def set_active(self, key):
        self.active = key
        for k, btn in self._buttons.items():
            active = k == key
            btn.set_bg_color((AppColors.PRIMARY[0], AppColors.PRIMARY[1], AppColors.PRIMARY[2], .14)
                             if active else AppColors.TRANSPARENT)
            btn._icon_lbl.set_color(AppColors.PRIMARY_LIGHT if active else AppColors.TEXT_MUTED)
            btn._text_lbl.color = AppColors.PRIMARY_LIGHT if active else AppColors.TEXT_MUTED
            btn._text_lbl.bold = active


Builder.load_file(_KV_PATH)
