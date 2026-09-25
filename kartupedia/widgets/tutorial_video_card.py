"""Kartu video tutorial YouTube: thumbnail + tombol play, buka video di browser saat disentuh."""
import webbrowser

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Ellipse

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.icons import VectorIcon

# Tinggi tetap (bukan dihitung reaktif dari lebar), sama seperti pola yang
# sudah dipakai FeaturedGameCard/GameCard di seluruh aplikasi ini. Pendekatan
# reaktif (tinggi = lebar * 9/16 lewat bind()) sempat dicoba tapi menyebabkan
# video "bocor" menimpa konten lain karena rantai width->height->minimum_height
# bertingkat tidak selesai dihitung tepat waktu sebelum widget di bawahnya
# ikut diposisikan.
_THUMB_HEIGHT = dp(180)
_LABEL_ROW_HEIGHT = dp(30)


class TutorialVideoCard(ButtonBehavior, BoxLayout, RoundedBG):
    """Kartu thumbnail video tutorial YouTube untuk satu game.

    Menyentuh kartu di mana saja membuka videonya lewat browser/app YouTube
    di perangkat (webbrowser.open), bukan diputar di dalam jendela aplikasi --
    lihat pembahasan di perencanaan fitur ini untuk alasannya.

    Thumbnail dimuat dari internet (img.youtube.com) lewat AsyncImage. Kalau
    gagal dimuat (mis. tidak ada koneksi), Kivy otomatis menampilkan gambar
    "broken image" bawaannya di atas latar kartu yang tetap gelap -- kartu
    tetap terlihat & tetap bisa disentuh, aplikasi tidak crash.
    """

    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.orientation = "vertical"
        self.size_hint_y = None
        self.spacing = AppSpacing.XS
        self.height = _THUMB_HEIGHT + AppSpacing.XS + _LABEL_ROW_HEIGHT
        self.init_rounded_bg(color=AppColors.ELEVATED, radius=AppRadius.MD)

        # --- Area thumbnail, tinggi tetap ---
        thumb_wrap = FloatLayout(size_hint_y=None, height=_THUMB_HEIGHT)

        thumb = AsyncImage(
            source=game.tutorial_thumbnail_url,
            allow_stretch=True, keep_ratio=True,
            size_hint=(1, 1),
        )
        thumb_wrap.add_widget(thumb)

        # Lingkaran gelap transparan + ikon play, di tengah thumbnail.
        play_wrap = FloatLayout(
            size_hint=(None, None), size=(dp(52), dp(52)),
            pos_hint={"center_x": .5, "center_y": .5},
        )
        with play_wrap.canvas.before:
            Color(0, 0, 0, 0.55)
            self._play_bg = Ellipse(pos=play_wrap.pos, size=play_wrap.size)
        play_wrap.bind(
            pos=lambda *a: setattr(self._play_bg, "pos", play_wrap.pos),
            size=lambda *a: setattr(self._play_bg, "size", play_wrap.size),
        )
        play_wrap.add_widget(VectorIcon(
            name="play", color=AppColors.WHITE,
            size_hint=(.5, .5), pos_hint={"center_x": .54, "center_y": .5},
        ))
        thumb_wrap.add_widget(play_wrap)
        self.add_widget(thumb_wrap)

        # --- Baris label di bawah thumbnail, tinggi tetap ---
        label_row = BoxLayout(size_hint_y=None, height=_LABEL_ROW_HEIGHT,
                               padding=(AppSpacing.SM, 0), spacing=AppSpacing.XS)
        icon_wrap = BoxLayout(size_hint=(None, 1), width=dp(16))
        icon_wrap.add_widget(VectorIcon(
            name="play", color=AppColors.GOLD_LIGHT,
            size_hint=(None, None), size=(dp(11), dp(11)),
            pos_hint={"center_x": .5, "center_y": .5},
        ))
        label_row.add_widget(icon_wrap)

        text_lbl = Label(
            text="Tonton Tutorial di YouTube", color=AppColors.GOLD_LIGHT,
            font_size=AppTypography.CAPTION, bold=True,
            halign="left", valign="middle", size_hint_x=1,
        )
        text_lbl.bind(size=text_lbl.setter("text_size"))
        label_row.add_widget(text_lbl)
        self.add_widget(label_row)

    def on_release(self):
        if self.game and self.game.tutorial_url:
            webbrowser.open(self.game.tutorial_url)
