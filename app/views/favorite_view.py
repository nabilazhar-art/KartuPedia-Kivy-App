"""Konten layar Favorit: daftar game yang ditandai favorit."""
import flet as ft

from app.database import GAME_OBJECTS
from app.theme import get_palette, AppSpacing, AppTypography
from app.components.game_card import game_list_tile
from app.components.empty_state import empty_state
from app.async_utils import async_handler


async def build_favorite_view(storage, mode: str, on_open_game, on_go_explore) -> ft.Control:
    c = get_palette(mode)
    fav_ids = await storage.get_favorites()
    games = [g for g in GAME_OBJECTS if g.id in fav_ids]

    count_text = f"{len(games)} permainan tersimpan" if games else "Belum ada permainan tersimpan"

    if not games:
        body = empty_state(
            mode, ft.Icons.FAVORITE_BORDER_ROUNDED,
            "Belum ada permainan favorit.",
            "Tekan ikon hati pada kartu atau halaman detail untuk menyimpan permainan.",
            button_text="Jelajahi Permainan",
            on_button=async_handler(on_go_explore),
        )
    else:
        body = ft.Column(
            expand=True,
            spacing=AppSpacing.XS,
            controls=[
                game_list_tile(g, mode, on_tap=async_handler(on_open_game, g.id))
                for g in games
            ] + [ft.Container(height=AppSpacing.XXL)],
        )

    return ft.Column(
        expand=True,
        spacing=AppSpacing.XS,
        controls=[
            ft.Container(height=AppSpacing.XS),
            ft.Text(count_text, size=AppTypography.CAPTION, color=c.TEXT_MUTED),
            body,
        ],
    )
