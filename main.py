"""Entry point KartuPedia.

Menjalankan configure_window() lebih dulu (WAJIB sebelum import modul UI,
karena AppSpacing/AppTypography di core.theme memakai dp()/sp() yang
dihitung saat modul diimpor), baru mengimpor dan menjalankan aplikasi.
"""
from kartupedia.config import configure_window

configure_window()

from kartupedia.app import KartuPediaApp  # noqa: E402  (harus setelah configure_window)

if __name__ == "__main__":
    KartuPediaApp().run()
