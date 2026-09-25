"""Layar Detail Game: aturan main, quick guide, kartu spesial, dan ranking."""
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.core.database import get_game_by_id
from kartupedia.core.storage import STORAGE
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.icons import VectorIcon
from kartupedia.widgets.buttons import AppIconButton, FavoriteButton
from kartupedia.widgets.common import SectionHeader, DifficultyBadge, MetadataItem
from kartupedia.widgets.detail_parts import QuickGuideStep, SpecialCardTile, RankingCard
from kartupedia.widgets.tutorial_video_card import TutorialVideoCard

class GameDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = None
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos), size=lambda *a: setattr(self._bg, "size", root.size))

        self.header = BoxLayout(size_hint_y=None, height=dp(56), padding=(AppSpacing.MD, 0), spacing=AppSpacing.XS)
        back_btn = AppIconButton(icon_text="<", size_dp=36)
        back_btn.bind(on_release=lambda *_: App.get_running_app().go_back())
        back_wrap = BoxLayout(size_hint=(None, 1), width=dp(36))
        back_wrap.add_widget(back_btn)
        self.header.add_widget(back_wrap)
        self.header.add_widget(BoxLayout())
        self.fav_wrap = BoxLayout(size_hint=(None, 1), width=dp(40))
        self.header.add_widget(self.fav_wrap)
        root.add_widget(self.header)

        # Blok info (kategori, judul, deskripsi, metadata) -- LOCKED, tidak ikut
        # scroll. Ini persis bagian "di atas garis" pada permintaan fitur video.
        self.info_block = BoxLayout(
            orientation="vertical", size_hint_y=None,
            padding=(AppSpacing.LG, 0, AppSpacing.LG, AppSpacing.MD),
            spacing=AppSpacing.XS,
        )
        self.info_block.bind(minimum_height=self.info_block.setter("height"))
        root.add_widget(self.info_block)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(orientation="vertical", size_hint_y=None,
                                  padding=(AppSpacing.LG, 0, AppSpacing.LG, AppSpacing.XXL),
                                  spacing=AppSpacing.LG)
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def open_game(self, game_id):
        game = get_game_by_id(game_id)
        if not game:
            return
        self.game = game
        STORAGE.add_recently_viewed(game_id)
        self._render()

    def _favorite_changed(self):
        app = App.get_running_app()
        try:
            app.main_shell.favorite_screen.refresh()
        except Exception:
            pass

    def _label(self, text, color=None, size=None, bold=False, height=None):
        from kivy.uix.label import Label
        lbl = Label(text=text, color=color or AppColors.TEXT, font_size=size or AppTypography.BODY,
                    bold=bold, halign="left", valign="top", size_hint_y=None)
        lbl.bind(width=lambda *a: setattr(lbl, "text_size", (lbl.width, None)))
        lbl.bind(texture_size=lambda *a: setattr(lbl, "height", lbl.texture_size[1]))
        return lbl

    def _section_block(self, title, body_widget):
        wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
        wrap.bind(minimum_height=wrap.setter("height"))
        wrap.add_widget(SectionHeader(title=title))
        wrap.add_widget(body_widget)
        return wrap

    def _render(self):
        game = self.game
        self.fav_wrap.clear_widgets()
        fav_btn = FavoriteButton(
            game_id=game.id, size_dp=40,
            on_change=lambda *_: self._favorite_changed()
        )
        self.fav_wrap.add_widget(fav_btn)

        # --- Blok locked: kategori, judul, deskripsi, metadata ---
        self.info_block.clear_widgets()

        cat_lbl = self._label(game.category.upper(), color=AppColors.GOLD, size=AppTypography.META, bold=True)
        cat_lbl.height = dp(18)
        self.info_block.add_widget(cat_lbl)

        name_lbl = self._label(game.name, color=AppColors.TEXT, size=AppTypography.HERO, bold=True)
        self.info_block.add_widget(name_lbl)

        desc_lbl = self._label(game.description, color=AppColors.TEXT_SECONDARY, size=AppTypography.BODY)
        self.info_block.add_widget(desc_lbl)

        meta_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=AppSpacing.LG)
        meta_row.add_widget(MetadataItem(label="Pemain", value=game.player_label()))
        meta_row.add_widget(MetadataItem(label="Durasi", value=game.duration))
        diff_col = BoxLayout(orientation="vertical", spacing=dp(2))
        diff_badge_wrap = BoxLayout(size_hint_y=None, height=dp(24))
        diff_badge_wrap.add_widget(DifficultyBadge(difficulty=game.difficulty))
        diff_col.add_widget(diff_badge_wrap)
        diff_col.add_widget(self._label("Difficulty", color=AppColors.TEXT_MUTED, size=AppTypography.META, height=dp(16)))
        meta_row.add_widget(diff_col)
        self.info_block.add_widget(meta_row)

        # --- Blok scrollable: video tutorial (kalau ada) lalu section lainnya ---
        self.content.clear_widgets()

        if game.tutorial_url:
            self.content.add_widget(TutorialVideoCard(game))

        if game.about:
            self.content.add_widget(self._section_block("Tentang", self._label(game.about, color=AppColors.TEXT_SECONDARY)))
        if game.objective:
            self.content.add_widget(self._section_block("Tujuan", self._label(game.objective, color=AppColors.TEXT_SECONDARY)))
        if game.setup:
            self.content.add_widget(self._section_block("Persiapan", self._label(game.setup, color=AppColors.TEXT_SECONDARY)))

        if game.how_to_play:
            steps_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
            steps_wrap.bind(minimum_height=steps_wrap.setter("height"))
            for i, step in enumerate(game.how_to_play, start=1):
                steps_wrap.add_widget(QuickGuideStep(i, step))
            self.content.add_widget(self._section_block("Cara Bermain", steps_wrap))

        if game.special_cards:
            special_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
            special_wrap.bind(minimum_height=special_wrap.setter("height"))
            for sc in game.special_cards:
                special_wrap.add_widget(SpecialCardTile(sc))
            self.content.add_widget(self._section_block("Kartu Khusus", special_wrap))

        if game.ranking:
            ranking_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6))
            ranking_wrap.bind(minimum_height=ranking_wrap.setter("height"))
            for i, r in enumerate(game.ranking, start=1):
                ranking_wrap.add_widget(RankingCard(i, r))
            self.content.add_widget(self._section_block("Ranking / Kombinasi", ranking_wrap))

        if game.scoring:
            self.content.add_widget(self._section_block("Scoring", self._label(game.scoring, color=AppColors.TEXT_SECONDARY)))

        if game.tips:
            tips_text = "\n".join(f"\u2022 {t}" for t in game.tips)
            self.content.add_widget(self._section_block("Tips", self._label(tips_text, color=AppColors.TEXT_SECONDARY)))

        if game.variations:
            var_text = "\n".join(f"\u2022 {v}" for v in game.variations)
            self.content.add_widget(self._section_block("Variasi", self._label(var_text, color=AppColors.TEXT_SECONDARY)))

        if game.quick_guide:
            qg_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
            qg_wrap.bind(minimum_height=qg_wrap.setter("height"))
            for i, step in enumerate(game.quick_guide, start=1):
                qg_wrap.add_widget(QuickGuideStep(i, step))
            self.content.add_widget(self._section_block("Panduan Cepat", qg_wrap))

        # Selalu mulai dari atas saat membuka game (baru atau berbeda dari
        # sebelumnya), bukan meneruskan posisi scroll game yang dibuka
        # sebelumnya. Ditunda 1 frame (schedule_once) supaya scroll_y benar-benar
        # diterapkan setelah Kivy selesai menghitung ulang tinggi konten.
        Clock.schedule_once(lambda dt: setattr(self.scroll, "scroll_y", 1), 0)
