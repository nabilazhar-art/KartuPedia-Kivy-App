"""Kontainer utama: ScreenManager untuk tab utama + BottomNavigation."""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from kartupedia.screens.home import HomeScreen
from kartupedia.screens.explore import ExploreScreen
from kartupedia.screens.finder import GameFinderScreen
from kartupedia.screens.random_game import RandomGameScreen
from kartupedia.screens.favorite import FavoriteScreen
from kartupedia.screens.about import AboutScreen
from kartupedia.widgets.bottom_nav import BottomNavigation


class MainShell(BoxLayout):
    """Kontainer utama: ScreenManager (untuk tab utama) + BottomNavigation."""

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.app = app

        self.tab_manager = ScreenManager(transition=FadeTransition(duration=0.12))
        self.home_screen = HomeScreen(name="home")
        self.explore_screen = ExploreScreen(name="explore")
        self.favorite_screen = FavoriteScreen(name="favorite")
        self.about_screen = AboutScreen(name="about")
        for s in (self.home_screen, self.explore_screen, self.favorite_screen, self.about_screen):
            self.tab_manager.add_widget(s)
        self.add_widget(self.tab_manager)

        self.bottom_nav = BottomNavigation(on_navigate=self._on_navigate)
        self.add_widget(self.bottom_nav)

    def _on_navigate(self, key):
        self.tab_manager.current = key

    def go_to_tab(self, key, **kwargs):
        self.tab_manager.current = key
        self.bottom_nav.set_active(key)
        if key == "explore":
            if "query" in kwargs:
                self.explore_screen.set_query(kwargs["query"])
            if "category" in kwargs:
                self.explore_screen.set_category(kwargs["category"])
