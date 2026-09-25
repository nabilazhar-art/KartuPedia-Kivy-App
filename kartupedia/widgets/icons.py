"""Ikon vektor ringan yang digambar langsung di canvas (tidak bergantung emoji/font icon)."""
from kivy.metrics import dp
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse, Mesh

from kartupedia.core.theme import AppColors


class VectorIcon(FloatLayout):
    """Ikon vektor ringan agar tidak bergantung pada emoji/font icon."""

    def __init__(self, name="search", color=None, stroke=1.6, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.icon_color = color or AppColors.TEXT
        self.stroke = dp(stroke)
        self.bind(pos=self._redraw, size=self._redraw)
        Clock.schedule_once(self._redraw, 0)

    def set_color(self, color):
        self.icon_color = color
        self._redraw()

    def _redraw(self, *args):
        self.canvas.clear()
        x, y, w, h = self.x, self.y, self.width, self.height
        if w <= 1 or h <= 1:
            return
        cx, cy = x + w/2, y + h/2
        r = min(w, h) * .28
        with self.canvas:
            Color(*self.icon_color)
            if self.name == "search":
                Ellipse(pos=(cx-r, cy-r), size=(2*r, 2*r))
                Color(*AppColors.SURFACE)
                Ellipse(pos=(cx-r+self.stroke*1.6, cy-r+self.stroke*1.6),
                        size=(2*r-self.stroke*3.2, 2*r-self.stroke*3.2))
                Color(*self.icon_color)
                Line(points=[cx+r*.70, cy-r*.70, cx+r*1.40, cy-r*1.40], width=self.stroke)
            elif self.name == "home":
                Line(points=[cx-r*1.25, cy, cx, cy+r, cx+r*1.25, cy], width=self.stroke, joint="round")
                Line(points=[cx-r*.88, cy+.02*r, cx-r*.88, cy-r, cx+r*.88, cy-r, cx+r*.88, cy+.02*r],
                     width=self.stroke, joint="round")
            elif self.name == "explore":
                Line(circle=(cx, cy, r*1.18), width=self.stroke)
                Line(points=[cx-r*.22, cy-r*.22, cx+r*.62, cy+r*.62], width=self.stroke)
                Line(circle=(cx+r*.62, cy+r*.62, r*.12), width=self.stroke)
            elif self.name in ("heart", "heart_filled"):
                # Hati digambar dengan canvas, bukan karakter Unicode, agar
                # tidak berubah menjadi kotak pada Windows/Android.
                Line(bezier=(cx, cy-r*.70, cx-r*1.55, cy-r*.02, cx-r*.90, cy+r*.95, cx, cy+r*.28),
                     width=self.stroke)
                Line(bezier=(cx, cy-r*.70, cx+r*1.55, cy-r*.02, cx+r*.90, cy+r*.95, cx, cy+r*.28),
                     width=self.stroke)
                Line(points=[cx-r*.90, cy+r*.25, cx, cy-r*1.00, cx+r*.90, cy+r*.25],
                     width=self.stroke)
            elif self.name == "info":
                Line(circle=(cx, cy, r*1.18), width=self.stroke)
                Line(points=[cx, cy-r*.48, cx, cy+r*.22], width=self.stroke)
                Ellipse(pos=(cx-self.stroke, cy+r*.58-self.stroke), size=(self.stroke*2, self.stroke*2))
            elif self.name == "chevron_right":
                Line(points=[cx-r*.45, cy-r*.72, cx+r*.25, cy, cx-r*.45, cy+r*.72], width=self.stroke)
            elif self.name == "back":
                Line(points=[cx+r*.35, cy-r*.72, cx-r*.35, cy, cx+r*.35, cy+r*.72], width=self.stroke)
            elif self.name == "cards":
                Line(rounded_rectangle=(cx-r*.95, cy-r*.72, r*1.25, r*1.48, dp(3)), width=self.stroke)
                Line(rounded_rectangle=(cx-r*.22, cy-r*.96, r*1.25, r*1.48, dp(3)), width=self.stroke)
            elif self.name == "play":
                # Segitiga play menghadap kanan, solid (bukan outline), pakai Mesh.
                p1 = (cx - r * .55, cy + r * .85)
                p2 = (cx - r * .55, cy - r * .85)
                p3 = (cx + r * .95, cy)
                verts = [p1[0], p1[1], 0, 0, p2[0], p2[1], 0, 0, p3[0], p3[1], 0, 0]
                Mesh(vertices=verts, indices=[0, 1, 2], mode="triangle_fan")
            else:
                Line(circle=(cx, cy, r), width=self.stroke)


# Didaftarkan manual ke Factory supaya bisa dipakai sebagai tag widget di file
# KV manapun (mis. "VectorIcon:" di kv/splash.kv), tanpa bergantung pada
# pendaftaran otomatis yang tidak selalu bisa diandalkan.
Factory.register("VectorIcon", cls=VectorIcon)
