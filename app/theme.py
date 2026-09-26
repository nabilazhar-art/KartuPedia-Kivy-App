"""Sistem warna (Light & Dark) dan design tokens KartuPedia versi Flet.

Warna di sini sengaja ditulis sebagai string hex biasa (bukan lewat konstanta
`ft.Colors.*`), supaya tidak bergantung pada penamaan enum Flet yang bisa
berubah antar versi -- hex selalu valid di semua versi Flet.

Palet Dark meneruskan identitas warna KartuPedia versi Kivy (navy + violet +
gold). Palet Light baru dibuat khusus untuk versi Flet ini, memakai hue yang
sama supaya identitas brand tetap terasa sama di kedua mode.
"""
import flet as ft


class DarkColors:
    BG = "#08111F"
    SURFACE = "#101B2D"
    ELEVATED = "#17243A"
    STRONG = "#20304B"

    PRIMARY = "#7C6CF2"
    PRIMARY_LIGHT = "#A69BFF"
    PRIMARY_DARK = "#5C4ED8"
    ON_PRIMARY = "#FFFFFF"

    GOLD = "#E3B95C"
    GOLD_LIGHT = "#F4D98F"

    TEXT = "#F8FAFC"
    TEXT_SECONDARY = "#B6C0D0"
    TEXT_MUTED = "#728097"

    BORDER = "#263754"
    BORDER_SOFT = "#1D2A40"

    SUCCESS = "#69C39A"
    WARNING = "#E0AE5A"
    ERROR = "#E47D8A"

    WHITE = "#FFFFFF"

    DIFFICULTY = {"Mudah": SUCCESS, "Sedang": WARNING, "Sulit": ERROR}


class LightColors:
    BG = "#F6F6FB"
    SURFACE = "#FFFFFF"
    ELEVATED = "#F1F0FA"
    STRONG = "#E4E2F5"

    PRIMARY = "#5C4ED8"
    PRIMARY_LIGHT = "#7C6CF2"
    PRIMARY_DARK = "#4636B0"
    ON_PRIMARY = "#FFFFFF"

    GOLD = "#B9822E"
    GOLD_LIGHT = "#C99A3B"

    TEXT = "#12131A"
    TEXT_SECONDARY = "#4B5568"
    TEXT_MUTED = "#7C8798"

    BORDER = "#E1E1EC"
    BORDER_SOFT = "#EBEBF5"

    SUCCESS = "#2F9E6E"
    WARNING = "#B9822E"
    ERROR = "#C94E5E"

    WHITE = "#FFFFFF"

    DIFFICULTY = {"Mudah": SUCCESS, "Sedang": WARNING, "Sulit": ERROR}


def get_palette(mode: str):
    """mode: "dark" atau "light" -> class warna yang sesuai."""
    return DarkColors if mode == "dark" else LightColors


# ==================================================
# DESIGN TOKENS (dipertahankan dari versi Kivy)
# ==================================================
class AppSpacing:
    XXS = 4
    XS = 8
    SM = 12
    MD = 16
    LG = 20
    XL = 24
    XXL = 32


class AppRadius:
    SM = 8
    MD = 14
    LG = 18
    XL = 24
    PILL = 999


class AppTypography:
    HERO = 26
    HEADING = 21
    SECTION = 17
    BODY = 14
    CAPTION = 12
    META = 11


def build_theme(mode: str) -> ft.Theme:
    """Buat ft.Theme untuk mode "dark" atau "light", memakai palet di atas."""
    c = get_palette(mode)
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=c.PRIMARY,
            on_primary=c.ON_PRIMARY,
            secondary=c.GOLD,
            on_secondary=c.TEXT if mode == "light" else "#1A1300",
            surface=c.SURFACE,
            on_surface=c.TEXT,
            error=c.ERROR,
            on_error=c.WHITE,
            outline=c.BORDER,
        ),
        scrollbar_theme=ft.ScrollbarTheme(thumb_visibility=False),
    )
