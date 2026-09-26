"""Konten layar Tentang: logo, nama app, tagline, deskripsi, info versi.

Layar statis (tidak ada state/interaksi selain warna tema), jadi cukup fungsi
sinkron biasa -- tidak perlu async seperti Home/Favorit yang membaca storage.
"""
import flet as ft

from app.config import APP_NAME, APP_TAGLINE, APP_VERSION
from app.database import GAME_OBJECTS
from app.theme import get_palette, AppSpacing, AppRadius, AppTypography

_DESC_TEXT = (
    "KartuPedia adalah ensiklopedia dan panduan permainan kartu offline. "
    "Aplikasi ini membantu kamu menemukan permainan kartu baru, memahami "
    "aturan mainnya secara lengkap, dan memilih permainan yang sesuai "
    "dengan jumlah pemain, waktu, serta gaya bermainmu. KartuPedia bukan "
    "aplikasi untuk memainkan game secara langsung, melainkan panduan "
    "referensi yang bisa diakses kapan saja tanpa koneksi internet."
)


def build_about_view(mode: str) -> ft.Control:
    c = get_palette(mode)

    logo = ft.Container(
        width=72, height=72,
        bgcolor=c.PRIMARY,
        border_radius=36,
        alignment=ft.Alignment.CENTER,
        content=ft.Text("K", size=30, weight=ft.FontWeight.BOLD, color=c.WHITE),
    )

    info_card = ft.Container(
        bgcolor=c.SURFACE,
        border=ft.Border.all(1, c.BORDER),
        border_radius=AppRadius.MD,
        padding=AppSpacing.MD,
        content=ft.Column(
            spacing=6,
            controls=[
                ft.Text(f"Versi Aplikasi: {APP_VERSION}", size=AppTypography.CAPTION, color=c.TEXT),
                ft.Text("Status: Panduan Permainan Kartu Offline",
                         size=AppTypography.CAPTION, color=c.TEXT_SECONDARY),
                ft.Text(f"Total Permainan: {len(GAME_OBJECTS)} game",
                         size=AppTypography.CAPTION, color=c.TEXT_SECONDARY),
            ],
        ),
    )

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=AppSpacing.LG,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(height=AppSpacing.MD),
            logo,
            ft.Text(APP_NAME, size=AppTypography.HEADING, weight=ft.FontWeight.BOLD, color=c.TEXT),
            ft.Text(APP_TAGLINE, size=AppTypography.BODY, color=c.GOLD_LIGHT,
                     text_align=ft.TextAlign.CENTER),
            ft.Text(_DESC_TEXT, size=AppTypography.BODY, color=c.TEXT_SECONDARY,
                     text_align=ft.TextAlign.LEFT),
            info_card,
            ft.Container(height=AppSpacing.XXL),
        ],
    )
