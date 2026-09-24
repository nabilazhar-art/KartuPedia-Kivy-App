"""Komponen khusus layar Detail Game: langkah quick guide, kartu spesial, ranking."""
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.widgets.base import RoundedBG


class QuickGuideStep(BoxLayout):
    """Satu langkah dalam Quick Guide dengan nomor."""

    def __init__(self, number, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(40)
        self.spacing = AppSpacing.SM
        from kivy.uix.label import Label

        class _NumBadge(BoxLayout, RoundedBG):
            pass

        badge = _NumBadge(size_hint=(None, None), size=(dp(26), dp(26)))
        badge.init_rounded_bg(color=AppColors.PRIMARY, radius=dp(13))
        badge.add_widget(Label(text=str(number), color=AppColors.WHITE, font_size=AppTypography.CAPTION, bold=True))
        badge_wrap = BoxLayout(size_hint=(None, 1), width=dp(26))
        badge_wrap.add_widget(badge)
        self.add_widget(badge_wrap)

        text_lbl = Label(text=text, color=AppColors.TEXT, font_size=AppTypography.BODY,
                          halign="left", valign="middle")
        text_lbl.bind(width=lambda *a: setattr(text_lbl, "text_size", (text_lbl.width, None)))
        text_lbl.bind(texture_size=lambda *a: setattr(self, "height", max(dp(40), text_lbl.texture_size[1] + dp(10))))
        self.add_widget(text_lbl)


class SpecialCardTile(BoxLayout, RoundedBG):
    """Menampilkan satu kartu spesial dengan penjelasannya."""

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.padding = (AppSpacing.SM, AppSpacing.XS)
        self.spacing = AppSpacing.XS
        self.init_rounded_bg(color=AppColors.SURFACE, radius=AppRadius.SM, border_color=AppColors.BORDER)
        from kivy.uix.label import Label
        mark = Label(text="\u2666", color=AppColors.GOLD, font_size=sp(14), size_hint=(None, None),
                     size=(dp(20), dp(20)))
        self.add_widget(mark)
        lbl = Label(text=text, color=AppColors.TEXT_SECONDARY, font_size=AppTypography.CAPTION,
                    halign="left", valign="middle")
        lbl.bind(width=lambda *a: setattr(lbl, "text_size", (lbl.width, None)))
        lbl.bind(texture_size=lambda *a: setattr(self, "height", max(dp(34), lbl.texture_size[1] + dp(16))))
        self.add_widget(lbl)


class RankingCard(BoxLayout, RoundedBG):
    """Menampilkan urutan ranking / kombinasi kartu."""

    def __init__(self, index, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(34)
        self.padding = (AppSpacing.SM, 0)
        self.spacing = AppSpacing.XS
        self.init_rounded_bg(color=AppColors.STRONG, radius=AppRadius.SM)
        from kivy.uix.label import Label
        num_lbl = Label(text=f"#{index}", color=AppColors.GOLD, font_size=AppTypography.CAPTION, bold=True,
                         size_hint=(None, 1), width=dp(30))
        self.add_widget(num_lbl)
        text_lbl = Label(text=text, color=AppColors.TEXT, font_size=AppTypography.CAPTION,
                          halign="left", valign="middle")
        text_lbl.bind(size=text_lbl.setter("text_size"))
        self.add_widget(text_lbl)
