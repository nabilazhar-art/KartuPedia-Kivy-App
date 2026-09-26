"""Kartu game yang dipakai ulang: versi besar (unggulan) dan versi ringkas (list tile).

Ditulis sebagai fungsi biasa (bukan class custom control) supaya tidak
bergantung pada API class-control Flet yang masih berubah-ubah -- fungsi yang
menyusun & mengembalikan native ft.Control jauh lebih stabil antar versi.
"""
import flet as ft

from app.theme import get_palette, AppSpacing, AppRadius, AppTypography


def featured_game_card(game, mode: str, on_tap=None) -> ft.Control:
    """Kartu besar untuk game unggulan di Beranda."""
    c = get_palette(mode)
    return ft.Container(
        on_click=on_tap,
        ink=True,
        bgcolor=c.SURFACE,
        border=ft.Border.all(1, c.BORDER),
        border_radius=AppRadius.LG,
        padding=AppSpacing.MD,
        content=ft.Row(
            spacing=AppSpacing.MD,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=64, height=64,
                    bgcolor=c.PRIMARY,
                    border_radius=AppRadius.MD,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.STYLE_ROUNDED, color=c.WHITE, size=32),
                ),
                ft.Column(
                    expand=True,
                    spacing=4,
                    controls=[
                        ft.Text(game.category.upper(), size=AppTypography.META,
                                 weight=ft.FontWeight.BOLD, color=c.GOLD),
                        ft.Text(game.name, size=AppTypography.HEADING,
                                 weight=ft.FontWeight.BOLD, color=c.TEXT),
                        ft.Text(game.description, size=AppTypography.CAPTION,
                                 color=c.TEXT_SECONDARY, max_lines=2,
                                 overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Row(
                            spacing=AppSpacing.SM,
                            controls=[
                                ft.Text(game.player_label(), size=AppTypography.CAPTION,
                                         weight=ft.FontWeight.BOLD, color=c.GOLD_LIGHT),
                                ft.Text("•", size=AppTypography.CAPTION, color=c.TEXT_MUTED),
                                ft.Text(game.duration, size=AppTypography.CAPTION,
                                         weight=ft.FontWeight.BOLD, color=c.GOLD_LIGHT),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


def game_list_tile(game, mode: str, on_tap=None) -> ft.Control:
    """Baris ringkas untuk daftar game (Populer, Baru Dilihat, hasil pencarian)."""
    c = get_palette(mode)
    return ft.Container(
        on_click=on_tap,
        ink=True,
        bgcolor=c.SURFACE,
        border_radius=AppRadius.MD,
        padding=AppSpacing.SM,
        content=ft.Row(
            spacing=AppSpacing.SM,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=44, height=44,
                    bgcolor=c.ELEVATED,
                    border_radius=AppRadius.SM,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.STYLE_ROUNDED, color=c.PRIMARY_LIGHT, size=22),
                ),
                ft.Column(
                    expand=True,
                    spacing=2,
                    controls=[
                        ft.Text(game.name, size=AppTypography.BODY,
                                 weight=ft.FontWeight.BOLD, color=c.TEXT,
                                 max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(f"{game.category} • {game.player_label()} • {game.duration}",
                                 size=AppTypography.META, color=c.TEXT_MUTED,
                                 max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ],
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=c.TEXT_MUTED, size=20),
            ],
        ),
    )
