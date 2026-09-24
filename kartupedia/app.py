"""Kelas aplikasi utama: root ScreenManager, navigasi antar layar, dan siklus hidup app."""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition

from kartupedia.config import APP_NAME
from kartupedia.core.theme import AppColors
from kartupedia.core.database import GAME_OBJECTS, get_game_by_id
from kartupedia.core.storage import STORAGE
from kartupedia.screens.splash import SplashScreen
from kartupedia.screens.finder import GameFinderScreen
from kartupedia.screens.random_game import RandomGameScreen
from kartupedia.screens.detail import GameDetailScreen
from kartupedia.shell import MainShell


class KartuPediaApp(App):
    def build(self):
        self.title = APP_NAME
        Window.clearcolor = AppColors.BG

        self.root_manager = ScreenManager(transition=SlideTransition(duration=0.2))
        self.splash_screen = SplashScreen(name="splash")
        self.root_manager.add_widget(self.splash_screen)

        self.main_shell_screen = Screen(name="main_shell")
        self.main_shell = MainShell(self)
        self.main_shell_screen.add_widget(self.main_shell)
        self.root_manager.add_widget(self.main_shell_screen)

        self.detail_screen = GameDetailScreen(name="detail")
        self.root_manager.add_widget(self.detail_screen)

        self.finder_screen = GameFinderScreen(name="finder")
        self.root_manager.add_widget(self.finder_screen)

        self.random_screen = RandomGameScreen(name="random")
        self.root_manager.add_widget(self.random_screen)

        self.nav_stack = []
        self.pending_search_query = ""
        self.random_filters = None

        self.root_manager.current = "splash"
        return self.root_manager

    def show_main_shell(self):
        self.root_manager.current = "main_shell"

    def open_game_detail(self, game_id):
        self.detail_screen.open_game(game_id)
        self.nav_stack.append(self.root_manager.current)
        self.root_manager.current = "detail"

    def open_finder(self):
        self.nav_stack.append(self.root_manager.current)
        self.root_manager.current = "finder"

    def open_random(self):
        self.nav_stack.append(self.root_manager.current)
        self.root_manager.current = "random"

    def refresh_favorites(self):
        try:
            self.main_shell.favorite_screen.refresh()
        except Exception:
            pass

    def go_to_explore(self, category=None):
        self.main_shell.go_to_tab("explore", category=category) if category else self.main_shell.go_to_tab("explore")
        self.root_manager.current = "main_shell"

    def go_to_search(self, query):
        self.main_shell.go_to_tab("explore", query=query)
        self.root_manager.current = "main_shell"

    def go_back(self):
        if self.nav_stack:
            previous = self.nav_stack.pop()
            self.root_manager.current = previous
        else:
            self.root_manager.current = "main_shell"
