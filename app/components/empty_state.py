"""Tampilan kosong (tidak ada hasil / belum ada favorit), dengan tombol aksi opsional."""
import flet as ft

from app.theme import get_palette, AppSpacing, AppTypography


def empty_state(mode: str, icon, title: str, subtitle: str = "",
                 button_text: str = "", on_button=None) -> ft.Control:
    c = get_palette(mode)
    controls = [
        ft.Icon(icon, color=c.TEXT_MUTED, size=44),
        ft.Container(height=AppSpacing.SM),
        ft.Text(title, size=AppTypography.SECTION, weight=ft.FontWeight.BOLD,
                 color=c.TEXT, text_align=ft.TextAlign.CENTER),
    ]
    if subtitle:
        controls.append(
            ft.Text(subtitle, size=AppTypography.CAPTION, color=c.TEXT_SECONDARY,
                     text_align=ft.TextAlign.CENTER)
        )
    if button_text:
        controls.append(ft.Container(height=AppSpacing.SM))
        controls.append(
            ft.Button(
                content=button_text,
                on_click=on_button,
                bgcolor=c.PRIMARY,
                color=c.ON_PRIMARY,
            )
        )
    return ft.Container(
        expand=True,
        padding=AppSpacing.XL,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=controls,
        ),
    )
