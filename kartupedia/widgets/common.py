"""Komponen UI umum: header section, empty state, badge, metadata, search bar.

SectionHeader, MetadataItem, dan DifficultyBadge tampilannya didefinisikan di
kv/common.kv (dimuat otomatis lewat load_common_kv() di bawah, dipanggil saat
modul ini diimpor). Class Python untuk ketiganya kini hanya mendeklarasikan
data (Kivy Properties) yang dibaca oleh KV.
"""
import os

from kivy.metrics import dp
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior

from kartupedia.core.theme import AppColors, AppSpacing, AppRadius, AppTypography
from kartupedia.widgets.base import RoundedBG
from kartupedia.widgets.icons import VectorIcon
from kartupedia.widgets.buttons import AppButton, AppIconButton

_KV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "kv", "common.kv")
_kv_loaded = False


def load_common_kv():
    """Muat kv/common.kv sekali saja (aman dipanggil berkali-kali)."""
    global _kv_loaded
    if not _kv_loaded:
        Builder.load_file(_KV_PATH)
        _kv_loaded = True


class _ActionLabel(ButtonBehavior, Label):
    """Label yang bisa ditekan; dipakai sebagai tombol aksi di SectionHeader (lihat kv/common.kv).

    Didaftarkan manual ke Factory (bukan lewat `#:import` di file KV), karena
    `#:import` yang menunjuk balik ke modul ini sendiri (kartupedia.widgets.common)
    memicu circular import saat modul ini masih di tengah proses impor.
    """
    pass


Factory.register("_ActionLabel", cls=_ActionLabel)


class SectionHeader(BoxLayout):
    """Header untuk tiap section (judul + optional aksi). Tampilan: kv/common.kv."""

    title = StringProperty("")
    action_text = StringProperty("")
    on_action = ObjectProperty(None, allownone=True)

    def _fire_action(self):
        if self.on_action:
            self.on_action()


class EmptyState(BoxLayout):
    """Tampilan saat data kosong (favorit kosong, hasil pencarian kosong, dsb)."""

    def __init__(self, icon="( )", title="Belum ada data", subtitle="", button_text="", on_button=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.padding = (AppSpacing.XL, AppSpacing.XXL)
        self.spacing = AppSpacing.SM
        from kivy.uix.label import Label
        icon_name = {"\u2661": "heart", "\u2665": "heart", "♡": "heart", "♥": "heart"}.get(icon, "cards")
        icon_wrap = BoxLayout(size_hint_y=None, height=dp(58))
        icon_wrap.add_widget(BoxLayout())
        icon_wrap.add_widget(VectorIcon(
            name=icon_name, color=AppColors.PRIMARY_LIGHT,
            size_hint=(None, None), size=(dp(44), dp(44)),
            pos_hint={"center_y": .5}, stroke=2.0
        ))
        icon_wrap.add_widget(BoxLayout())
        self.add_widget(icon_wrap)
        title_label = Label(text=title, color=AppColors.TEXT, font_size=AppTypography.SECTION,
                             bold=True, size_hint_y=None, height=dp(28))
        self.add_widget(title_label)
        if subtitle:
            sub_label = Label(text=subtitle, color=AppColors.TEXT_SECONDARY, font_size=AppTypography.BODY,
                               size_hint_y=None, height=dp(40), halign="center")
            sub_label.bind(width=lambda *a: setattr(sub_label, "text_size", (sub_label.width, None)))
            self.add_widget(sub_label)
        if button_text and on_button:
            btn = AppButton(text=button_text, size_hint=(None, None), size=(dp(200), dp(44)),
                             pos_hint={"center_x": 0.5})
            btn.bind(on_release=lambda *_: on_button())
            holder = BoxLayout(size_hint_y=None, height=dp(56))
            holder.add_widget(BoxLayout())
            holder.add_widget(btn)
            holder.add_widget(BoxLayout())
            self.add_widget(holder)
        self.bind(minimum_height=self.setter("height"))


class DifficultyBadge(BoxLayout, RoundedBG):
    """Badge kecil untuk menampilkan tingkat kesulitan. Tampilan: kv/common.kv.

    Catatan: `difficulty` tidak pernah diubah setelah widget dibuat di aplikasi
    ini, jadi badge_color/badge_bg_color (properti Python biasa, bukan Kivy
    Property) cukup dievaluasi sekali oleh KV saat widget dibuat.
    """

    difficulty = StringProperty("Mudah")

    @property
    def badge_color(self):
        return AppColors.DIFFICULTY.get(self.difficulty, AppColors.TEXT_MUTED)

    @property
    def badge_bg_color(self):
        c = self.badge_color
        return (c[0], c[1], c[2], 0.18)


class MetadataItem(BoxLayout):
    """Menampilkan satu metadata singkat (misal jumlah pemain / durasi) dengan label kecil.

    Tampilan: kv/common.kv.
    """

    label = StringProperty("")
    value = StringProperty("")


class AppSearchBar(BoxLayout, RoundedBG):
    """Search bar modern dengan ikon vektor, tinggi nyaman, dan outline lembut."""

    def __init__(self, hint_text="Cari...", on_text=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(52)
        self.padding = (dp(14), 0, dp(12), 0)
        self.spacing = dp(8)
        self.init_rounded_bg(color=AppColors.ELEVATED, radius=dp(16), border_color=AppColors.BORDER_SOFT)

        icon_wrap = BoxLayout(size_hint=(None, 1), width=dp(26))
        icon_wrap.add_widget(VectorIcon(name="search", color=AppColors.TEXT_MUTED,
                                        size_hint=(None, None), size=(dp(19), dp(19)),
                                        pos_hint={"center_x": .5, "center_y": .5}))
        self.add_widget(icon_wrap)

        self.input = TextInput(
            hint_text=hint_text, multiline=False,
            background_color=AppColors.TRANSPARENT,
            foreground_color=AppColors.TEXT,
            cursor_color=AppColors.PRIMARY_LIGHT,
            hint_text_color=AppColors.TEXT_MUTED,
            font_size=AppTypography.BODY,
            padding=(0, dp(15), 0, 0),
            size_hint=(1, 1),
        )
        if on_text:
            self.input.bind(text=lambda instance, value: on_text(value))
        self.add_widget(self.input)


# Muat kv/common.kv setelah semua class di atas didefinisikan, supaya rule KV
# (<SectionHeader>:, <MetadataItem>:, <DifficultyBadge>:) selalu punya class
# Python yang sudah lengkap saat dicocokkan.
load_common_kv()
