"""Layar Favorit: daftar game yang ditandai favorit oleh pengguna."""
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.core.database import GAME_OBJECTS, get_game_by_id
from kartupedia.core.storage import STORAGE
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.common import SectionHeader, EmptyState
from kartupedia.widgets.game_cards import GameCard

class FavoriteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos), size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(size_hint_y=None, height=dp(72), padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, 0), spacing=dp(8))
        title_box = BoxLayout(orientation="vertical", spacing=dp(1))
        title = Label(text="Favorit", color=AppColors.TEXT, font_size=AppTypography.HEADING, bold=True,
                      halign="left", valign="bottom", size_hint_y=None, height=dp(34))
        title.bind(size=title.setter("text_size"))
        self.count_label = Label(text="", color=AppColors.TEXT_MUTED, font_size=AppTypography.META,
                                 halign="left", valign="top", size_hint_y=None, height=dp(18))
        self.count_label.bind(size=self.count_label.setter("text_size"))
        title_box.add_widget(title)
        title_box.add_widget(self.count_label)
        header.add_widget(title_box)
        root.add_widget(header)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(orientation="vertical", size_hint_y=None,
                                  padding=(AppSpacing.LG, AppSpacing.SM, AppSpacing.LG, AppSpacing.XXL),
                                  spacing=AppSpacing.SM)
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        app = App.get_running_app()
        self.content.clear_widgets()
        fav_ids = STORAGE.get_favorites()
        games = [g for g in GAME_OBJECTS if g.id in fav_ids]
        self.count_label.text = f"{len(games)} permainan tersimpan" if games else "Belum ada permainan tersimpan"
        if not games:
            self.content.add_widget(EmptyState(
                icon="heart", title="Belum ada permainan favorit.",
                subtitle="Tekan ikon hati pada kartu atau halaman detail untuk menyimpan permainan.",
                button_text="Jelajahi Permainan", on_button=lambda: app.go_to_explore(),
            ))
            return
        for g in games:
            self.content.add_widget(GameCard(
                g, on_press_game=app.open_game_detail,
                on_favorite_change=self._favorite_changed
            ))

    def _favorite_changed(self, game_id, is_favorite):
        if not is_favorite:
            Clock.schedule_once(lambda dt: self.refresh(), 0)
