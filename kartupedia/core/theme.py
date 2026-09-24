"""Sistem warna dan design tokens (spacing, radius, tipografi) KartuPedia."""
from kivy.metrics import dp, sp


# ==================================================
# COLOR SYSTEM
# ==================================================
def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b, alpha)


class AppColors:
    # Modern navy + violet accent
    BG = hex_to_rgba("#08111F")
    SURFACE = hex_to_rgba("#101B2D")
    ELEVATED = hex_to_rgba("#17243A")
    STRONG = hex_to_rgba("#20304B")

    PRIMARY = hex_to_rgba("#7C6CF2")
    PRIMARY_LIGHT = hex_to_rgba("#A69BFF")
    PRIMARY_DARK = hex_to_rgba("#5C4ED8")

    GOLD = hex_to_rgba("#E3B95C")
    GOLD_LIGHT = hex_to_rgba("#F4D98F")

    TEXT = hex_to_rgba("#F8FAFC")
    TEXT_SECONDARY = hex_to_rgba("#B6C0D0")
    TEXT_MUTED = hex_to_rgba("#728097")

    BORDER = hex_to_rgba("#263754")
    BORDER_SOFT = hex_to_rgba("#1D2A40")

    SUCCESS = hex_to_rgba("#69C39A")
    WARNING = hex_to_rgba("#E0AE5A")
    ERROR = hex_to_rgba("#E47D8A")
    INFO = PRIMARY

    WHITE = hex_to_rgba("#FFFFFF")
    TRANSPARENT = (0, 0, 0, 0)

    DIFFICULTY = {
        "Mudah": SUCCESS,
        "Sedang": WARNING,
        "Sulit": ERROR,
    }


# ==================================================
# DESIGN TOKENS
# ==================================================
class AppSpacing:
    XXS = dp(4)
    XS = dp(8)
    SM = dp(12)
    MD = dp(16)
    LG = dp(20)
    XL = dp(24)
    XXL = dp(32)


class AppRadius:
    SM = dp(8)
    MD = dp(14)
    LG = dp(18)
    XL = dp(24)
    PILL = dp(999)


class AppTypography:
    HERO = sp(26)
    HEADING = sp(21)
    SECTION = sp(17)
    BODY = sp(14)
    CAPTION = sp(12)
    META = sp(11)
