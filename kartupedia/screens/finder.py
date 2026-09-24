"""Layar Game Finder: rekomendasi game berdasarkan jawaban pengguna (tanpa AI/internet)."""
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
from kartupedia.core.database import GAME_OBJECTS
from kartupedia.core.models import Game
from kartupedia.core.utils import duration_bucket, player_bucket_matches
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.icons import VectorIcon
from kartupedia.widgets.buttons import AppButton, AppIconButton
from kartupedia.widgets.common import SectionHeader, EmptyState
from kartupedia.widgets.finder_parts import GameRecommendationCard, GameFinderStep

class GameFinderScreen(Screen):
    """Rekomendasi game berbasis jawaban pengguna, tanpa AI/internet."""

    PLAYER_OPTIONS = ["1 pemain", "2 pemain", "3-4 pemain", "5+ pemain"]
    TIME_OPTIONS = ["< 15 menit", "15-30 menit", "30-60 menit", "> 60 menit"]
    STYLE_OPTIONS = ["Santai", "Strategis", "Cepat"]
    DIFFICULTY_OPTIONS = ["Mudah", "Sedang", "Sulit"]
    MODE_OPTIONS = ["Sendiri", "Kompetitif", "Kerja sama", "Bebas"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answers = {}
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos),
                  size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(size_hint_y=None, height=dp(66),
                           padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, 0), spacing=dp(10))
        back_btn = AppIconButton(icon_text="<", size_dp=36)
        back_btn.bind(on_release=lambda *_: App.get_running_app().go_back())
        header.add_widget(back_btn)

        title_wrap = BoxLayout(orientation="vertical", spacing=0)
        title = Label(text="Game Finder", color=AppColors.TEXT, font_size=AppTypography.HEADING,
                      bold=True, halign="left", valign="bottom", size_hint_y=.6)
        title.bind(size=title.setter("text_size"))
        subtitle = Label(text="Cari game berdasarkan kebutuhanmu", color=AppColors.TEXT_MUTED,
                         font_size=sp(9.5), halign="left", valign="top", size_hint_y=.4)
        subtitle.bind(size=subtitle.setter("text_size"))
        title_wrap.add_widget(title)
        title_wrap.add_widget(subtitle)
        header.add_widget(title_wrap)
        root.add_widget(header)

        self.scroll = ScrollView(size_hint=(1, 1), bar_width=0)
        self.content = BoxLayout(orientation="vertical", size_hint_y=None,
                                 padding=(AppSpacing.LG, AppSpacing.SM, AppSpacing.LG, AppSpacing.XXL),
                                 spacing=dp(10))
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)
        self.add_widget(root)
        self._build_form()

    def _build_form(self):
        self.content.clear_widgets()
        self.answers = {}

        class _FinderIntro(FloatLayout, RoundedBG):
            pass

        intro = _FinderIntro(size_hint_y=None, height=dp(92))
        intro.init_rounded_bg(color=AppColors.STRONG, radius=dp(18), border_color=AppColors.BORDER)
        intro.add_widget(VectorIcon(name="cards", color=AppColors.GOLD_LIGHT,
                                    size_hint=(None, None), size=(dp(38), dp(38)),
                                    pos_hint={"x": .06, "center_y": .58}))
        title = Label(text="Temukan permainan yang cocok", color=AppColors.TEXT, font_size=sp(14),
                      bold=True, halign="left", valign="middle", size_hint=(.78, None),
                      height=dp(25), pos_hint={"x": .23, "top": .83})
        title.bind(size=title.setter("text_size"))
        intro.add_widget(title)
        desc = Label(text="Pilih satu jawaban pada setiap pertanyaan. Hasil akan diurutkan berdasarkan kecocokan.",
                     color=AppColors.TEXT_SECONDARY, font_size=sp(10), halign="left", valign="top",
                     size_hint=(.72, None), height=dp(34), pos_hint={"x": .23, "top": .50})
        desc.bind(width=lambda *a: setattr(desc, "text_size", (desc.width, None)))
        intro.add_widget(desc)
        self.content.add_widget(intro)

        questions = [
            ("1. Berapa orang yang akan bermain?", self.PLAYER_OPTIONS, "players"),
            ("2. Berapa banyak waktu yang tersedia?", self.TIME_OPTIONS, "duration"),
            ("3. Gaya bermain yang diinginkan?", self.STYLE_OPTIONS, "style"),
            ("4. Seberapa sulit game yang diinginkan?", self.DIFFICULTY_OPTIONS, "difficulty"),
            ("5. Mode permainan yang dicari?", self.MODE_OPTIONS, "mode"),
        ]
        for title, options, key in questions:
            self.content.add_widget(GameFinderStep(
                title, options,
                on_select=lambda value, k=key: self.answers.__setitem__(k, value),
            ))

        find_btn = AppButton(text="Temukan Rekomendasi", size_hint_y=None, height=dp(52))
        find_btn.bind(on_release=lambda *_: self._find())
        self.content.add_widget(find_btn)

        reset_btn = AppButton(text="Ulangi Jawaban", bg_color=AppColors.ELEVATED, text_color=AppColors.TEXT,
                              size_hint_y=None, height=dp(44))
        reset_btn.bind(on_release=lambda *_: self._build_form())
        self.content.add_widget(reset_btn)

        self.results_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
        self.results_wrap.bind(minimum_height=self.results_wrap.setter("height"))
        self.content.add_widget(self.results_wrap)

    def _bucket_to_game_value(self, answer):
        return {
            "1 pemain": "1",
            "2 pemain": "2",
            "3-4 pemain": "3-4",
            "5+ pemain": "5+",
        }.get(answer)

    def _score_game(self, game: Game):
        # Game casino/betting tidak dimasukkan ke hasil rekomendasi untuk penggunaan aplikasi yang aman.
        if game.category == "Casino" or "betting" in game.tags:
            return -999, []

        score = 0
        reasons = []

        players = self._bucket_to_game_value(self.answers.get("players"))
        if players and player_bucket_matches(game, players):
            score += 4
            reasons.append(f"cocok untuk {game.player_label()}")

        duration = self.answers.get("duration")
        if duration and duration_bucket(game.duration_minutes) == duration:
            score += 3
            reasons.append(f"durasi {game.duration}")

        style = self.answers.get("style")
        if style and game.style == style:
            score += 3
            reasons.append(f"gaya {game.style.lower()}")

        difficulty = self.answers.get("difficulty")
        if difficulty and game.difficulty == difficulty:
            score += 2
            reasons.append(f"level {game.difficulty.lower()}")

        mode = self.answers.get("mode")
        if mode == "Sendiri" and game.players_min == 1:
            score += 4
            reasons.append("bisa dimainkan sendiri")
        elif mode == "Kerja sama" and any(t in game.tags for t in ("kooperatif", "tim")):
            score += 4
            reasons.append("memiliki unsur kerja sama/tim")
        elif mode == "Kompetitif" and game.players_max >= 2 and not any(t in game.tags for t in ("kooperatif", "tim")):
            score += 2
            reasons.append("cocok untuk bermain kompetitif")
        elif mode == "Bebas":
            score += 1

        return score, reasons

    def _find(self):
        if not self.answers:
            self.results_wrap.clear_widgets()
            self.results_wrap.add_widget(SectionHeader(title="Pilih jawaban terlebih dahulu"))
            return

        app = App.get_running_app()
        scored = []
        for game in GAME_OBJECTS:
            score, reasons = self._score_game(game)
            if score >= 0:
                scored.append((score, game, reasons))

        scored.sort(key=lambda item: (-item[0], item[1].name))
        top = scored[:5]

        self.results_wrap.clear_widgets()
        self.results_wrap.add_widget(SectionHeader(title="Rekomendasi Untukmu"))

        if not top:
            self.results_wrap.add_widget(EmptyState(
                title="Belum menemukan game",
                subtitle="Coba ubah beberapa jawaban agar hasilnya lebih luas.",
            ))
            return

        best_score = top[0][0]
        for score, game, reasons in top:
            reason_text = " • ".join(reasons[:3]) if reasons else "Pilihan yang cukup sesuai dengan jawabanmu."
            if score == best_score:
                reason_text = "Paling cocok: " + reason_text
            self.results_wrap.add_widget(
                GameRecommendationCard(game, reason=reason_text, on_press_game=app.open_game_detail)
            )

        note = Label(text="Rekomendasi dihitung langsung dari data game di aplikasi dan dapat dicoba ulang kapan saja.",
                     color=AppColors.TEXT_MUTED, font_size=sp(9.5), halign="center", valign="middle",
                     size_hint_y=None, height=dp(34))
        note.bind(width=lambda *a: setattr(note, "text_size", (note.width, None)))
        self.results_wrap.add_widget(note)

    def on_pre_enter(self):
        self._build_form()
