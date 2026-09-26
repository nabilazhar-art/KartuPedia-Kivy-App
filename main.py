"""Entry point KartuPedia (Flet)."""
import flet as ft

from app.config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from app.theme import build_theme
from app.storage import Storage
from app.shell import AppShell


async def main(page: ft.Page):
    page.title = APP_NAME
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.padding = 0
    page.theme = build_theme("light")
    page.dark_theme = build_theme("dark")

    storage = Storage(page)
    saved_mode = await storage.get_theme_mode()
    page.theme_mode = ft.ThemeMode.DARK if saved_mode == "dark" else ft.ThemeMode.LIGHT

    shell = AppShell(page, storage)
    await shell.mount()


ft.run(main)
