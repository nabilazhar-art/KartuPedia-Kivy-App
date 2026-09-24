# KartuPedia

Ensiklopedia permainan kartu offline berbasis Kivy.
"Temukan permainan. Pahami aturannya. Mulai bermain."

Berisi 34 permainan kartu lintas kategori (Poker, Casino, Trick-Taking, Rummy,
Solitaire, Party, Classic, Family), lengkap dengan aturan main, quick guide,
kartu spesial, dan ranking/kombinasi. Semua data tersimpan lokal — tidak
butuh koneksi internet.

## Fitur

- **Beranda** — game unggulan, promo Game Finder, kategori, dan riwayat dilihat
- **Jelajah** — pencarian dan filter (jumlah pemain, durasi, tingkat kesulitan, kategori)
- **Game Finder** — rekomendasi game berdasarkan jawaban pengguna (tanpa AI/internet)
- **Random Game** — memilih satu game secara acak untuk dimainkan
- **Detail Game** — aturan main, quick guide bertahap, kartu spesial, ranking
- **Favorit** — game yang ditandai favorit, tersimpan secara lokal

## Menjalankan

```bash
pip install -r requirements.txt
python main.py
```

## Struktur Proyek

```
main.py                    # entry point
data/
    games.json              # database 34 game
kartupedia/
    config.py                # konstanta & setup Window
    app.py                    # kelas aplikasi utama, navigasi antar layar
    shell.py                  # ScreenManager tab utama + bottom navigation
    core/                     # data & logika (tanpa tampilan)
        theme.py                # warna & design tokens
        models.py               # model data Game
        database.py             # muat games.json
        storage.py               # simpan favorit & riwayat (JSON lokal)
        utils.py                 # filter & bucket
    widgets/                  # komponen UI yang dipakai ulang
    screens/                  # satu file per layar
```

## Menambah Game Baru

Cukup edit `data/games.json` dan tambahkan satu objek baru mengikuti struktur
game yang sudah ada (id, name, category, description, players_min/max,
duration_minutes, difficulty, how_to_play, dst). Tidak perlu menyentuh kode
Python.

## Riwayat Refactor

Proyek ini awalnya berupa satu file `main.py` (± 3.000 baris) dan telah
dipisah menjadi modul-modul di atas agar lebih mudah dikelola, tanpa
mengubah perilaku maupun tampilan aplikasi.
