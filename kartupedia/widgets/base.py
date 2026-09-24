"""Mixin dasar untuk menggambar background rounded rect di canvas widget."""
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line

from kartupedia.core.theme import AppColors, AppRadius


class RoundedBG:
    """Mixin: menggambar background rounded rect yang mengikuti ukuran widget."""

    def init_rounded_bg(self, color=AppColors.SURFACE, radius=AppRadius.MD, border_color=None, border_width=1):
        self._bg_color = color
        self._bg_radius = radius
        self._border_color = border_color
        self._border_width = border_width
        with self.canvas.before:
            self._bg_color_instr = Color(*color)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
            if border_color:
                self._border_color_instr = Color(*border_color)
                self._border_line = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, radius), width=dp(border_width))
            else:
                self._border_line = None
        self.bind(pos=self._update_rounded_bg, size=self._update_rounded_bg)

    def _update_rounded_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        if self._border_line is not None:
            self._border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self._bg_radius)

    def set_bg_color(self, color):
        self._bg_color_instr.rgba = color
