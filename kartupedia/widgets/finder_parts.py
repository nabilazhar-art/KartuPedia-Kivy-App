"""Komponen khusus layar Game Finder: kartu rekomendasi dan langkah pertanyaan."""
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.core.models import Game
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.common import MetadataItem, DifficultyBadge


class GameRecommendationCard(ButtonBehavior, BoxLayout, RoundedBG):
    """Hasil rekomendasi dari Game Finder."""

    def __init__(self, game: Game, reason="", on_press_game=None, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.on_press_game = on_press_game
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(128)
        self.padding = (AppSpacing.MD, AppSpacing.SM)
        self.spacing = dp(4)
        self.init_rounded_bg(color=AppColors.ELEVATED, radius=AppRadius.MD, border_color=AppColors.BORDER)
        from kivy.uix.label import Label

        top = BoxLayout(size_hint_y=None, height=dp(24))
        name_lbl = Label(text=game.name, color=AppColors.TEXT, font_size=AppTypography.SECTION, bold=True,
                          halign="left", valign="middle")
        name_lbl.bind(size=name_lbl.setter("text_size"))
        top.add_widget(name_lbl)
        badge_wrap = BoxLayout(size_hint_x=None, width=dp(70))
        badge_wrap.add_widget(DifficultyBadge(difficulty=game.difficulty))
        top.add_widget(badge_wrap)
        self.add_widget(top)

        reason_lbl = Label(text=reason, color=AppColors.GOLD_LIGHT, font_size=AppTypography.CAPTION,
                            halign="left", valign="top", size_hint_y=None, height=dp(32))
        reason_lbl.bind(size=lambda *a: setattr(reason_lbl, "text_size", (reason_lbl.width, dp(32))))
        self.add_widget(reason_lbl)

        meta_lbl = Label(
            text=f"{game.category}  \u00b7  {game.player_label()}  \u00b7  {game.duration}",
            color=AppColors.TEXT_MUTED, font_size=AppTypography.META, halign="left", valign="middle",
            size_hint_y=None, height=dp(20),
        )
        meta_lbl.bind(size=meta_lbl.setter("text_size"))
        self.add_widget(meta_lbl)

    def on_release(self):
        if self.on_press_game:
            self.on_press_game(self.game.id)


class GameFinderStep(BoxLayout):
    """Satu pertanyaan Game Finder dengan pilihan yang mudah dipahami."""

    def __init__(self, title, options, on_select=None, selected=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(8)
        self.size_hint_y = None
        self.selected = selected
        self.on_select = on_select
        self._chips = []

        title_lbl = Label(text=title, color=AppColors.TEXT, font_size=AppTypography.BODY, bold=True,
                           halign="left", valign="middle", size_hint_y=None, height=dp(24))
        title_lbl.bind(size=title_lbl.setter("text_size"))
        self.add_widget(title_lbl)

        chip_row = GridLayout(cols=2, size_hint_y=None, spacing=dp(8), row_default_height=dp(42),
                               row_force_default=True)
        chip_row.bind(minimum_height=chip_row.setter("height"))
        for opt in options:
            chip = self._make_chip(opt)
            self._chips.append(chip)
            chip_row.add_widget(chip)
        self.add_widget(chip_row)
        self.height = dp(24) + dp(8) + chip_row.height + dp(8)
        chip_row.bind(height=lambda *a: setattr(self, "height", dp(24) + dp(8) + chip_row.height + dp(8)))

    def _make_chip(self, opt):
        class _OptChip(ButtonBehavior, BoxLayout, RoundedBG):
            pass

        selected = opt == self.selected
        chip = _OptChip(size_hint_y=None, height=dp(42))
        chip.init_rounded_bg(
            color=(AppColors.PRIMARY[0], AppColors.PRIMARY[1], AppColors.PRIMARY[2], .22) if selected else AppColors.SURFACE,
            radius=dp(13), border_color=AppColors.PRIMARY_LIGHT if selected else AppColors.BORDER
        )
        lbl = Label(text=opt, color=AppColors.WHITE if selected else AppColors.TEXT_SECONDARY,
                    font_size=sp(11.5), bold=selected, halign="center", valign="middle")
        lbl.bind(size=lbl.setter("text_size"))
        chip.add_widget(lbl)
        chip._label = lbl
        chip._value = opt

        def select(*_):
            self.selected = opt
            for c in self._chips:
                is_sel = c._value == opt
                c.set_bg_color((AppColors.PRIMARY[0], AppColors.PRIMARY[1], AppColors.PRIMARY[2], .22)
                               if is_sel else AppColors.SURFACE)
                c._label.color = AppColors.WHITE if is_sel else AppColors.TEXT_SECONDARY
                c._label.bold = is_sel
            if self.on_select:
                self.on_select(opt)

        chip.bind(on_release=select)
        return chip
