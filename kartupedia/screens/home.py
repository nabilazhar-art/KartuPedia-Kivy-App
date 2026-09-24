"""Layar Beranda: game unggulan, promo Game Finder, kategori, dan riwayat dilihat."""
import random

from kivy.metrics import dp, sp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.config import APP_NAME
from kartupedia.core.database import GAME_OBJECTS, CATEGORIES, get_game_by_id
from kartupedia.core.storage import STORAGE
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.icons import VectorIcon
from kartupedia.widgets.buttons import CategoryChip
from kartupedia.widgets.common import SectionHeader, EmptyState, AppSearchBar
from kartupedia.widgets.game_cards import GameListTile, FeaturedGameCard

class FinderPromoCard(ButtonBehavior, BoxLayout, RoundedBG):
    """Kartu ajakan Game Finder untuk membantu pengguna memilih game."""

    def __init__(self, on_press_finder=None, **kwargs):
        super().__init__(**kwargs)
        self.on_press_finder = on_press_finder
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(116)
        self.padding = (dp(16), dp(14))
        self.spacing = dp(12)
        self.init_rounded_bg(color=AppColors.STRONG, radius=dp(20), border_color=AppColors.BORDER)

        class _FinderArt(FloatLayout, RoundedBG):
            pass

        art = _FinderArt(size_hint=(None, 1), width=dp(68))
        art.init_rounded_bg(color=AppColors.PRIMARY_DARK, radius=dp(17))
        art.add_widget(VectorIcon(name="cards", color=AppColors.GOLD_LIGHT,
                                  size_hint=(None, None), size=(dp(38), dp(38)),
                                  pos_hint={"center_x": .5, "center_y": .56}))
        art.add_widget(Label(text="FINDER", color=AppColors.WHITE, font_size=sp(7.5),
                             bold=True, size_hint=(1, None), height=dp(16),
                             pos_hint={"x": 0, "y": .06}))
        self.add_widget(art)

        info = BoxLayout(orientation="vertical", spacing=dp(3), size_hint_x=1)
        title = Label(text="Bingung mau main apa?", color=AppColors.TEXT,
                      font_size=sp(15.5), bold=True, halign="left", valign="middle",
                      size_hint_y=None, height=dp(25))
        title.bind(size=title.setter("text_size"))
        info.add_widget(title)

        desc = Label(text="Jawab beberapa pertanyaan dan KartuPedia akan memilihkan game yang paling cocok.",
                     color=AppColors.TEXT_SECONDARY, font_size=sp(10.5),
                     halign="left", valign="top", size_hint_y=None, height=dp(40))
        desc.bind(width=lambda *a: setattr(desc, "text_size", (desc.width, None)))
        info.add_widget(desc)

        cta = Label(text="Mulai Game Finder  ›", color=AppColors.GOLD_LIGHT,
                    font_size=sp(10.5), bold=True, halign="left", valign="middle",
                    size_hint_y=None, height=dp(20))
        cta.bind(size=cta.setter("text_size"))
        info.add_widget(cta)
        self.add_widget(info)

    def on_release(self):
        if self.on_press_finder:
            self.on_press_finder()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos),
                  size=lambda *a: setattr(self._bg, "size", root.size))

        # App bar lebih modern: logo kecil + nama aplikasi + badge offline
        header = BoxLayout(size_hint_y=None, height=dp(78), padding=(dp(20), dp(14), dp(20), dp(8)), spacing=dp(10))
        logo = FloatLayout(size_hint=(None, None), size=(dp(42), dp(42)), pos_hint={"center_y": .5})
        with logo.canvas.before:
            Color(*AppColors.PRIMARY)
            logo._bg = RoundedRectangle(pos=logo.pos, size=logo.size, radius=[dp(13)])
        logo.bind(pos=lambda *a: setattr(logo._bg, "pos", logo.pos), size=lambda *a: setattr(logo._bg, "size", logo.size))
        logo.add_widget(VectorIcon(name="cards", color=AppColors.WHITE, size_hint=(.68,.68),
                                   pos_hint={"center_x":.5,"center_y":.5}))
        header.add_widget(logo)

        title_wrap = BoxLayout(orientation="vertical", spacing=0)
        title = Label(text=APP_NAME, color=AppColors.TEXT, font_size=sp(20), bold=True,
                      halign="left", valign="bottom", size_hint_y=.58)
        title.bind(size=title.setter("text_size"))
        subtitle = Label(text="Ensiklopedia permainan kartu", color=AppColors.TEXT_MUTED, font_size=sp(10.5),
                         halign="left", valign="top", size_hint_y=.42)
        subtitle.bind(size=subtitle.setter("text_size"))
        title_wrap.add_widget(title); title_wrap.add_widget(subtitle)
        header.add_widget(title_wrap)

        class _OfflineBadge(BoxLayout, RoundedBG):
            pass
        badge = _OfflineBadge(size_hint=(None,None), size=(dp(64),dp(26)), pos_hint={"center_y":.5}, padding=(dp(8),0))
        badge.init_rounded_bg(color=(AppColors.SUCCESS[0],AppColors.SUCCESS[1],AppColors.SUCCESS[2],.12), radius=dp(13))
        badge.add_widget(Label(text="OFFLINE", color=AppColors.SUCCESS, font_size=sp(8.5), bold=True))
        header.add_widget(badge)
        root.add_widget(header)

        self.scroll = ScrollView(size_hint=(1, 1), bar_width=0)
        self.content = BoxLayout(orientation="vertical", size_hint_y=None,
                                 padding=(dp(20), dp(6), dp(20), dp(34)), spacing=dp(18))
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        self.content.clear_widgets()
        app = App.get_running_app()

        search = AppSearchBar(hint_text="Cari nama permainan, kategori, atau tag...", on_text=self._on_search_text)
        self.content.add_widget(search)

        self.content.add_widget(FinderPromoCard(on_press_finder=app.open_finder))

        featured = random.choice(GAME_OBJECTS) if GAME_OBJECTS else None
        if featured:
            self.content.add_widget(FeaturedGameCard(featured, on_press_game=app.open_game_detail))

        self.content.add_widget(SectionHeader(title="Kategori"))
        cat_scroll = ScrollView(size_hint=(1, None), height=dp(42), do_scroll_y=False, do_scroll_x=True, bar_width=0)
        cat_row = BoxLayout(size_hint=(None, 1), spacing=dp(8))
        cat_row.bind(minimum_width=cat_row.setter("width"))
        for cat in CATEGORIES:
            cat_row.add_widget(CategoryChip(text=cat, selected=False, on_toggle=self._go_category))
        cat_scroll.add_widget(cat_row)
        self.content.add_widget(cat_scroll)

        self.content.add_widget(SectionHeader(title="Populer", action_text="Lihat Semua", on_action=self._go_explore))
        pop_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
        pop_wrap.bind(minimum_height=pop_wrap.setter("height"))
        for g in GAME_OBJECTS[:6]:
            pop_wrap.add_widget(GameListTile(g, on_press_game=app.open_game_detail))
        self.content.add_widget(pop_wrap)

        self.content.add_widget(SectionHeader(title="Baru Dilihat"))
        recent_ids = STORAGE.get_recently_viewed()
        if recent_ids:
            recent_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
            recent_wrap.bind(minimum_height=recent_wrap.setter("height"))
            for gid in recent_ids[:5]:
                g = get_game_by_id(gid)
                if g:
                    recent_wrap.add_widget(GameListTile(g, on_press_game=app.open_game_detail))
            self.content.add_widget(recent_wrap)
        else:
            empty = EmptyState(icon="", title="Belum ada riwayat",
                               subtitle="Permainan yang dibuka akan tersimpan di bagian ini.")
            self.content.add_widget(empty)

    def _on_search_text(self, value):
        app = App.get_running_app()
        app.pending_search_query = value
        if value:
            app.go_to_search(value)

    def _go_category(self, category):
        App.get_running_app().go_to_explore(category=category)

    def _go_explore(self):
        App.get_running_app().go_to_explore()
