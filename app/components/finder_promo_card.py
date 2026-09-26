"""Kartu ajakan Game Finder di Beranda."""
import flet as ft

from app.theme import get_palette, AppSpacing, AppRadius, AppTypography


def finder_promo_card(mode: str, on_tap=None) -> ft.Control:
    c = get_palette(mode)
    return ft.Container(
        on_click=on_tap,
        ink=True,
        bgcolor=c.STRONG,
        border=ft.Border.all(1, c.BORDER),
        border_radius=AppRadius.LG,
        padding=AppSpacing.MD,
        content=ft.Row(
            spacing=AppSpacing.MD,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    width=64, height=64,
                    bgcolor=c.PRIMARY_DARK,
                    border_radius=AppRadius.MD,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED, color=c.GOLD_LIGHT, size=30),
                ),
                ft.Column(
                    expand=True,
                    spacing=4,
                    controls=[
                        ft.Text("Bingung mau main apa?", size=AppTypography.SECTION,
                                 weight=ft.FontWeight.BOLD, color=c.TEXT),
                        ft.Text(
                            "Jawab beberapa pertanyaan, KartuPedia carikan game yang paling cocok.",
                            size=AppTypography.CAPTION, color=c.TEXT_SECONDARY,
                            max_lines=2, overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text("Mulai Game Finder  \u203a", size=AppTypography.CAPTION,
                                 weight=ft.FontWeight.BOLD, color=c.GOLD_LIGHT),
                    ],
                ),
            ],
        ),
    )
