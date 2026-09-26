"""Shell aplikasi: AppBar + NavigationBar (Beranda/Jelajah/Favorit/Tentang) di
level page (persisten), dengan area konten yang berganti sesuai tab aktif.

page.navigation_bar & page.appbar dipasang SEKALI di level page (bukan per
ft.View) -- ini pola resmi Flet untuk navigasi tab yang persisten. Rute "/"
di page.views hanya berisi wadah konten (content_area) yang isinya ditukar
saat pindah tab. Layar "tarik turun" sungguhan (Detail Game, Game Finder,
dst, yang butuh tombol back) memakai page.views.append(...) terpisah di
batch-batch berikutnya -- untuk sekarang ditampilkan sbg placeholder supaya
seluruh interaksi di Home tetap bisa dicoba dari sekarang.
"""
import flet as ft

from app.config import APP_NAME
from app.theme import get_palette, AppSpacing, AppTypography
from app.views.home_view import build_home_view

TABS = ["home", "explore", "favorite", "about"]
TAB_TITLES = {"home": APP_NAME, "explore": "Jelajah", "favorite": "Favorit", "about": "Tentang"}


class AppShell:
    """Menyimpan state tab aktif & merender ulang chrome/isi saat tab atau tema berubah."""

    def __init__(self, page: ft.Page, storage):
        self.page = page
        self.storage = storage
        self.tab = "home"
        self.content_area = ft.Container(expand=True)

    def mode(self) -> str:
        return "dark" if self.page.theme_mode == ft.ThemeMode.DARK else "light"

    # ---------- Siklus render ----------

    async def mount(self):
        """Dipanggil sekali di awal (dari main.py) untuk memasang shell pertama kali."""
        self.page.views.clear()
        self.page.views.append(ft.View(route="/", padding=0, controls=[self.content_area]))
        self.page.on_view_pop = self._handle_view_pop
        await self._render_chrome()
        await self._render_tab()

    async def _render_chrome(self):
        c = get_palette(self.mode())
        self.page.bgcolor = c.BG
        self.page.appbar = ft.AppBar(
            title=ft.Text(TAB_TITLES[self.tab], color=c.TEXT, weight=ft.FontWeight.BOLD),
            bgcolor=c.SURFACE,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.DARK_MODE_ROUNDED if self.mode() == "light" else ft.Icons.LIGHT_MODE_ROUNDED,
                    icon_color=c.TEXT,
                    tooltip="Ganti tema",
                    on_click=self.toggle_theme,
                ),
            ],
        )
        self.page.navigation_bar = ft.NavigationBar(
            selected_index=TABS.index(self.tab),
            bgcolor=c.SURFACE,
            on_change=self.switch_tab,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME_ROUNDED, label="Beranda"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH_OUTLINED, selected_icon=ft.Icons.SEARCH_ROUNDED, label="Jelajah"),
                ft.NavigationBarDestination(icon=ft.Icons.FAVORITE_BORDER_ROUNDED, selected_icon=ft.Icons.FAVORITE_ROUNDED, label="Favorit"),
                ft.NavigationBarDestination(icon=ft.Icons.INFO_OUTLINE_ROUNDED, selected_icon=ft.Icons.INFO_ROUNDED, label="Tentang"),
            ],
        )
        self.page.update()

    async def _render_tab(self):
        c = get_palette(self.mode())
        self.content_area.bgcolor = c.BG
        self.content_area.padding = ft.Padding.symmetric(horizontal=AppSpacing.LG, vertical=AppSpacing.XS)
        self.content_area.content = await self._build_tab_content()
        self.page.update()

    async def _build_tab_content(self) -> ft.Control:
        c = get_palette(self.mode())
        if self.tab == "home":
            return await build_home_view(
                self.storage, self.mode(),
                on_open_game=self.open_game,
                on_open_finder=self.open_finder,
                on_open_category=self.open_category,
                on_see_all_popular=self.see_all_popular,
            )
        # Explore/Favorit/Tentang sungguhan menyusul di Batch F3.
        return ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                f'Tab "{TAB_TITLES[self.tab]}" menyusul di Batch F3.',
                color=c.TEXT_MUTED, size=AppTypography.BODY, text_align=ft.TextAlign.CENTER,
            ),
        )

    # ---------- Aksi ----------

    async def toggle_theme(self, e=None):
        new_mode = "light" if self.mode() == "dark" else "dark"
        self.page.theme_mode = ft.ThemeMode.DARK if new_mode == "dark" else ft.ThemeMode.LIGHT
        await self.storage.set_theme_mode(new_mode)
        await self._render_chrome()
        await self._render_tab()

    async def switch_tab(self, e):
        self.tab = TABS[e.control.selected_index]
        await self._render_chrome()
        await self._render_tab()

    async def see_all_popular(self):
        self.tab = "explore"
        await self._render_chrome()
        await self._render_tab()

    # ---------- Navigasi ke layar lain (placeholder utk sementara) ----------

    async def _push_placeholder(self, title: str):
        c = get_palette(self.mode())
        self.page.views.append(
            ft.View(
                route=f"/placeholder/{len(self.page.views)}",
                bgcolor=c.BG,
                appbar=ft.AppBar(
                    title=ft.Text(title, color=c.TEXT),
                    bgcolor=c.SURFACE,
                    leading=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_ROUNDED, icon_color=c.TEXT,
                        on_click=self._pop_view,
                    ),
                ),
                controls=[
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment.CENTER,
                        padding=AppSpacing.LG,
                        content=ft.Text(
                            f'Layar "{title}" akan dibangun di batch berikutnya.',
                            color=c.TEXT_SECONDARY, size=AppTypography.BODY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    )
                ],
            )
        )
        self.page.update()

    async def open_game(self, game_id: str):
        await self._push_placeholder(f"Detail Game ({game_id})")

    async def open_finder(self):
        await self._push_placeholder("Game Finder")

    async def open_category(self, category: str):
        await self._push_placeholder(f"Jelajah - {category}")

    async def _handle_view_pop(self, e):
        if len(self.page.views) > 1:
            self.page.views.pop()
            self.page.update()

    def _pop_view(self, e):
        if len(self.page.views) > 1:
            self.page.views.pop()
            self.page.update()
