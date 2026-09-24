"""Tombol-tombol dasar: primary button, icon button, chip kategori, tombol favorit.

AppButton tampilannya didefinisikan di kv/buttons.kv (dimuat di bawah). Widget
lain di file ini (AppIconButton, CategoryChip, FavoriteButton) tetap ditulis
manual seperti sebelumnya, karena warnanya berubah dinamis lewat VectorIcon
yang menggambar manual di canvas (bukan Kivy Property reaktif) — lihat
kv/bottom_nav.kv untuk penjelasan yang sama pada BottomNavigation.
"""
import os

from kivy.metrics import dp
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.core.storage import STORAGE
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.icons import VectorIcon

_KV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kv", "buttons.kv")


class AppButton(ButtonBehavior, BoxLayout, RoundedBG):
    """Tombol primary dengan background indigo. Tampilan: kv/buttons.kv."""

    text = StringProperty("")
    bg_color = ListProperty(list(AppColors.PRIMARY))
    text_color = ListProperty(list(AppColors.WHITE))

    def on_press(self):
        anim = Animation(opacity=0.7, duration=0.06) + Animation(opacity=1, duration=0.1)
        anim.start(self)


class AppIconButton(ButtonBehavior, FloatLayout, RoundedBG):
    """Tombol ikon vektor; tetap menerima icon_text agar kode lama tidak rusak."""

    icon_text = StringProperty("")

    def __init__(self, icon_text="back", bg_color=None, icon_color=None, size_dp=40, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(size_dp), dp(size_dp))
        self.init_rounded_bg(color=bg_color or AppColors.ELEVATED, radius=dp(12))
        mapping = {"<": "back", ">": "chevron_right", "?": "info"}
        self.icon_name = mapping.get(icon_text, icon_text)
        self._icon = VectorIcon(name=self.icon_name, color=icon_color or AppColors.TEXT,
                                size_hint=(.58, .58), pos_hint={"center_x": .5, "center_y": .5})
        self.add_widget(self._icon)

    def on_press(self):
        (Animation(opacity=.55, duration=.05) + Animation(opacity=1, duration=.10)).start(self)


class CategoryChip(ButtonBehavior, BoxLayout, RoundedBG):
    """Chip kategori yang dapat dipilih (toggle)."""

    def __init__(self, text="", selected=False, on_toggle=None, **kwargs):
        super().__init__(**kwargs)
        self.text_value = text
        self.selected = selected
        self.on_toggle = on_toggle
        self.size_hint = (None, None)
        self.height = dp(34)
        self.padding = (AppSpacing.SM, 0)
        self.width = dp(18) + len(text) * dp(8)
        self.init_rounded_bg(
            color=AppColors.PRIMARY if selected else AppColors.ELEVATED,
            radius=AppRadius.PILL,
            border_color=None if selected else AppColors.BORDER,
        )
        from kivy.uix.label import Label
        self._label = Label(
            text=text, color=AppColors.WHITE if selected else AppColors.TEXT_SECONDARY,
            font_size=AppTypography.CAPTION, bold=selected,
        )
        self.add_widget(self._label)

    def set_selected(self, selected):
        self.selected = selected
        self.set_bg_color(AppColors.PRIMARY if selected else AppColors.ELEVATED)
        self._label.color = AppColors.WHITE if selected else AppColors.TEXT_SECONDARY
        self._label.bold = selected

    def on_press(self):
        if self.on_toggle:
            self.on_toggle(self.text_value)


class FavoriteButton(ButtonBehavior, FloatLayout, RoundedBG):
    """Tombol favorit tanpa Unicode; status disimpan ke LocalStorage."""

    def __init__(self, game_id="", on_change=None, size_dp=40, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.on_change = on_change
        self.size_hint = (None, None)
        self.size = (dp(size_dp), dp(size_dp))
        self.init_rounded_bg(
            color=AppColors.ELEVATED,
            radius=dp(size_dp) / 2,
            border_color=AppColors.BORDER_SOFT,
        )
        self._is_fav = STORAGE.is_favorite(game_id)
        self._icon = VectorIcon(
            name="heart",
            color=self._icon_color(),
            size_hint=(None, None),
            size=(dp(size_dp * .52), dp(size_dp * .52)),
            pos_hint={"center_x": .5, "center_y": .5},
            stroke=1.8,
        )
        self.add_widget(self._icon)

    def _icon_color(self):
        return AppColors.ERROR if self._is_fav else AppColors.TEXT_SECONDARY

    def refresh(self):
        self._is_fav = STORAGE.is_favorite(self.game_id)
        self._icon.set_color(self._icon_color())

    def on_press(self):
        self._is_fav = STORAGE.toggle_favorite(self.game_id)
        self._icon.set_color(self._icon_color())
        anim = (
            Animation(size=(dp(self.width * .65), dp(self.height * .65)), duration=.07)
            + Animation(size=(dp(self.width * .52), dp(self.height * .52)), duration=.09)
        )
        anim.start(self._icon)
        if self.on_change:
            self.on_change(self.game_id, self._is_fav)


Builder.load_file(_KV_PATH)
