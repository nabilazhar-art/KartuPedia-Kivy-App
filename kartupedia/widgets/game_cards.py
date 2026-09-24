"""Kartu/tile untuk menampilkan game: daftar, grid, dan kartu unggulan (hero)."""
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.core.models import Game
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.icons import VectorIcon
from kartupedia.widgets.buttons import FavoriteButton
from kartupedia.widgets.common import DifficultyBadge, MetadataItem


class GameListTile(ButtonBehavior, BoxLayout, RoundedBG):
    """Tile modern untuk daftar permainan di beranda."""

    def __init__(self, game: Game, on_press_game=None, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.on_press_game = on_press_game
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(88)
        self.padding = (dp(12), dp(10), dp(10), dp(10))
        self.spacing = dp(12)
        self.init_rounded_bg(color=AppColors.SURFACE, radius=dp(18), border_color=AppColors.BORDER_SOFT)

        class _Avatar(FloatLayout, RoundedBG):
            pass

        av = _Avatar(size_hint=(None, None), size=(dp(56), dp(56)), pos_hint={"center_y": .5})
        av.init_rounded_bg(color=AppColors.ELEVATED, radius=dp(16))
        av.add_widget(VectorIcon(name="cards", color=AppColors.GOLD,
                                 size_hint=(None, None), size=(dp(30), dp(30)),
                                 pos_hint={"center_x": .5, "center_y": .5}))
        self.add_widget(av)

        from kivy.uix.label import Label
        info = BoxLayout(orientation="vertical", spacing=dp(2), size_hint_x=1)
        name_lbl = Label(text=game.name, color=AppColors.TEXT, font_size=sp(14.5), bold=True,
                         halign="left", valign="bottom", size_hint_y=None, height=dp(28))
        name_lbl.bind(size=name_lbl.setter("text_size"))
        info.add_widget(name_lbl)

        meta_lbl = Label(text=f"{game.category}  •  {game.player_label()}",
                         color=AppColors.TEXT_SECONDARY, font_size=sp(11.5),
                         halign="left", valign="middle", size_hint_y=None, height=dp(20))
        meta_lbl.bind(size=meta_lbl.setter("text_size"))
        info.add_widget(meta_lbl)

        time_lbl = Label(text=game.duration, color=AppColors.TEXT_MUTED, font_size=sp(10.5),
                         halign="left", valign="top", size_hint_y=None, height=dp(18))
        time_lbl.bind(size=time_lbl.setter("text_size"))
        info.add_widget(time_lbl)
        self.add_widget(info)

        right = BoxLayout(orientation="horizontal", size_hint=(None, 1), width=dp(116), spacing=dp(7))
        fav = FavoriteButton(game_id=game.id, size_dp=34)
        right.add_widget(fav)
        diff_col = BoxLayout(orientation="vertical", size_hint_x=None, width=dp(70), spacing=dp(4))
        diff_col.add_widget(BoxLayout())
        diff_col.add_widget(DifficultyBadge(difficulty=game.difficulty))
        chev = BoxLayout(size_hint_y=None, height=dp(18))
        chev.add_widget(BoxLayout())
        chev.add_widget(VectorIcon(name="chevron_right", color=AppColors.TEXT_MUTED,
                                   size_hint=(None, None), size=(dp(16), dp(16))))
        diff_col.add_widget(chev)
        right.add_widget(diff_col)
        self.add_widget(right)

    def on_press(self):
        self.set_bg_color(AppColors.ELEVATED)

    def on_release(self):
        self.set_bg_color(AppColors.SURFACE)
        if self.on_press_game:
            self.on_press_game(self.game.id)


class GameCard(ButtonBehavior, BoxLayout, RoundedBG):
    """Card game dengan tombol favorit yang dapat dipakai langsung."""

    def __init__(self, game: Game, on_press_game=None, on_favorite_change=None, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.on_press_game = on_press_game
        self.on_favorite_change = on_favorite_change
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(132)
        self.padding = (AppSpacing.MD, AppSpacing.SM)
        self.spacing = dp(5)
        self.init_rounded_bg(color=AppColors.SURFACE, radius=AppRadius.MD, border_color=AppColors.BORDER)

        top_row = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        cat_lbl = Label(text=game.category, color=AppColors.GOLD, font_size=AppTypography.META,
                         bold=True, halign="left", valign="middle")
        cat_lbl.bind(size=cat_lbl.setter("text_size"))
        top_row.add_widget(cat_lbl)
        top_row.add_widget(BoxLayout())

        fav = FavoriteButton(
            game_id=game.id, size_dp=30,
            on_change=self._favorite_changed
        )
        top_row.add_widget(fav)

        badge = DifficultyBadge(difficulty=game.difficulty)
        badge_wrap = BoxLayout(size_hint_x=None, width=dp(70))
        badge_wrap.add_widget(badge)
        top_row.add_widget(badge_wrap)
        self.add_widget(top_row)

        name_lbl = Label(text=game.name, color=AppColors.TEXT, font_size=AppTypography.SECTION,
                          bold=True, halign="left", valign="middle", size_hint_y=None, height=dp(24))
        name_lbl.bind(size=name_lbl.setter("text_size"))
        self.add_widget(name_lbl)

        desc_lbl = Label(text=game.description, color=AppColors.TEXT_SECONDARY, font_size=AppTypography.CAPTION,
                          halign="left", valign="top", size_hint_y=None, height=dp(31))
        desc_lbl.bind(size=lambda *a: setattr(desc_lbl, "text_size", (desc_lbl.width, dp(31))))
        self.add_widget(desc_lbl)

        meta_lbl = Label(
            text=f"{game.player_label()}  ·  {game.duration}",
            color=AppColors.TEXT_MUTED, font_size=AppTypography.META,
            halign="left", valign="middle", size_hint_y=None, height=dp(18)
        )
        meta_lbl.bind(size=meta_lbl.setter("text_size"))
        self.add_widget(meta_lbl)

    def _favorite_changed(self, game_id, is_favorite):
        if self.on_favorite_change:
            self.on_favorite_change(game_id, is_favorite)

    def on_release(self):
        if self.on_press_game:
            self.on_press_game(self.game.id)


class FeaturedGameCard(ButtonBehavior, BoxLayout, RoundedBG):
    """Hero card beranda dengan hierarki visual seperti aplikasi modern."""

    def __init__(self, game: Game, on_press_game=None, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.on_press_game = on_press_game
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(168)
        self.padding = (dp(18), dp(18))
        self.spacing = dp(14)
        self.init_rounded_bg(color=AppColors.STRONG, radius=dp(22), border_color=AppColors.BORDER)

        left = BoxLayout(orientation="vertical", spacing=dp(5), size_hint_x=1)
        from kivy.uix.label import Label
        eyebrow = Label(text="REKOMENDASI HARI INI", color=AppColors.PRIMARY_LIGHT,
                        font_size=sp(10.5), bold=True, halign="left", valign="middle",
                        size_hint_y=None, height=dp(18))
        eyebrow.bind(size=eyebrow.setter("text_size"))
        left.add_widget(eyebrow)

        title = Label(text=game.name, color=AppColors.TEXT, font_size=sp(22), bold=True,
                      halign="left", valign="middle", size_hint_y=None, height=dp(34))
        title.bind(size=title.setter("text_size"))
        left.add_widget(title)

        desc = Label(text=game.description, color=AppColors.TEXT_SECONDARY, font_size=sp(11.5),
                     halign="left", valign="top", size_hint_y=None, height=dp(46))
        desc.bind(size=lambda *a: setattr(desc, "text_size", (desc.width, dp(46))))
        left.add_widget(desc)

        meta = Label(text=f"{game.player_label()}  •  {game.duration}  •  {game.difficulty}",
                     color=AppColors.GOLD_LIGHT, font_size=sp(10.5), bold=True,
                     halign="left", valign="middle", size_hint_y=None, height=dp(20))
        meta.bind(size=meta.setter("text_size"))
        left.add_widget(meta)
        self.add_widget(left)

        class _DeckArt(FloatLayout, RoundedBG):
            pass
        art = _DeckArt(size_hint=(None, 1), width=dp(88))
        art.init_rounded_bg(color=AppColors.ELEVATED, radius=dp(18))
        art.add_widget(VectorIcon(name="cards", color=AppColors.GOLD,
                                  size_hint=(None, None), size=(dp(54), dp(54)),
                                  pos_hint={"center_x": .5, "center_y": .55}))
        art.add_widget(Label(text=game.category.upper(), color=AppColors.TEXT_MUTED, font_size=sp(8.5), bold=True,
                             size_hint=(1, None), height=dp(20), pos_hint={"x":0,"y":.05}))
        self.add_widget(art)

    def on_release(self):
        if self.on_press_game:
            self.on_press_game(self.game.id)
