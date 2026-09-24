"""Layar Jelajah: pencarian dan filter seluruh daftar game."""
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.core.database import GAME_OBJECTS, CATEGORIES
from kartupedia.core.utils import filter_games
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.buttons import AppIconButton, CategoryChip
from kartupedia.widgets.common import SectionHeader, EmptyState, AppSearchBar
from kartupedia.widgets.game_cards import GameCard
from kartupedia.widgets.filter_sheet import FilterSheet

class ExploreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.query = ""
        self.selected_category = None
        self.filters = {"players": set(), "duration": set(), "difficulty": set(), "category": set()}
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos), size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(64),
                            padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, 0), spacing=AppSpacing.XS)
        title = Label(text="Jelajah", color=AppColors.TEXT, font_size=AppTypography.HEADING, bold=True,
                      halign="left", valign="middle", size_hint_y=None, height=dp(30))
        title.bind(size=title.setter("text_size"))
        header.add_widget(title)
        root.add_widget(header)

        search_row = BoxLayout(size_hint_y=None, height=dp(46), padding=(AppSpacing.LG, 0), spacing=AppSpacing.XS)
        self.search_bar = AppSearchBar(hint_text="Cari permainan kartu...", on_text=self._on_search)
        search_row.add_widget(self.search_bar)
        filter_btn = AppIconButton(icon_text="\u2261", size_dp=46)
        filter_btn.bind(on_release=lambda *_: self._open_filter())
        filter_wrap = BoxLayout(size_hint=(None, 1), width=dp(46))
        filter_wrap.add_widget(filter_btn)
        search_row.add_widget(filter_wrap)
        root.add_widget(search_row)

        chip_scroll = ScrollView(size_hint=(1, None), height=dp(48), do_scroll_y=False, do_scroll_x=True, bar_width=0)
        self.chip_row = BoxLayout(size_hint=(None, 1), spacing=AppSpacing.XS,
                                   padding=(AppSpacing.LG, AppSpacing.XS, AppSpacing.LG, AppSpacing.XS))
        self.chip_row.bind(minimum_width=self.chip_row.setter("width"))
        chip_scroll.add_widget(self.chip_row)
        root.add_widget(chip_scroll)

        self.result_label = Label(text="", color=AppColors.TEXT_MUTED, font_size=AppTypography.CAPTION,
                                   halign="left", valign="middle", size_hint_y=None, height=dp(24),
                                   padding=(AppSpacing.LG, 0))
        self.result_label.bind(size=self.result_label.setter("text_size"))
        root.add_widget(self.result_label)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.list_wrap = BoxLayout(orientation="vertical", size_hint_y=None,
                                    padding=(AppSpacing.LG, AppSpacing.XS, AppSpacing.LG, AppSpacing.XXL),
                                    spacing=AppSpacing.SM)
        self.list_wrap.bind(minimum_height=self.list_wrap.setter("height"))
        self.scroll.add_widget(self.list_wrap)
        root.add_widget(self.scroll)
        self.add_widget(root)
        self._build_chips()

    def _build_chips(self):
        self.chip_row.clear_widgets()
        self._chips = {}
        for cat in CATEGORIES:
            chip = CategoryChip(text=cat, selected=(cat == self.selected_category), on_toggle=self._toggle_category)
            self._chips[cat] = chip
            self.chip_row.add_widget(chip)

    def _toggle_category(self, category):
        if self.selected_category == category:
            self.selected_category = None
        else:
            self.selected_category = category
        for cat, chip in self._chips.items():
            chip.set_selected(cat == self.selected_category)
        self.refresh()

    def _on_search(self, value):
        self.query = value
        self.refresh()

    def _open_filter(self):
        sheet = FilterSheet(self.filters, on_apply=self._apply_filters)
        sheet.open()

    def _apply_filters(self, selected):
        self.filters = selected
        self.refresh()

    def set_query(self, query):
        self.query = query
        self.search_bar.input.text = query
        self.refresh()

    def set_category(self, category):
        self.selected_category = category
        for cat, chip in self._chips.items():
            chip.set_selected(cat == self.selected_category)
        self.refresh()

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        app = App.get_running_app()
        categories = set(self.filters.get("category", set()))
        if self.selected_category:
            categories.add(self.selected_category)
        results = filter_games(
            GAME_OBJECTS, query=self.query,
            categories=categories or None,
            player_buckets=self.filters.get("players") or None,
            duration_buckets=self.filters.get("duration") or None,
            difficulties=self.filters.get("difficulty") or None,
        )
        self.result_label.text = f"{len(results)} permainan ditemukan"
        self.list_wrap.clear_widgets()
        if not results:
            self.list_wrap.add_widget(EmptyState(
                icon="\u2205", title="Tidak ada hasil",
                subtitle="Coba ubah kata kunci atau filter pencarian.",
            ))
            return
        for g in results:
            self.list_wrap.add_widget(GameCard(g, on_press_game=app.open_game_detail))
