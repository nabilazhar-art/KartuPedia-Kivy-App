"""Bottom sheet filter: jumlah pemain, durasi, tingkat kesulitan, kategori."""
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.core.database import CATEGORIES
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.buttons import AppButton, AppIconButton, CategoryChip


class FilterSheet(ModalView):
    """Bottom sheet untuk filter: jumlah pemain, durasi, difficulty, kategori."""

    PLAYER_OPTIONS = ["1", "2", "3-4", "5+"]
    DURATION_OPTIONS = ["< 15 menit", "15-30 menit", "30-60 menit", "> 60 menit"]
    DIFFICULTY_OPTIONS = ["Mudah", "Sedang", "Sulit"]

    def __init__(self, current_filters, on_apply=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = Window.height * 0.82
        self.pos_hint = {"bottom": 1}
        self.background_color = (0, 0, 0, 0.5)
        self.on_apply = on_apply
        self.selected = {
            "players": set(current_filters.get("players", set())),
            "duration": set(current_filters.get("duration", set())),
            "difficulty": set(current_filters.get("difficulty", set())),
            "category": set(current_filters.get("category", set())),
        }
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label

        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.SURFACE)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[AppRadius.XL, AppRadius.XL, 0, 0])
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos))
        root.bind(size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(size_hint_y=None, height=dp(52), padding=(AppSpacing.LG, 0))
        title = Label(text="Filter", color=AppColors.TEXT, font_size=AppTypography.SECTION, bold=True,
                      halign="left", valign="middle")
        title.bind(size=title.setter("text_size"))
        header.add_widget(title)
        close_btn = AppIconButton(icon_text="X", size_dp=32)
        close_btn.bind(on_release=lambda *_: self.dismiss())
        close_wrap = BoxLayout(size_hint_x=None, width=dp(32))
        close_wrap.add_widget(close_btn)
        header.add_widget(close_wrap)
        root.add_widget(header)

        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation="vertical", size_hint_y=None, padding=(AppSpacing.LG, AppSpacing.SM),
                             spacing=AppSpacing.LG)
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(self._section("Jumlah Pemain", self.PLAYER_OPTIONS, "players"))
        content.add_widget(self._section("Durasi", self.DURATION_OPTIONS, "duration"))
        content.add_widget(self._section("Difficulty", self.DIFFICULTY_OPTIONS, "difficulty"))
        content.add_widget(self._section("Kategori", CATEGORIES, "category"))

        scroll.add_widget(content)
        root.add_widget(scroll)

        footer = BoxLayout(size_hint_y=None, height=dp(76), padding=(AppSpacing.LG, AppSpacing.SM), spacing=AppSpacing.SM)
        reset_btn = AppButton(text="Reset", bg_color=AppColors.ELEVATED, text_color=AppColors.TEXT)
        reset_btn.bind(on_release=lambda *_: self._reset())
        apply_btn = AppButton(text="Terapkan Filter")
        apply_btn.bind(on_release=lambda *_: self._apply())
        footer.add_widget(reset_btn)
        footer.add_widget(apply_btn)
        root.add_widget(footer)

        self.add_widget(root)

    def _section(self, title, options, key):
        from kivy.uix.label import Label
        wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
        title_lbl = Label(text=title, color=AppColors.TEXT, font_size=AppTypography.BODY, bold=True,
                           halign="left", valign="middle", size_hint_y=None, height=dp(22))
        title_lbl.bind(size=title_lbl.setter("text_size"))
        wrap.add_widget(title_lbl)

        rows = (len(options) + 1) // 2
        grid = GridLayout(cols=2, size_hint_y=None, height=rows * dp(42), spacing=dp(8))
        for opt in options:
            chip = CategoryChip(text=opt, selected=opt in self.selected[key],
                                 on_toggle=lambda val, k=key: self._toggle(k, val))
            chip.size_hint = (1, None)
            chip.height = dp(38)
            grid.add_widget(chip)
        wrap.add_widget(grid)
        wrap.height = dp(22) + AppSpacing.XS + grid.height
        return wrap

    def _toggle(self, key, value):
        s = self.selected[key]
        if value in s:
            s.remove(value)
        else:
            s.add(value)

    def _reset(self):
        for k in self.selected:
            self.selected[k] = set()
        self.dismiss()
        if self.on_apply:
            self.on_apply(self.selected)

    def _apply(self):
        if self.on_apply:
            self.on_apply(self.selected)
        self.dismiss()
