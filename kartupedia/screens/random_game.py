"""Layar Random Game: memilih satu game secara acak untuk dimainkan."""
import random

from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.core.database import GAME_OBJECTS
from kartupedia.core.utils import filter_games
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.buttons import AppButton, AppIconButton
from kartupedia.widgets.common import DifficultyBadge, MetadataItem
from kartupedia.widgets.game_cards import FeaturedGameCard

class RandomGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_game = None
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos), size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(size_hint_y=None, height=dp(64), padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, 0))
        back_btn = AppIconButton(icon_text="<", size_dp=36)
        back_btn.bind(on_release=lambda *_: App.get_running_app().go_back())
        back_wrap = BoxLayout(size_hint=(None, 1), width=dp(36))
        back_wrap.add_widget(back_btn)
        header.add_widget(back_wrap)
        title = Label(text="Random Game", color=AppColors.TEXT, font_size=AppTypography.HEADING, bold=True,
                      halign="left", valign="middle")
        title.bind(size=title.setter("text_size"))
        header.add_widget(title)
        root.add_widget(header)

        self.card_wrap = BoxLayout(orientation="vertical", padding=(AppSpacing.LG, AppSpacing.SM),
                                    spacing=AppSpacing.LG)
        self.result_holder = BoxLayout(orientation="vertical", size_hint_y=None)
        self.card_wrap.add_widget(self.result_holder)

        roll_btn = AppButton(text="Acak Permainan", size_hint_y=None, height=dp(50))
        roll_btn.bind(on_release=lambda *_: self._roll())
        self.card_wrap.add_widget(roll_btn)
        self.open_btn = AppButton(text="Buka Detail", bg_color=AppColors.ELEVATED, text_color=AppColors.TEXT,
                                   size_hint_y=None, height=dp(50))
        self.open_btn.bind(on_release=lambda *_: self._open_detail())
        self.open_btn.opacity = 0
        self.open_btn.disabled = True
        self.card_wrap.add_widget(self.open_btn)
        self.card_wrap.add_widget(BoxLayout())
        root.add_widget(self.card_wrap)
        self.add_widget(root)

    def _roll(self):
        pool = GAME_OBJECTS
        app = App.get_running_app()
        filters = getattr(app, "random_filters", None)
        if filters:
            pool = filter_games(
                GAME_OBJECTS,
                categories=filters.get("category") or None,
                player_buckets=filters.get("players") or None,
                duration_buckets=filters.get("duration") or None,
                difficulties=filters.get("difficulty") or None,
            ) or GAME_OBJECTS
        self.current_game = random.choice(pool)
        self.result_holder.clear_widgets()
        card = FeaturedGameCard(self.current_game, on_press_game=lambda gid: self._open_detail())
        self.result_holder.add_widget(card)
        self.result_holder.height = card.height
        self.open_btn.opacity = 1
        self.open_btn.disabled = False
        anim = Animation(opacity=0.3, duration=0.08) + Animation(opacity=1, duration=0.18)
        anim.start(card)

    def _open_detail(self):
        if self.current_game:
            App.get_running_app().open_game_detail(self.current_game.id)

    def on_pre_enter(self):
        if not self.current_game:
            self._roll()
