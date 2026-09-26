"""Header judul section (+ tombol aksi opsional, mis. "Lihat Semua")."""
import flet as ft

from app.theme import get_palette, AppTypography


def section_header(title: str, mode: str, action_text: str = "", on_action=None) -> ft.Control:
    c = get_palette(mode)
    controls = [ft.Text(title, size=AppTypography.SECTION, weight=ft.FontWeight.BOLD,
                          color=c.TEXT, expand=True)]
    if action_text:
        controls.append(
            ft.TextButton(
                content=action_text,
                on_click=on_action,
                style=ft.ButtonStyle(color=c.PRIMARY_LIGHT),
            )
        )
    return ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                   vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=controls)
