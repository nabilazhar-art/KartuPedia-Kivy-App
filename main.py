# ==================================================
# KARTUPEDIA - Ensiklopedia Permainan Kartu Offline
# "Temukan permainan. Pahami aturannya. Mulai bermain."
# Single-file Kivy Application
# ==================================================

# ==================================================
# 01. IMPORTS
# ==================================================
import os
import json
import random
import re

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.properties import (
    StringProperty, NumericProperty, BooleanProperty,
    ListProperty, ObjectProperty
)
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse
from kivy.utils import platform

# ==================================================
# 02. APP CONFIGURATION
# ==================================================
Window.softinput_mode = "below_target"
BASE_WIDTH = 390
BASE_HEIGHT = 844

if platform not in ("android", "ios"):
    try:
        Window.size = (390, 844)
    except Exception:
        pass

APP_NAME = "KartuPedia"
APP_TAGLINE = "Temukan permainan. Pahami aturannya. Mulai bermain."
APP_VERSION = "1.0.0"

def get_storage_directory():
    if platform == "android":
        try:
            from android.storage import app_storage_path  # type: ignore
            return app_storage_path()
        except ImportError:
            return os.path.expanduser("~")

    return os.path.dirname(os.path.abspath(__file__))

STORAGE_DIR = get_storage_directory()
STORAGE_FILE = os.path.join(STORAGE_DIR, "kartupedia_data.json")

# ==================================================
# 03. COLOR SYSTEM
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
# 04. DESIGN TOKENS
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


# ==================================================
# 05. DATA MODEL
# ==================================================
class Game:
    """Representasi satu permainan kartu."""

    def __init__(self, data: dict):
        self.id = data.get("id", "")
        self.name = data.get("name", "Tanpa Nama")
        self.category = data.get("category", "Klasik")
        self.description = data.get("description", "")
        self.players_min = data.get("players_min", 1)
        self.players_max = data.get("players_max", 1)
        self.duration = data.get("duration", "15-30 menit")
        self.duration_minutes = data.get("duration_minutes", 20)
        self.difficulty = data.get("difficulty", "Mudah")
        self.tags = data.get("tags", [])
        self.style = data.get("style", "Santai")
        self.about = data.get("about", "")
        self.objective = data.get("objective", "")
        self.setup = data.get("setup", "")
        self.how_to_play = data.get("how_to_play", [])
        self.special_cards = data.get("special_cards", [])
        self.ranking = data.get("ranking", [])
        self.scoring = data.get("scoring", "")
        self.tips = data.get("tips", [])
        self.variations = data.get("variations", [])
        self.quick_guide = data.get("quick_guide", [])

    def player_label(self):
        if self.players_min == self.players_max:
            return f"{self.players_min} Pemain"
        return f"{self.players_min}-{self.players_max} Pemain"

    def matches_query(self, query: str) -> bool:
        if not query:
            return True
        q = query.strip().lower()
        haystack = " ".join([
            self.name, self.category, self.description,
            " ".join(self.tags),
        ]).lower()
        return q in haystack


# ==================================================
# 06. GAME DATABASE
# ==================================================
GAME_DATABASE = [
    {
        "id": "regicide", "name": "Regicide", "category": "Classic",
        "description": "Game kartu kooperatif melawan raja jahat menggunakan kartu standar.",
        "players_min": 1, "players_max": 4, "duration": "20-40 menit", "duration_minutes": 30,
        "difficulty": "Sedang", "tags": ["kooperatif", "fantasy", "boss battle"], "style": "Strategis",
        "about": "Regicide adalah game kooperatif fantasi di mana pemain bekerja sama mengalahkan 12 Jack, Queen, dan King sebagai musuh boss menggunakan kartu angka dan As sebagai senjata serta mantra.",
        "objective": "Kalahkan seluruh 12 kartu wajah (Jack, Queen, King) sebelum tumpukan kartu tangan pemain habis.",
        "setup": "Pisahkan kartu wajah sebagai dek musuh urut dari Jack ke King per suit, sisanya jadi dek pemain yang dibagikan sesuai jumlah pemain.",
        "how_to_play": [
            "Pemain bergiliran memainkan kartu dari tangan untuk menyerang musuh.",
            "Nilai kartu menjadi jumlah damage, suit menentukan efek khusus.",
            "Musuh membalas menyerang sesuai nilai attack-nya kecuali dilemahkan.",
            "Jika damage tidak cukup membunuh musuh, giliran berpindah ke pemain berikut.",
        ],
        "special_cards": [
            "Club: melipatgandakan damage yang diberikan ke musuh.",
            "Diamond: menambah kartu dari dek ke tangan seluruh pemain.",
            "Heart: memulihkan kartu dari discard pile ke dek pemain.",
            "Spade: mengurangi attack musuh untuk sisa giliran.",
        ],
        "ranking": [],
        "scoring": "Tidak ada skor individu; permainan menang atau kalah secara tim.",
        "tips": ["Simpan Heart untuk saat dek hampir habis.", "Kombinasikan kartu bernilai sama untuk damage lebih besar."],
        "variations": ["Mode solo dengan aturan tangan lebih besar.", "Varian kompetitif untuk pemain yang ingin saling bersaing skor."],
        "quick_guide": ["Susun dek musuh dan dek pemain.", "Bagikan kartu ke tiap pemain.", "Serang musuh bergiliran.", "Gunakan efek suit secara taktis.", "Kalahkan seluruh musuh untuk menang."],
    },
    {
        "id": "blackjack", "name": "Blackjack", "category": "Casino",
        "description": "Game kartu melawan dealer, targetkan nilai tangan sedekat mungkin dengan 21.",
        "players_min": 1, "players_max": 7, "duration": "10-20 menit", "duration_minutes": 15,
        "difficulty": "Mudah", "tags": ["casino", "dealer", "21"], "style": "Cepat",
        "about": "Blackjack, atau 21, adalah game kartu populer di mana pemain berusaha mengalahkan dealer dengan mendekati nilai 21 tanpa melebihinya.",
        "objective": "Dapatkan total nilai kartu lebih tinggi dari dealer tanpa melebihi 21.",
        "setup": "Gunakan satu atau beberapa dek standar. Dealer membagikan dua kartu ke tiap pemain dan dua kartu untuk dirinya sendiri.",
        "how_to_play": [
            "Kartu angka bernilai sesuai angkanya, kartu wajah bernilai 10, As bernilai 1 atau 11.",
            "Pemain memilih Hit untuk menambah kartu atau Stand untuk berhenti.",
            "Jika total melebihi 21, pemain langsung Bust dan kalah.",
            "Dealer bermain setelah semua pemain selesai, biasanya harus Hit di bawah 17.",
        ],
        "special_cards": ["As dapat bernilai 1 atau 11 tergantung mana yang menguntungkan.", "Kombinasi As + kartu bernilai 10 disebut Blackjack alami."],
        "ranking": [],
        "scoring": "Blackjack alami membayar lebih tinggi dari kemenangan biasa; tangan yang lebih dekat ke 21 tanpa bust menang.",
        "tips": ["Stand pada 17 ke atas umumnya aman.", "Hindari Hit berlebihan saat tangan sudah di atas 12."],
        "variations": ["Spanish 21 tanpa kartu 10.", "Blackjack Switch dengan dua tangan yang bisa ditukar."],
        "quick_guide": ["Bagikan dua kartu ke tiap pemain dan dealer.", "Pemain memilih Hit atau Stand.", "Hindari melebihi 21.", "Dealer menyelesaikan tangannya.", "Bandingkan total untuk menentukan pemenang."],
    },
    {
        "id": "baccarat", "name": "Baccarat", "category": "Casino",
        "description": "Game casino sederhana membandingkan tangan Player dan Banker mendekati nilai 9.",
        "players_min": 1, "players_max": 8, "duration": "10-15 menit", "duration_minutes": 12,
        "difficulty": "Mudah", "tags": ["casino", "banker", "elegan"], "style": "Cepat",
        "about": "Baccarat adalah game casino klasik yang elegan, di mana pemain bertaruh pada tangan Player, Banker, atau Tie yang nilainya paling dekat dengan 9.",
        "objective": "Menebak tangan mana (Player atau Banker) yang totalnya paling dekat dengan 9.",
        "setup": "Gunakan beberapa dek kartu dalam shoe. Dua tangan dibagikan: Player dan Banker, masing-masing dua kartu.",
        "how_to_play": [
            "Nilai kartu 2-9 sesuai angka, kartu 10 dan wajah bernilai 0, As bernilai 1.",
            "Jika total dua digit, hanya digit terakhir yang dihitung.",
            "Aturan kartu ketiga otomatis berlaku berdasarkan total awal.",
            "Tangan dengan nilai lebih dekat ke 9 menang.",
        ],
        "special_cards": ["Kartu 10 dan wajah dianggap bernilai 0."],
        "ranking": [],
        "scoring": "Total 8 atau 9 dari dua kartu awal disebut Natural dan otomatis menang kecuali seri.",
        "tips": ["Taruhan Banker memiliki house edge sedikit lebih rendah.", "Perhatikan komisi pada kemenangan Banker."],
        "variations": ["Mini Baccarat dengan meja lebih kecil.", "Chemin de Fer versi Prancis dengan pemain bergilir jadi Banker."],
        "quick_guide": ["Pasang taruhan pada Player, Banker, atau Tie.", "Bagikan dua kartu untuk tiap tangan.", "Terapkan aturan kartu ketiga bila perlu.", "Bandingkan total mendekati 9.", "Menangkan taruhan sesuai hasil."],
    },
    {
        "id": "war", "name": "War", "category": "Family",
        "description": "Game kartu sederhana untuk anak-anak, adu kartu tertinggi setiap ronde.",
        "players_min": 2, "players_max": 2, "duration": "10-20 menit", "duration_minutes": 15,
        "difficulty": "Mudah", "tags": ["anak", "sederhana", "keberuntungan"], "style": "Santai",
        "about": "War adalah game kartu paling sederhana, cocok untuk anak-anak, di mana kemenangan murni ditentukan oleh nilai kartu yang dibuka.",
        "objective": "Kumpulkan seluruh kartu dengan memenangkan setiap pertarungan kartu.",
        "setup": "Bagikan seluruh dek secara merata ke dua pemain tanpa melihat kartu.",
        "how_to_play": [
            "Kedua pemain membuka kartu teratas secara bersamaan.",
            "Kartu dengan nilai lebih tinggi memenangkan kedua kartu.",
            "Jika nilai sama terjadi 'War': buka tiga kartu tertutup lalu satu kartu terbuka untuk menentukan pemenang.",
            "Kartu yang dimenangkan diletakkan di bawah tumpukan pemenang.",
        ],
        "special_cards": [],
        "ranking": ["As tertinggi, lalu King, Queen, Jack, hingga angka 2 terendah."],
        "scoring": "Pemain yang menguasai seluruh kartu menang.",
        "tips": ["Kocok ulang tumpukan menang agar urutan acak.", "Gunakan batas waktu agar permainan tidak berlarut."],
        "variations": ["War tiga pemain dengan aturan modifikasi.", "Egyptian War yang menambahkan aturan slap."],
        "quick_guide": ["Bagi dek jadi dua sama rata.", "Buka kartu teratas bersamaan.", "Nilai tertinggi menang kedua kartu.", "Jika seri, lakukan War.", "Pemain dengan seluruh kartu menang."],
    },
]
GAME_DATABASE += [
    {
        "id": "texas_holdem", "name": "Texas Hold'em", "category": "Poker",
        "description": "Varian poker paling populer dengan dua kartu pribadi dan lima kartu komunitas.",
        "players_min": 2, "players_max": 9, "duration": "30-60 menit", "duration_minutes": 45,
        "difficulty": "Sedang", "tags": ["poker", "betting", "turnamen"], "style": "Strategis",
        "about": "Texas Hold'em adalah varian poker paling populer di dunia, memadukan kartu pribadi dan kartu komunitas dengan ronde taruhan bertingkat.",
        "objective": "Bentuk kombinasi kartu lima terbaik atau buat lawan fold untuk memenangkan pot.",
        "setup": "Setiap pemain mendapat dua kartu tertutup (hole cards). Dealer button dan blind bergilir searah jarum jam.",
        "how_to_play": [
            "Ronde taruhan Pre-flop dimulai setelah kartu hole dibagikan.",
            "Flop membuka tiga kartu komunitas diikuti ronde taruhan.",
            "Turn membuka kartu keempat, River membuka kartu kelima, masing-masing diikuti taruhan.",
            "Showdown menentukan pemenang berdasarkan kombinasi lima kartu terbaik.",
        ],
        "special_cards": [],
        "ranking": ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair", "High Card"],
        "scoring": "Pemenang mengambil seluruh pot berdasarkan kombinasi tertinggi atau lawan yang fold.",
        "tips": ["Perhatikan posisi meja sebelum memutuskan taruhan.", "Jangan terlalu sering bermain kartu lemah."],
        "variations": ["No-Limit dengan taruhan bebas.", "Limit Hold'em dengan batas taruhan tetap."],
        "quick_guide": ["Bagikan dua kartu hole per pemain.", "Lakukan ronde taruhan Pre-flop.", "Buka Flop, Turn, dan River bertahap.", "Lakukan taruhan tiap tahap.", "Bandingkan tangan terbaik saat Showdown."],
    },
    {
        "id": "omaha", "name": "Omaha", "category": "Poker",
        "description": "Varian poker dengan empat kartu hole, wajib pakai tepat dua kartu hole.",
        "players_min": 2, "players_max": 9, "duration": "30-60 menit", "duration_minutes": 45,
        "difficulty": "Sedang", "tags": ["poker", "betting", "kombinasi"], "style": "Strategis",
        "about": "Omaha mirip Texas Hold'em namun setiap pemain menerima empat kartu hole dan wajib menggunakan tepat dua di antaranya.",
        "objective": "Bentuk kombinasi lima kartu terbaik menggunakan tepat dua kartu hole dan tiga kartu komunitas.",
        "setup": "Setiap pemain mendapat empat kartu tertutup, lima kartu komunitas dibuka bertahap seperti Hold'em.",
        "how_to_play": [
            "Ronde taruhan berjalan sama seperti Texas Hold'em: Pre-flop, Flop, Turn, River.",
            "Pemain wajib memakai tepat dua kartu hole, tidak boleh lebih atau kurang.",
            "Kombinasi dibentuk dari dua kartu hole plus tiga kartu komunitas.",
            "Showdown menentukan kombinasi terbaik yang sah.",
        ],
        "special_cards": [],
        "ranking": ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair", "High Card"],
        "scoring": "Pemenang mengambil pot berdasarkan kombinasi sah tertinggi.",
        "tips": ["Empat kartu hole memberi lebih banyak kombinasi, hitung dengan cermat.", "Waspadai kombinasi lawan yang lebih besar karena banyak opsi kartu."],
        "variations": ["Omaha Hi-Lo membagi pot untuk tangan tertinggi dan terendah."],
        "quick_guide": ["Bagikan empat kartu hole per pemain.", "Jalankan ronde taruhan bertahap.", "Buka kartu komunitas seperti Hold'em.", "Gunakan tepat dua kartu hole.", "Tentukan pemenang saat Showdown."],
    },
    {
        "id": "five_card_draw", "name": "Five Card Draw", "category": "Poker",
        "description": "Varian poker klasik di mana pemain bisa menukar kartu untuk memperbaiki tangan.",
        "players_min": 2, "players_max": 8, "duration": "20-40 menit", "duration_minutes": 30,
        "difficulty": "Mudah", "tags": ["poker", "klasik", "draw"], "style": "Santai",
        "about": "Five Card Draw adalah bentuk poker paling tradisional, populer sejak abad ke-19, dengan mekanisme penukaran kartu yang sederhana.",
        "objective": "Miliki kombinasi lima kartu terbaik setelah kesempatan menukar kartu.",
        "setup": "Setiap pemain mendapat lima kartu tertutup di awal.",
        "how_to_play": [
            "Ronde taruhan pertama dilakukan setelah kartu dibagikan.",
            "Pemain dapat menukar hingga tiga kartu (atau empat jika memegang As) dengan kartu baru dari dek.",
            "Ronde taruhan kedua dilakukan setelah penukaran.",
            "Showdown menentukan kombinasi terbaik di antara pemain yang bertahan.",
        ],
        "special_cards": [],
        "ranking": ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair", "High Card"],
        "scoring": "Pemenang mengambil pot berdasarkan kombinasi tertinggi.",
        "tips": ["Jangan menukar terlalu banyak kartu tanpa rencana jelas.", "Pertahankan pair atau lebih sebagai dasar tangan."],
        "variations": ["Varian Jackpots yang mensyaratkan pair Jack untuk membuka taruhan."],
        "quick_guide": ["Bagikan lima kartu per pemain.", "Lakukan ronde taruhan awal.", "Tukar kartu yang tidak diinginkan.", "Lakukan ronde taruhan kedua.", "Bandingkan kombinasi saat Showdown."],
    },
    {
        "id": "seven_card_stud", "name": "Seven Card Stud", "category": "Poker",
        "description": "Varian poker dengan tujuh kartu bertahap, tanpa kartu komunitas.",
        "players_min": 2, "players_max": 8, "duration": "30-60 menit", "duration_minutes": 45,
        "difficulty": "Sulit", "tags": ["poker", "stud", "klasik"], "style": "Strategis",
        "about": "Seven Card Stud adalah varian poker populer sebelum era Texas Hold'em, di mana setiap pemain menerima kartu terbuka dan tertutup secara bertahap.",
        "objective": "Bentuk kombinasi lima kartu terbaik dari total tujuh kartu yang diterima.",
        "setup": "Setiap pemain menerima dua kartu tertutup dan satu kartu terbuka di awal.",
        "how_to_play": [
            "Kartu tambahan dibagikan satu per satu, empat kartu terbuka dan satu kartu tertutup terakhir.",
            "Ronde taruhan terjadi setelah setiap kartu terbuka dibagikan.",
            "Pemain dengan kartu terbuka tertinggi biasanya memulai taruhan.",
            "Showdown menentukan kombinasi lima kartu terbaik dari tujuh kartu.",
        ],
        "special_cards": [],
        "ranking": ["Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair", "High Card"],
        "scoring": "Pemenang mengambil pot berdasarkan kombinasi lima kartu terbaik.",
        "tips": ["Perhatikan kartu terbuka lawan untuk membaca kemungkinan tangan.", "Ingat kartu yang sudah terbuang untuk menghitung peluang."],
        "variations": ["Seven Card Stud Hi-Lo membagi pot tinggi dan rendah."],
        "quick_guide": ["Bagikan dua kartu tertutup dan satu terbuka.", "Lakukan taruhan tiap kartu terbuka baru.", "Bagikan kartu tertutup terakhir.", "Lakukan taruhan akhir.", "Bandingkan tujuh kartu saat Showdown."],
    },
    {
        "id": "hearts", "name": "Hearts", "category": "Trick-Taking",
        "description": "Game trick-taking di mana pemain menghindari kartu Hati dan Queen of Spades.",
        "players_min": 4, "players_max": 4, "duration": "30-45 menit", "duration_minutes": 35,
        "difficulty": "Sedang", "tags": ["trick-taking", "strategi", "menghindar"], "style": "Strategis",
        "about": "Hearts adalah game trick-taking di mana tujuan utamanya justru menghindari mengambil trik berisi kartu berbahaya, bukan memenangkan trik sebanyak mungkin.",
        "objective": "Kumpulkan poin sesedikit mungkin dengan menghindari kartu Hati dan Queen of Spades.",
        "setup": "Bagikan seluruh 52 kartu merata ke empat pemain, masing-masing 13 kartu.",
        "how_to_play": [
            "Sebelum ronde dimulai, pemain saling mengoper tiga kartu ke pemain lain.",
            "Pemain dengan 2 of Clubs memulai trik pertama.",
            "Pemain wajib mengikuti suit yang dimainkan bila memungkinkan.",
            "Pemenang trik adalah yang memainkan kartu tertinggi sesuai suit yang dipimpin.",
        ],
        "special_cards": ["Setiap kartu Hati bernilai 1 poin buruk.", "Queen of Spades bernilai 13 poin buruk."],
        "ranking": [],
        "scoring": "Pemain dengan poin terendah setelah mencapai batas skor (biasanya 100) menang; 'Shooting the Moon' membalik skor jika berhasil ambil semua kartu berbahaya.",
        "tips": ["Buang kartu tinggi berbahaya di awal permainan.", "Waspadai peluang lawan melakukan Shoot the Moon."],
        "variations": ["Omnibus Hearts menambahkan bonus untuk 10 of Diamonds."],
        "quick_guide": ["Bagikan 13 kartu per pemain.", "Oper tiga kartu sebelum bermain.", "Mulai dengan pemegang 2 of Clubs.", "Ikuti suit dan hindari kartu berbahaya.", "Hitung skor terendah sebagai pemenang."],
    },
    {
        "id": "spades", "name": "Spades", "category": "Trick-Taking",
        "description": "Game trick-taking berpasangan dengan bidding jumlah trik yang akan diambil.",
        "players_min": 4, "players_max": 4, "duration": "30-45 menit", "duration_minutes": 35,
        "difficulty": "Sedang", "tags": ["trick-taking", "tim", "bidding"], "style": "Strategis",
        "about": "Spades adalah game trick-taking berpasangan yang populer, di mana tim menebak (bid) jumlah trik yang bisa mereka menangkan sebelum bermain.",
        "objective": "Capai atau lampaui jumlah bid trik yang dijanjikan bersama pasangan.",
        "setup": "Empat pemain dibagi menjadi dua tim berpasangan, masing-masing menerima 13 kartu.",
        "how_to_play": [
            "Setiap pemain melakukan bid jumlah trik yang yakin bisa dimenangkan.",
            "Spade selalu menjadi suit trump sepanjang permainan.",
            "Pemain wajib mengikuti suit yang dipimpin bila memungkinkan.",
            "Trik dimenangkan oleh kartu Spade tertinggi atau kartu suit tertinggi bila tidak ada Spade.",
        ],
        "special_cards": ["Seluruh kartu Spade berfungsi sebagai trump."],
        "ranking": [],
        "scoring": "Tim mendapat 10 poin per trik sesuai bid; kelebihan trik (bags) dapat mengurangi skor bila menumpuk.",
        "tips": ["Hitung kekuatan Spade di tangan sebelum bid.", "Koordinasikan sinyal sederhana dengan pasangan."],
        "variations": ["Solo Spades tanpa berpasangan.", "Whiz atau Mirror dengan aturan bid khusus."],
        "quick_guide": ["Bagikan 13 kartu per pemain.", "Lakukan bid jumlah trik.", "Mainkan trik dengan Spade sebagai trump.", "Ikuti suit yang dipimpin.", "Hitung skor tim berdasarkan bid."],
    },
    {
        "id": "bridge", "name": "Bridge", "category": "Trick-Taking",
        "description": "Game trick-taking klasik dan kompetitif dengan sistem bidding kompleks.",
        "players_min": 4, "players_max": 4, "duration": "45-90 menit", "duration_minutes": 60,
        "difficulty": "Sulit", "tags": ["trick-taking", "tim", "kompetitif"], "style": "Strategis",
        "about": "Contract Bridge adalah salah satu game kartu paling kompleks dan kompetitif di dunia, dimainkan oleh dua pasangan dengan sistem bidding dan komunikasi kontrak.",
        "objective": "Penuhi kontrak jumlah trik yang disepakati melalui proses bidding sebelum permainan.",
        "setup": "Empat pemain berpasangan silang duduk, masing-masing menerima 13 kartu.",
        "how_to_play": [
            "Fase bidding menentukan kontrak (jumlah trik dan suit trump) melalui tawaran bertingkat.",
            "Setelah bidding selesai, dummy membuka kartunya untuk dilihat semua pemain.",
            "Declarer memainkan kartu dari tangan sendiri dan tangan dummy.",
            "Trik dimenangkan sesuai suit trump atau suit tertinggi yang dipimpin.",
        ],
        "special_cards": ["Suit trump yang disepakati saat bidding mengalahkan suit lain."],
        "ranking": [],
        "scoring": "Skor dihitung berdasarkan pemenuhan kontrak, bonus overtrick, dan penalti undertrick.",
        "tips": ["Pelajari sistem bidding standar sebelum bermain kompetitif.", "Perhatikan sinyal dari kartu yang dibuang pasangan."],
        "variations": ["Rubber Bridge dengan skor per rubber.", "Duplicate Bridge untuk turnamen."],
        "quick_guide": ["Bagikan 13 kartu per pemain.", "Lakukan proses bidding kontrak.", "Buka kartu dummy.", "Mainkan trik sesuai kontrak.", "Hitung skor berdasarkan pemenuhan kontrak."],
    },
    {
        "id": "whist", "name": "Whist", "category": "Trick-Taking",
        "description": "Game trick-taking klasik pendahulu Bridge, sederhana dan berpasangan.",
        "players_min": 4, "players_max": 4, "duration": "20-40 menit", "duration_minutes": 30,
        "difficulty": "Sedang", "tags": ["trick-taking", "tim", "klasik"], "style": "Strategis",
        "about": "Whist adalah game trick-taking klasik yang menjadi cikal bakal Bridge dan Spades, dimainkan berpasangan tanpa proses bidding.",
        "objective": "Menangkan trik sebanyak mungkin bersama pasangan untuk mencapai skor target.",
        "setup": "Seluruh 52 kartu dibagikan habis ke empat pemain yang berpasangan silang.",
        "how_to_play": [
            "Kartu terakhir yang dibagikan menentukan suit trump untuk ronde tersebut.",
            "Pemain wajib mengikuti suit yang dipimpin bila memungkinkan.",
            "Trik dimenangkan oleh kartu trump tertinggi atau kartu suit tertinggi.",
            "Pemenang trik memimpin trik berikutnya.",
        ],
        "special_cards": ["Suit trump ditentukan dari kartu terakhir yang dibagikan."],
        "ranking": [],
        "scoring": "Tim yang menangkan lebih dari enam trik mendapat poin sesuai kelebihan trik tersebut.",
        "tips": ["Perhatikan kartu trump yang sudah keluar.", "Mainkan kartu tinggi di awal saat aman."],
        "variations": ["Knockout Whist dengan babak eliminasi.", "Bid Whist yang menambahkan sistem bidding."],
        "quick_guide": ["Bagikan seluruh kartu ke empat pemain.", "Tentukan trump dari kartu terakhir.", "Ikuti suit yang dipimpin.", "Menangkan trik dengan kartu tertinggi.", "Hitung total trik tim di akhir ronde."],
    },
    {
        "id": "euchre", "name": "Euchre", "category": "Trick-Taking",
        "description": "Game trick-taking cepat menggunakan dek pendek 24 kartu.",
        "players_min": 4, "players_max": 4, "duration": "20-30 menit", "duration_minutes": 25,
        "difficulty": "Sedang", "tags": ["trick-taking", "dek pendek", "tim"], "style": "Cepat",
        "about": "Euchre adalah game trick-taking cepat yang populer di Amerika Utara, menggunakan dek pendek berisi 9 hingga As saja.",
        "objective": "Bersama pasangan, menangkan mayoritas dari lima trik dalam satu ronde.",
        "setup": "Gunakan 24 kartu (9, 10, J, Q, K, A tiap suit) dan bagikan lima kartu ke tiap pemain.",
        "how_to_play": [
            "Kartu teratas sisa dek dibalik untuk menentukan calon trump.",
            "Pemain bergiliran memilih menerima trump tersebut atau melewatkannya.",
            "Jack suit trump (Right Bower) menjadi kartu tertinggi, Jack suit sewarna (Left Bower) kedua tertinggi.",
            "Trik dimainkan mengikuti suit dengan trump mengalahkan suit lain.",
        ],
        "special_cards": ["Right Bower: Jack suit trump, kartu tertinggi.", "Left Bower: Jack suit sewarna dengan trump, kartu kedua tertinggi."],
        "ranking": [],
        "scoring": "Tim yang memanggil trump mendapat poin jika menang tiga trik atau lebih; euchre (gagal) memberi poin ke tim lawan.",
        "tips": ["Right dan Left Bower sangat kuat, rencanakan penggunaannya.", "Jangan memanggil trump dengan tangan lemah."],
        "variations": ["Euchre tiga pemain (Cutthroat).", "Stick the Dealer yang memaksa dealer memilih trump."],
        "quick_guide": ["Bagikan lima kartu per pemain dari dek 24 kartu.", "Tentukan trump dari kartu yang dibalik.", "Ikuti suit dan mainkan trump strategis.", "Menangkan tiga dari lima trik.", "Hitung skor tim tiap ronde."],
    },
    {
        "id": "oh_hell", "name": "Oh Hell", "category": "Trick-Taking",
        "description": "Game trick-taking dengan bidding tepat, salah tebak berarti tidak dapat poin.",
        "players_min": 3, "players_max": 7, "duration": "30-45 menit", "duration_minutes": 35,
        "difficulty": "Sedang", "tags": ["trick-taking", "bidding", "presisi"], "style": "Strategis",
        "about": "Oh Hell (juga dikenal sebagai Oh Well atau Blackout) adalah game trick-taking di mana pemain harus menebak dengan tepat jumlah trik yang akan dimenangkan.",
        "objective": "Tebak jumlah trik secara akurat dan penuhi tebakan tersebut untuk mendapat poin.",
        "setup": "Jumlah kartu yang dibagikan berubah tiap ronde, biasanya naik lalu turun.",
        "how_to_play": [
            "Kartu teratas sisa dek dibuka untuk menentukan suit trump ronde tersebut.",
            "Setiap pemain mengumumkan bid jumlah trik secara berurutan.",
            "Pemain wajib mengikuti suit yang dipimpin bila memungkinkan.",
            "Trik dimenangkan oleh trump tertinggi atau kartu suit tertinggi.",
        ],
        "special_cards": ["Suit trump ditentukan tiap ronde dari kartu yang dibuka."],
        "ranking": [],
        "scoring": "Bid yang tepat memberi bonus poin; meleset bid berarti poin nol atau minus tergantung varian.",
        "tips": ["Hitung ulang bid berdasarkan kartu trump yang dipegang.", "Total bid semua pemain sering tidak boleh sama dengan jumlah trik tersedia."],
        "variations": ["Varian tanpa trump untuk ronde tertentu.", "Varian dengan penalti minus untuk bid meleset."],
        "quick_guide": ["Bagikan jumlah kartu sesuai ronde.", "Tentukan trump dari kartu terbuka.", "Umumkan bid tiap pemain.", "Mainkan trik sesuai suit dan trump.", "Hitung poin berdasarkan ketepatan bid."],
    },
    {
        "id": "rummy", "name": "Rummy", "category": "Rummy",
        "description": "Game membentuk set dan run kartu untuk mengosongkan tangan lebih dulu.",
        "players_min": 2, "players_max": 6, "duration": "20-40 menit", "duration_minutes": 30,
        "difficulty": "Mudah", "tags": ["rummy", "set", "klasik"], "style": "Santai",
        "about": "Rummy adalah keluarga game kartu klasik di mana pemain menyusun kombinasi kartu berupa set atau run untuk mengosongkan tangan mereka.",
        "objective": "Jadi pemain pertama yang berhasil menyusun seluruh kartu di tangan menjadi kombinasi sah.",
        "setup": "Bagikan 7-10 kartu per pemain tergantung jumlah pemain, sisanya jadi stock pile.",
        "how_to_play": [
            "Pemain mengambil satu kartu dari stock atau discard pile tiap giliran.",
            "Susun kartu menjadi set (kartu sama nilai beda suit) atau run (urutan sama suit).",
            "Buang satu kartu ke discard pile untuk mengakhiri giliran.",
            "Permainan berakhir saat satu pemain berhasil mengosongkan tangannya.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Pemain lain menghitung poin dari kartu tersisa di tangan; total poin terendah dari beberapa ronde menang.",
        "tips": ["Simpan kartu fleksibel yang bisa masuk beberapa kombinasi.", "Perhatikan kartu yang dibuang lawan untuk membaca strategi mereka."],
        "variations": ["Indian Rummy dengan aturan joker wajib.", "500 Rummy dengan sistem skor kumulatif."],
        "quick_guide": ["Bagikan 7-10 kartu per pemain.", "Ambil kartu dari stock atau discard.", "Susun set atau run yang sah.", "Buang satu kartu tiap giliran.", "Menang saat tangan kosong lebih dulu."],
    },
    {
        "id": "gin_rummy", "name": "Gin Rummy", "category": "Rummy",
        "description": "Varian Rummy dua pemain dengan konsep 'knocking' saat deadwood rendah.",
        "players_min": 2, "players_max": 2, "duration": "20-30 menit", "duration_minutes": 25,
        "difficulty": "Sedang", "tags": ["rummy", "dua pemain", "strategi"], "style": "Strategis",
        "about": "Gin Rummy adalah varian Rummy dua pemain yang lebih strategis, terkenal dengan konsep 'knock' untuk mengakhiri ronde lebih awal.",
        "objective": "Kurangi nilai deadwood (kartu yang tidak membentuk kombinasi) serendah mungkin lalu knock.",
        "setup": "Bagikan 10 kartu ke tiap pemain, sisanya jadi stock pile dengan satu kartu dibuka sebagai discard awal.",
        "how_to_play": [
            "Pemain mengambil kartu dari stock atau discard pile tiap giliran.",
            "Susun kartu menjadi set atau run untuk mengurangi deadwood.",
            "Jika deadwood 10 poin atau kurang, pemain bisa knock untuk mengakhiri ronde.",
            "Lawan dapat 'lay off' kartu deadwood-nya ke kombinasi milik penjambak knock.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Selisih deadwood menentukan poin; 'Gin' (deadwood nol) memberi bonus tambahan.",
        "tips": ["Jangan buang kartu yang mungkin dibutuhkan lawan.", "Knock secepatnya saat deadwood sudah sangat rendah."],
        "variations": ["Oklahoma Gin dengan batas knock berubah tiap ronde.", "Hollywood Gin dengan skor tiga game paralel."],
        "quick_guide": ["Bagikan 10 kartu per pemain.", "Ambil dan buang kartu tiap giliran.", "Susun set atau run.", "Knock saat deadwood cukup rendah.", "Hitung selisih poin deadwood."],
    },
    {
        "id": "canasta", "name": "Canasta", "category": "Rummy",
        "description": "Varian Rummy berpasangan dengan target menyusun 'canasta' tujuh kartu.",
        "players_min": 2, "players_max": 6, "duration": "45-90 menit", "duration_minutes": 60,
        "difficulty": "Sulit", "tags": ["rummy", "tim", "canasta"], "style": "Strategis",
        "about": "Canasta adalah varian Rummy berpasangan asal Amerika Selatan yang berkembang menjadi salah satu game kartu paling populer pada masanya.",
        "objective": "Bersama pasangan, susun sebanyak mungkin canasta (tumpukan tujuh kartu sejenis) untuk skor tinggi.",
        "setup": "Gunakan dua dek kartu plus joker, bagikan 11-15 kartu tergantung jumlah pemain.",
        "how_to_play": [
            "Pemain mengambil kartu dari stock atau seluruh discard pile jika memenuhi syarat.",
            "Susun meld minimal tiga kartu sejenis, bisa ditambah hingga menjadi canasta tujuh kartu.",
            "Kartu liar (joker dan 2) dapat digunakan sebagai pengganti dalam meld tertentu.",
            "Ronde berakhir saat satu pemain mengosongkan tangan dengan minimal satu canasta selesai.",
        ],
        "special_cards": ["Joker dan kartu 2 berfungsi sebagai kartu liar.", "Kartu 3 merah memberi bonus, kartu 3 hitam bersifat defensif."],
        "ranking": [],
        "scoring": "Canasta alami (tanpa kartu liar) memberi poin lebih tinggi dari canasta campuran; total skor dihitung tiap ronde.",
        "tips": ["Prioritaskan menyelesaikan satu canasta penuh sebelum membuka banyak meld baru.", "Jaga kartu liar untuk melengkapi canasta besar."],
        "variations": ["Hand and Foot dengan dua set tangan per pemain.", "Samba Canasta dengan run sebagai meld tambahan."],
        "quick_guide": ["Bagikan kartu sesuai jumlah pemain.", "Ambil dari stock atau discard pile.", "Susun meld menuju canasta tujuh kartu.", "Selesaikan minimal satu canasta.", "Hitung skor akhir tim."],
    },
    {
        "id": "indian_rummy", "name": "Indian Rummy", "category": "Rummy",
        "description": "Varian Rummy 13 kartu dengan wajib satu pure sequence tanpa joker.",
        "players_min": 2, "players_max": 6, "duration": "20-30 menit", "duration_minutes": 25,
        "difficulty": "Sedang", "tags": ["rummy", "joker", "sequence"], "style": "Strategis",
        "about": "Indian Rummy adalah varian Rummy 13 kartu yang sangat populer di India, mensyaratkan minimal satu pure sequence untuk deklarasi sah.",
        "objective": "Susun seluruh 13 kartu menjadi sequence dan set yang sah lalu deklarasikan lebih dulu.",
        "setup": "Bagikan 13 kartu per pemain, satu kartu dibuka sebagai joker acak.",
        "how_to_play": [
            "Pemain mengambil satu kartu dari stock atau discard pile tiap giliran.",
            "Wajib membentuk minimal satu pure sequence (urutan sama suit tanpa joker).",
            "Kartu joker dapat menggantikan kartu apa pun kecuali pada pure sequence.",
            "Deklarasi dilakukan saat seluruh 13 kartu tersusun sah.",
        ],
        "special_cards": ["Kartu joker yang ditentukan acak tiap ronde menggantikan kartu apapun."],
        "ranking": [],
        "scoring": "Deklarasi tanpa pure sequence dianggap tidak sah dan mendapat penalti penuh; kartu tersisa dihitung sebagai poin.",
        "tips": ["Selesaikan pure sequence secepat mungkin sebagai prioritas.", "Buang kartu tinggi yang tidak berguna lebih awal."],
        "variations": ["Deals Rummy dengan jumlah ronde tetap.", "Pool Rummy dengan batas poin eliminasi."],
        "quick_guide": ["Bagikan 13 kartu per pemain.", "Tentukan kartu joker.", "Susun pure sequence lebih dulu.", "Lengkapi sequence dan set lain.", "Deklarasikan saat seluruh kartu tersusun."],
    },
    {
        "id": "crazy_eights", "name": "Crazy Eights", "category": "Party",
        "description": "Game membuang kartu sesuai suit atau angka, kartu 8 bersifat liar.",
        "players_min": 2, "players_max": 7, "duration": "10-20 menit", "duration_minutes": 15,
        "difficulty": "Mudah", "tags": ["party", "membuang kartu", "keluarga"], "style": "Santai",
        "about": "Crazy Eights adalah game kartu membuang yang menyenangkan untuk keluarga, dengan kartu angka 8 yang bisa mengganti suit permainan.",
        "objective": "Jadi pemain pertama yang berhasil membuang seluruh kartu di tangan.",
        "setup": "Bagikan 5-7 kartu per pemain, sisanya jadi stock pile dengan satu kartu dibuka sebagai awal.",
        "how_to_play": [
            "Pemain harus membuang kartu sesuai suit atau angka kartu teratas discard pile.",
            "Kartu 8 dapat dimainkan kapan saja dan mengubah suit sesuai keinginan pemain.",
            "Jika tidak punya kartu yang cocok, pemain mengambil kartu dari stock.",
            "Permainan berlanjut hingga satu pemain menghabiskan kartunya.",
        ],
        "special_cards": ["Kartu 8: liar, bisa dimainkan kapan saja dan mengubah suit."],
        "ranking": [],
        "scoring": "Kartu tersisa di tangan pemain lain dihitung sebagai poin bagi pemenang ronde.",
        "tips": ["Simpan kartu 8 untuk situasi darurat.", "Perhatikan suit yang sering diubah lawan."],
        "variations": ["Mempersulit dengan kartu Skip dan Draw Two seperti Uno."],
        "quick_guide": ["Bagikan 5-7 kartu per pemain.", "Buka satu kartu awal di discard pile.", "Mainkan kartu sesuai suit atau angka.", "Gunakan kartu 8 untuk mengubah suit.", "Menang saat tangan kosong lebih dulu."],
    },
    {
        "id": "president", "name": "President", "category": "Party",
        "description": "Game membuang kartu kompetitif dengan hierarki sosial pemenang dan pecundang.",
        "players_min": 3, "players_max": 8, "duration": "15-30 menit", "duration_minutes": 20,
        "difficulty": "Sedang", "tags": ["party", "hierarki", "kompetitif"], "style": "Cepat",
        "about": "President (juga dikenal sebagai Scum atau Daifugo) adalah game kartu membuang yang penuh strategi sosial, dengan sistem hierarki pemain tiap ronde.",
        "objective": "Jadi pemain pertama yang menghabiskan seluruh kartu untuk menjadi President ronde berikutnya.",
        "setup": "Bagikan seluruh dek merata ke semua pemain.",
        "how_to_play": [
            "Pemain pertama memainkan kartu atau kombinasi kartu apa saja untuk memulai.",
            "Pemain berikutnya harus memainkan kartu bernilai sama atau lebih tinggi dengan jumlah kartu sama.",
            "Pemain yang tidak bisa atau tidak mau bermain harus pass.",
            "Ronde berakhir saat semua pass kecuali satu pemain, tumpukan dibuang dan pemain itu memimpin lagi.",
        ],
        "special_cards": ["Kartu 2 sering dianggap kartu terkuat.", "Kombinasi empat kartu sama (bom) bisa mengalahkan kartu tinggi."],
        "ranking": [],
        "scoring": "Urutan pemain menghabiskan kartu menentukan status: President, Vice President, hingga Scum.",
        "tips": ["Buang kartu rendah lebih dulu saat memungkinkan.", "Simpan kombinasi kuat untuk momen kritis."],
        "variations": ["Aturan tukar kartu antara President dan Scum di ronde berikutnya.", "Aturan revolusi yang membalik urutan kekuatan kartu."],
        "quick_guide": ["Bagikan seluruh kartu ke pemain.", "Mulai dengan kartu atau kombinasi bebas.", "Naikkan nilai kartu tiap giliran.", "Pass jika tidak bisa melanjutkan.", "Pemain pertama habis kartu jadi President."],
    },
    {
        "id": "mau_mau", "name": "Mau-Mau", "category": "Party",
        "description": "Game membuang kartu populer di Eropa mirip Crazy Eights dengan aturan tambahan.",
        "players_min": 2, "players_max": 6, "duration": "15-25 menit", "duration_minutes": 20,
        "difficulty": "Mudah", "tags": ["party", "membuang kartu", "eropa"], "style": "Santai",
        "about": "Mau-Mau adalah game kartu populer di Jerman dan Eropa Tengah, mirip dengan Crazy Eights namun memiliki kartu aksi tambahan yang lebih dinamis.",
        "objective": "Jadi pemain pertama yang berhasil membuang seluruh kartu di tangan.",
        "setup": "Bagikan 5-7 kartu per pemain, sisanya jadi stock pile dengan satu kartu dibuka sebagai awal.",
        "how_to_play": [
            "Pemain membuang kartu sesuai suit atau angka kartu teratas.",
            "Kartu 7 memaksa pemain berikutnya mengambil dua kartu kecuali punya kartu 7 lain.",
            "Kartu 8 melewati giliran pemain berikutnya.",
            "Kartu Jack bersifat liar dan mengubah suit permainan.",
        ],
        "special_cards": ["Kartu 7: memaksa lawan mengambil dua kartu.", "Kartu 8: melewati giliran lawan.", "Jack: liar, mengubah suit."],
        "ranking": [],
        "scoring": "Kartu tersisa di tangan pemain lain dihitung sebagai poin bagi pemenang.",
        "tips": ["Simpan kartu 7 sebagai pertahanan dari serangan lawan.", "Gunakan Jack di saat kritis untuk mengubah arah permainan."],
        "variations": ["Penambahan aturan 'Mau' wajib diucapkan saat kartu tersisa satu."],
        "quick_guide": ["Bagikan 5-7 kartu per pemain.", "Mainkan kartu sesuai suit atau angka.", "Gunakan kartu aksi 7, 8, dan Jack.", "Ucapkan 'Mau' saat kartu tersisa satu.", "Menang saat tangan kosong lebih dulu."],
    },
    {
        "id": "klondike", "name": "Klondike (Solitaire)", "category": "Solitaire",
        "description": "Solitaire klasik paling terkenal, susun kartu ke foundation berdasarkan suit.",
        "players_min": 1, "players_max": 1, "duration": "10-20 menit", "duration_minutes": 15,
        "difficulty": "Mudah", "tags": ["solitaire", "single player", "klasik"], "style": "Santai",
        "about": "Klondike adalah bentuk Solitaire paling terkenal di dunia, sering disebut sebagai 'Solitaire' saja karena kepopulerannya.",
        "objective": "Pindahkan seluruh kartu ke empat foundation pile berurutan dari As hingga King per suit.",
        "setup": "Susun tableau tujuh kolom dengan jumlah kartu bertambah, kartu teratas tiap kolom terbuka, sisanya jadi stock pile.",
        "how_to_play": [
            "Susun kartu di tableau secara turun dan berselang warna (merah-hitam).",
            "Pindahkan As ke foundation begitu terbuka, lalu lanjutkan urutan menaik per suit.",
            "Ambil kartu dari stock pile saat tidak ada langkah di tableau.",
            "Permainan menang saat seluruh kartu tersusun rapi di foundation.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Skor dihitung dari jumlah kartu berhasil dipindah ke foundation, waktu, dan jumlah langkah.",
        "tips": ["Buka kartu tertutup di tableau sesegera mungkin.", "Jangan buru-buru memindah kartu ke foundation bila masih dibutuhkan di tableau."],
        "variations": ["Klondike Draw 1 dan Draw 3 yang mengatur jumlah kartu diambil dari stock.", "Vegas Scoring dengan sistem taruhan skor."],
        "quick_guide": ["Susun tableau tujuh kolom.", "Pindahkan As ke foundation.", "Susun tableau turun berselang warna.", "Ambil kartu dari stock saat buntu.", "Selesaikan seluruh foundation untuk menang."],
    },
    {
        "id": "spider", "name": "Spider (Solitaire)", "category": "Solitaire",
        "description": "Solitaire dua dek dengan tujuan menyusun urutan lengkap satu suit.",
        "players_min": 1, "players_max": 1, "duration": "15-30 menit", "duration_minutes": 20,
        "difficulty": "Sulit", "tags": ["solitaire", "dua dek", "tantangan"], "style": "Santai",
        "about": "Spider Solitaire menggunakan dua dek kartu penuh dan dikenal sebagai salah satu varian Solitaire paling menantang.",
        "objective": "Susun urutan K hingga As dalam satu suit yang sama untuk menghapusnya dari tableau.",
        "setup": "Susun tableau 10 kolom dari dua dek kartu, sebagian besar tertutup kecuali kartu teratas.",
        "how_to_play": [
            "Pindahkan kartu secara menurun tanpa memandang suit, meski urutan satu suit lebih mudah dipindah bersamaan.",
            "Urutan lengkap satu suit dari King ke As otomatis terhapus dari tableau.",
            "Ambil sepuluh kartu baru dari stock saat tableau buntu.",
            "Permainan menang saat seluruh kartu berhasil dihapus dari tableau.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Skor dihitung dari jumlah langkah dan kecepatan menyelesaikan seluruh tumpukan.",
        "tips": ["Prioritaskan membuka kartu tertutup di kolom terpanjang.", "Jaga agar tidak menumpuk kartu campur suit terlalu banyak."],
        "variations": ["Spider satu suit untuk pemula.", "Spider empat suit untuk level ahli."],
        "quick_guide": ["Susun tableau 10 kolom dari dua dek.", "Pindahkan kartu menurun antar kolom.", "Susun urutan lengkap satu suit.", "Hapus urutan lengkap dari tableau.", "Selesaikan seluruh kartu untuk menang."],
    },
    {
        "id": "freecell", "name": "FreeCell", "category": "Solitaire",
        "description": "Solitaire dengan sel bebas untuk menyimpan kartu sementara, hampir selalu bisa dimenangkan.",
        "players_min": 1, "players_max": 1, "duration": "10-20 menit", "duration_minutes": 15,
        "difficulty": "Sedang", "tags": ["solitaire", "puzzle", "strategi"], "style": "Santai",
        "about": "FreeCell adalah varian Solitaire berbasis strategi penuh tanpa keberuntungan acak, karena seluruh kartu terbuka sejak awal.",
        "objective": "Pindahkan seluruh kartu ke foundation pile berurutan dari As hingga King per suit.",
        "setup": "Susun tableau delapan kolom dengan seluruh kartu terbuka, sediakan empat free cell kosong.",
        "how_to_play": [
            "Pindahkan kartu di tableau secara menurun dan berselang warna.",
            "Gunakan free cell untuk menyimpan sementara satu kartu apa saja.",
            "Pindahkan kartu ke foundation begitu urutannya memungkinkan.",
            "Rencanakan langkah karena seluruh kartu terlihat sejak awal.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Skor dihitung dari jumlah langkah dan penggunaan free cell seefisien mungkin.",
        "tips": ["Jangan mengisi seluruh free cell sekaligus tanpa rencana.", "Cari kombinasi langkah yang membebaskan banyak kartu sekaligus."],
        "variations": ["FreeCell dengan dua sel bebas untuk tingkat kesulitan lebih tinggi."],
        "quick_guide": ["Susun tableau delapan kolom terbuka.", "Gunakan free cell untuk kartu sementara.", "Susun tableau turun berselang warna.", "Pindahkan kartu ke foundation.", "Selesaikan seluruh foundation untuk menang."],
    },
    {
        "id": "pyramid", "name": "Pyramid (Solitaire)", "category": "Solitaire",
        "description": "Solitaire dengan kartu tersusun piramida, pasangkan kartu berjumlah 13.",
        "players_min": 1, "players_max": 1, "duration": "10-15 menit", "duration_minutes": 12,
        "difficulty": "Sedang", "tags": ["solitaire", "puzzle", "pasangan"], "style": "Santai",
        "about": "Pyramid Solitaire menyusun kartu dalam bentuk piramida dan mengharuskan pemain memasangkan kartu yang jumlahnya 13.",
        "objective": "Hapus seluruh kartu piramida dengan memasangkan kartu terbuka yang totalnya 13.",
        "setup": "Susun 28 kartu membentuk piramida tujuh baris, sisanya jadi stock pile.",
        "how_to_play": [
            "Hanya kartu yang tidak tertutup kartu lain di bawahnya yang bisa dipasangkan.",
            "Pasangkan dua kartu terbuka yang jumlah nilainya 13, King dihapus sendirian karena bernilai 13.",
            "Ambil kartu dari stock pile jika tidak ada pasangan tersedia di piramida.",
            "Permainan menang saat seluruh kartu piramida berhasil dihapus.",
        ],
        "special_cards": ["King bernilai 13 dan bisa dihapus sendirian tanpa pasangan.", "As selalu bernilai 1."],
        "ranking": [],
        "scoring": "Skor dihitung dari jumlah kartu piramida yang berhasil dihapus.",
        "tips": ["Prioritaskan kartu yang membuka banyak kartu baru di baris bawah.", "Rencanakan pasangan sebelum menarik kartu baru dari stock."],
        "variations": ["Varian dengan batas jumlah putaran stock pile."],
        "quick_guide": ["Susun 28 kartu bentuk piramida.", "Cari kartu terbuka berjumlah 13.", "Pasangkan dan hapus kartu tersebut.", "Ambil kartu baru dari stock bila buntu.", "Hapus seluruh piramida untuk menang."],
    },
    {
        "id": "golf", "name": "Golf (Solitaire)", "category": "Solitaire",
        "description": "Solitaire dengan target membuang kartu berurutan naik atau turun tanpa suit.",
        "players_min": 1, "players_max": 1, "duration": "10-15 menit", "duration_minutes": 12,
        "difficulty": "Mudah", "tags": ["solitaire", "sederhana", "santai"], "style": "Santai",
        "about": "Golf Solitaire adalah game santai dengan aturan sederhana, dinamakan seperti golf karena skor lebih rendah lebih baik.",
        "objective": "Buang sebanyak mungkin kartu tableau ke discard pile mengikuti urutan naik atau turun.",
        "setup": "Susun tableau tujuh kolom dengan lima kartu terbuka tiap kolom, satu kartu dibuka sebagai discard awal.",
        "how_to_play": [
            "Pindahkan kartu teratas tableau ke discard pile jika nilainya satu tingkat lebih tinggi atau rendah.",
            "Suit tidak berpengaruh, hanya urutan angka yang penting.",
            "Ambil kartu baru dari stock pile saat tableau buntu.",
            "Permainan menang jika seluruh tableau berhasil dikosongkan.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Skor dihitung dari jumlah kartu tableau yang berhasil dibuang, makin sedikit tersisa makin baik.",
        "tips": ["King tidak memiliki kartu berikutnya, rencanakan penempatannya.", "Prioritaskan membuka kartu yang menghalangi kolom lain."],
        "variations": ["Varian dengan urutan melingkar dari King kembali ke As."],
        "quick_guide": ["Susun tableau tujuh kolom terbuka.", "Buang kartu berurutan naik atau turun.", "Ambil kartu baru saat buntu.", "Lanjutkan hingga tableau kosong.", "Hitung sisa kartu sebagai skor."],
    },
    {
        "id": "yukon", "name": "Yukon (Solitaire)", "category": "Solitaire",
        "description": "Solitaire mirip Klondike tanpa stock pile, seluruh kartu tableau terbuka sejak awal.",
        "players_min": 1, "players_max": 1, "duration": "15-25 menit", "duration_minutes": 20,
        "difficulty": "Sulit", "tags": ["solitaire", "tantangan", "strategi"], "style": "Santai",
        "about": "Yukon adalah varian Solitaire yang lebih menantang dari Klondike karena tidak ada stock pile, seluruh kartu tableau terlihat sejak awal.",
        "objective": "Pindahkan seluruh kartu ke foundation pile berurutan dari As hingga King per suit.",
        "setup": "Susun tableau tujuh kolom dengan sebagian besar kartu terbuka sejak awal, tanpa stock pile tersisa.",
        "how_to_play": [
            "Pindahkan kelompok kartu (bukan hanya satu) di tableau meski urutannya tidak berselang warna sempurna.",
            "Susun tableau turun dan berselang warna untuk memudahkan pemindahan ke foundation.",
            "Pindahkan kartu ke foundation begitu urutannya memungkinkan.",
            "Permainan menang saat seluruh kartu tersusun di foundation.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Skor dihitung dari jumlah langkah dan kartu berhasil dipindah ke foundation.",
        "tips": ["Rencanakan pemindahan kelompok kartu besar dengan cermat.", "Fokus membuka kartu tertutup di kolom terpanjang lebih dulu."],
        "variations": ["Varian Russian Solitaire dengan aturan pemindahan lebih ketat."],
        "quick_guide": ["Susun tableau tujuh kolom terbuka.", "Pindahkan kelompok kartu antar kolom.", "Susun turun berselang warna.", "Pindahkan kartu ke foundation.", "Selesaikan seluruh foundation untuk menang."],
    },
    {
        "id": "memory_match", "name": "Memory Match", "category": "Family",
        "description": "Game mengingat posisi kartu berpasangan yang tertutup di atas meja.",
        "players_min": 1, "players_max": 6, "duration": "10-20 menit", "duration_minutes": 15,
        "difficulty": "Mudah", "tags": ["memori", "anak", "keluarga"], "style": "Santai",
        "about": "Memory Match adalah game klasik untuk melatih daya ingat, cocok dimainkan sendiri maupun bersama keluarga.",
        "objective": "Kumpulkan pasangan kartu terbanyak dengan mengingat posisi kartu yang sudah dibuka.",
        "setup": "Susun seluruh kartu tertutup secara acak dalam grid rapi di atas meja.",
        "how_to_play": [
            "Pemain membuka dua kartu secara bergiliran untuk mencari pasangan.",
            "Jika kedua kartu cocok, pemain mengambil pasangan tersebut dan bermain lagi.",
            "Jika tidak cocok, kartu ditutup kembali dan giliran berpindah ke pemain berikutnya.",
            "Permainan berakhir saat seluruh kartu berhasil dipasangkan.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Pemain dengan pasangan kartu terbanyak di akhir permainan menang.",
        "tips": ["Ingat posisi kartu yang sudah pernah dibuka lawan.", "Fokus pada area grid yang belum banyak terbuka."],
        "variations": ["Versi kecepatan dengan batas waktu tiap giliran."],
        "quick_guide": ["Susun kartu tertutup dalam grid.", "Buka dua kartu tiap giliran.", "Ambil pasangan yang cocok.", "Tutup kembali bila tidak cocok.", "Hitung pasangan terbanyak di akhir."],
    },
    {
        "id": "concentration", "name": "Concentration", "category": "Family",
        "description": "Varian klasik Memory Match dengan fokus penuh pada posisi kartu tersembunyi.",
        "players_min": 1, "players_max": 8, "duration": "10-20 menit", "duration_minutes": 15,
        "difficulty": "Mudah", "tags": ["memori", "konsentrasi", "keluarga"], "style": "Santai",
        "about": "Concentration adalah nama lain sekaligus varian klasik dari Memory Match yang menekankan konsentrasi penuh saat mengingat posisi kartu.",
        "objective": "Kumpulkan pasangan kartu terbanyak melalui daya ingat dan konsentrasi.",
        "setup": "Susun seluruh kartu tertutup dalam grid rapi, bisa menggunakan satu atau dua dek tergantung jumlah pemain.",
        "how_to_play": [
            "Setiap pemain membuka dua kartu secara bergiliran.",
            "Kartu yang cocok diambil oleh pemain dan memberi giliran tambahan.",
            "Kartu yang tidak cocok ditutup kembali di posisi semula.",
            "Permainan selesai saat seluruh kartu di grid sudah dipasangkan.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Pemenang ditentukan dari jumlah pasangan kartu terbanyak.",
        "tips": ["Buat pola mental grid untuk mempermudah mengingat posisi.", "Perhatikan giliran lawan karena mereka juga membuka informasi baru."],
        "variations": ["Versi tim di mana pasangan saling membantu mengingat posisi."],
        "quick_guide": ["Susun kartu tertutup dalam grid.", "Buka dua kartu tiap giliran.", "Ambil pasangan yang cocok.", "Lanjutkan giliran bila berhasil.", "Hitung pasangan terbanyak sebagai pemenang."],
    },
    {
        "id": "spoons", "name": "Spoons", "category": "Party",
        "description": "Game party cepat mengumpulkan empat kartu sama sambil berebut sendok.",
        "players_min": 3, "players_max": 8, "duration": "10-15 menit", "duration_minutes": 12,
        "difficulty": "Mudah", "tags": ["party", "reaksi cepat", "seru"], "style": "Cepat",
        "about": "Spoons adalah game party yang penuh tawa dan refleks cepat, menggabungkan permainan kartu dengan aksi berebut sendok.",
        "objective": "Kumpulkan empat kartu bernilai sama lebih dulu lalu ambil sendok sebelum kehabisan.",
        "setup": "Letakkan sendok di tengah meja berjumlah satu kurang dari jumlah pemain, tiap pemain menerima empat kartu.",
        "how_to_play": [
            "Setiap pemain mengambil satu kartu dan membuang satu kartu secara terus-menerus dan cepat.",
            "Tujuannya adalah mengumpulkan empat kartu dengan nilai yang sama.",
            "Begitu ada pemain mendapat empat kartu sama, ia diam-diam mengambil sendok.",
            "Pemain lain harus cepat menyadari dan ikut mengambil sendok sebelum kehabisan.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Pemain yang tidak kebagian sendok kalah di ronde tersebut dan tersingkir bertahap.",
        "tips": ["Perhatikan gerak-gerik pemain lain, bukan hanya kartu sendiri.", "Jangan terlalu jelas menunjukkan sudah memiliki empat kartu sama."],
        "variations": ["Versi tanpa sendok menggunakan benda lain sebagai penanda."],
        "quick_guide": ["Siapkan sendok satu kurang dari jumlah pemain.", "Bagikan empat kartu per pemain.", "Ambil dan buang kartu secara cepat.", "Ambil sendok saat dapat empat kartu sama.", "Pemain tanpa sendok tersingkir."],
    },
    {
        "id": "kemps", "name": "Kemps", "category": "Party",
        "description": "Game tim dengan sinyal rahasia untuk menandakan empat kartu sejenis.",
        "players_min": 4, "players_max": 8, "duration": "15-25 menit", "duration_minutes": 20,
        "difficulty": "Sedang", "tags": ["party", "tim", "sinyal"], "style": "Cepat",
        "about": "Kemps adalah game kartu tim yang unik karena mengandalkan sinyal rahasia antar pasangan tanpa berbicara.",
        "objective": "Bersama pasangan, jadi tim pertama yang mengumpulkan empat kartu sama dan berhasil memberi sinyal 'Kemps'.",
        "setup": "Bagi pemain menjadi pasangan yang duduk berhadapan, masing-masing menerima empat kartu.",
        "how_to_play": [
            "Setiap pemain menukar satu kartu dengan pemain lain di tim berbeda secara bersamaan.",
            "Tujuannya adalah mengumpulkan empat kartu bernilai sama secepat mungkin.",
            "Saat berhasil, pemain memberi sinyal rahasia ke pasangannya tanpa berbicara.",
            "Pasangan yang menyadari sinyal berteriak 'Kemps' untuk menang ronde tersebut.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Tim yang berhasil berteriak Kemps dengan benar memenangkan ronde.",
        "tips": ["Sepakati sinyal sederhana dan tidak mencolok dengan pasangan.", "Perhatikan pasangan lawan untuk mendeteksi sinyal mereka."],
        "variations": ["Varian dengan penalti jika salah teriak Kemps."],
        "quick_guide": ["Bagi pemain menjadi pasangan berhadapan.", "Bagikan empat kartu per pemain.", "Tukar kartu secara bersamaan tiap ronde.", "Beri sinyal rahasia saat dapat empat sama.", "Pasangan berteriak Kemps untuk menang."],
    },
    {
        "id": "egyptian_ratscrew", "name": "Egyptian Ratscrew", "category": "Party",
        "description": "Game refleks cepat menepuk tumpukan kartu saat pola tertentu muncul.",
        "players_min": 2, "players_max": 8, "duration": "10-20 menit", "duration_minutes": 15,
        "difficulty": "Sedang", "tags": ["party", "refleks", "seru"], "style": "Cepat",
        "about": "Egyptian Ratscrew adalah game kartu cepat dan energik yang menuntut refleks tinggi untuk menepuk tumpukan kartu di momen tepat.",
        "objective": "Kumpulkan seluruh kartu dengan menepuk tumpukan saat pola tertentu muncul.",
        "setup": "Bagikan seluruh dek merata ke semua pemain tanpa melihat kartu.",
        "how_to_play": [
            "Pemain bergiliran menumpuk kartu dari tangan ke tengah meja secara terbuka.",
            "Kartu wajah dan As memicu aturan khusus yang mengubah giliran menepuk.",
            "Pemain menepuk tumpukan saat muncul pola seperti kartu kembar atau sandwich.",
            "Pemain yang menepuk paling cepat dan benar mengambil seluruh tumpukan.",
        ],
        "special_cards": ["As: memicu giliran menumpuk empat kartu tambahan.", "King: memicu tiga kartu tambahan.", "Queen: dua kartu tambahan.", "Jack: satu kartu tambahan."],
        "ranking": [],
        "scoring": "Pemain yang menguasai seluruh kartu di akhir permainan menang.",
        "tips": ["Fokus pada pola dua kartu kembar berurutan atau sandwich.", "Jaga kuku tetap pendek demi keamanan bermain."],
        "variations": ["Aturan penalti kartu bagi yang menepuk salah."],
        "quick_guide": ["Bagi seluruh kartu ke pemain.", "Tumpuk kartu secara bergiliran.", "Terapkan aturan kartu wajah dan As.", "Tepuk tumpukan saat pola muncul.", "Kumpulkan seluruh kartu untuk menang."],
    },
    {
        "id": "old_maid", "name": "Old Maid", "category": "Family",
        "description": "Game keluarga sederhana menghindari memegang kartu 'Old Maid' tunggal.",
        "players_min": 2, "players_max": 8, "duration": "10-15 menit", "duration_minutes": 12,
        "difficulty": "Mudah", "tags": ["keluarga", "anak", "sederhana"], "style": "Santai",
        "about": "Old Maid adalah game kartu klasik untuk anak-anak, sederhana dan menyenangkan, sering menjadi pengenalan pertama pada permainan kartu.",
        "objective": "Buang seluruh pasangan kartu dan hindari menjadi orang terakhir yang memegang kartu Old Maid.",
        "setup": "Buang satu Queen dari dek sehingga tersisa satu Queen tunggal, bagikan seluruh kartu ke pemain.",
        "how_to_play": [
            "Pemain memeriksa tangan dan membuang pasangan kartu bernilai sama.",
            "Secara bergiliran, pemain mengambil satu kartu acak dari tangan pemain di sebelahnya.",
            "Jika mendapat pasangan baru, buang pasangan tersebut.",
            "Permainan berlanjut hingga hanya tersisa satu kartu Queen tunggal di satu pemain.",
        ],
        "special_cards": ["Queen tunggal (Old Maid): kartu yang harus dihindari hingga akhir."],
        "ranking": [],
        "scoring": "Pemain yang memegang Old Maid di akhir permainan dianggap kalah.",
        "tips": ["Susun kartu serapi mungkin agar lawan sulit menebak posisi Old Maid.", "Perhatikan ekspresi lawan saat mengambil kartu."],
        "variations": ["Versi bertema dengan kartu karakter khusus menggantikan Queen."],
        "quick_guide": ["Buang satu Queen dari dek.", "Bagikan seluruh kartu ke pemain.", "Buang pasangan kartu yang cocok.", "Ambil kartu acak dari pemain sebelah.", "Pemain tanpa Old Maid di akhir menang."],
    },
    {
        "id": "go_fish", "name": "Go Fish", "category": "Family",
        "description": "Game keluarga meminta kartu ke pemain lain untuk membentuk set empat kartu.",
        "players_min": 2, "players_max": 6, "duration": "10-20 menit", "duration_minutes": 15,
        "difficulty": "Mudah", "tags": ["keluarga", "anak", "klasik"], "style": "Santai",
        "about": "Go Fish adalah game kartu ramah anak yang sangat populer, mengajarkan konsep bertanya dan strategi sederhana.",
        "objective": "Kumpulkan sebanyak mungkin set empat kartu bernilai sama.",
        "setup": "Bagikan 5-7 kartu per pemain, sisanya diletakkan tertutup sebagai 'kolam' di tengah.",
        "how_to_play": [
            "Pemain bergiliran meminta kartu bernilai tertentu ke pemain lain yang dipilih.",
            "Jika pemain yang diminta punya kartu tersebut, ia wajib memberikannya.",
            "Jika tidak punya, pemain yang bertanya harus 'Go Fish' mengambil kartu dari kolam.",
            "Set empat kartu sama diletakkan terbuka di depan pemain sebagai poin.",
        ],
        "special_cards": [],
        "ranking": [],
        "scoring": "Pemain dengan jumlah set kartu terbanyak di akhir permainan menang.",
        "tips": ["Ingat kartu yang pernah diminta lawan untuk menebak tangan mereka.", "Jangan lupa untuk 'Go Fish' dengan sopan saat kalah bertanya."],
        "variations": ["Versi dengan set hanya butuh tiga kartu untuk pemain lebih muda."],
        "quick_guide": ["Bagikan 5-7 kartu per pemain.", "Minta kartu ke pemain lain.", "Ambil dari kolam bila tidak diberi.", "Kumpulkan set empat kartu sama.", "Set terbanyak di akhir menang."],
    },
]


def get_game_by_id(game_id: str):
    for g in GAME_OBJECTS:
        if g.id == game_id:
            return g
    return None


GAME_OBJECTS = [Game(d) for d in GAME_DATABASE]
CATEGORIES = ["Poker", "Casino", "Trick-Taking", "Rummy", "Solitaire", "Party", "Classic", "Family"]


# ==================================================
# 07. LOCAL STORAGE
# ==================================================
class LocalStorage:
    """Penyimpanan lokal sederhana berbasis JSON untuk favorit & recently viewed."""

    def __init__(self, path=STORAGE_FILE):
        self.path = path
        self.data = {"favorites": [], "recently_viewed": []}
        self.load()

    def load(self):
        try:
            if os.path.exists(self.path):
                with open(self.path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        self.data["favorites"] = loaded.get("favorites", []) or []
                        self.data["recently_viewed"] = loaded.get("recently_viewed", []) or []
        except Exception:
            self.data = {"favorites": [], "recently_viewed": []}

    def save(self):
        try:
            parent = os.path.dirname(self.path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            tmp_path = self.path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.path)
        except Exception:
            try:
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

    def get_favorites(self):
        return list(self.data.get("favorites", []))

    def is_favorite(self, game_id):
        return game_id in self.data.get("favorites", [])

    def toggle_favorite(self, game_id):
        favs = self.data.setdefault("favorites", [])
        if game_id in favs:
            favs.remove(game_id)
            result = False
        else:
            favs.append(game_id)
            result = True
        self.save()
        return result

    def get_recently_viewed(self):
        return list(self.data.get("recently_viewed", []))

    def add_recently_viewed(self, game_id):
        recent = self.data.setdefault("recently_viewed", [])
        if game_id in recent:
            recent.remove(game_id)
        recent.insert(0, game_id)
        del recent[10:]
        self.save()


STORAGE = LocalStorage()


# ==================================================
# 08. UTILITY FUNCTIONS
# ==================================================
def duration_bucket(minutes: int) -> str:
    if minutes < 15:
        return "< 15 menit"
    if minutes <= 30:
        return "15-30 menit"
    if minutes <= 60:
        return "30-60 menit"
    return "> 60 menit"


def player_bucket_matches(game: Game, bucket: str) -> bool:
    lo, hi = game.players_min, game.players_max
    if bucket == "1":
        return lo <= 1 <= hi
    if bucket == "2":
        return lo <= 2 <= hi
    if bucket == "3-4":
        return not (hi < 3 or lo > 4)
    if bucket == "5+":
        return hi >= 5
    return True


def filter_games(games, query="", categories=None, player_buckets=None,
                  duration_buckets=None, difficulties=None):
    result = []
    for g in games:
        if query and not g.matches_query(query):
            continue
        if categories and g.category not in categories:
            continue
        if player_buckets and not any(player_bucket_matches(g, b) for b in player_buckets):
            continue
        if duration_buckets and duration_bucket(g.duration_minutes) not in duration_buckets:
            continue
        if difficulties and g.difficulty not in difficulties:
            continue
        result.append(g)
    return result


def safe_get(lst, idx, default=None):
    try:
        return lst[idx]
    except Exception:
        return default


# ==================================================
# 09. REUSABLE UI COMPONENTS
# ==================================================
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


class AppButton(ButtonBehavior, BoxLayout, RoundedBG):
    """Tombol primary dengan background indigo."""

    text = StringProperty("")

    def __init__(self, text="", bg_color=None, text_color=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.padding = (AppSpacing.MD, AppSpacing.SM)
        self.size_hint_y = None
        self.height = dp(48)
        self.init_rounded_bg(color=bg_color or AppColors.PRIMARY, radius=AppRadius.MD)
        self.text = text
        from kivy.uix.label import Label
        self._label = Label(
            text=text, color=text_color or AppColors.WHITE,
            font_size=AppTypography.BODY, bold=True,
            halign="center", valign="middle",
        )
        self._label.bind(size=self._label.setter("text_size"))
        self.add_widget(self._label)

    def on_text(self, instance, value):
        if hasattr(self, "_label"):
            self._label.text = value

    def on_press(self):
        anim = Animation(opacity=0.7, duration=0.06) + Animation(opacity=1, duration=0.1)
        anim.start(self)


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
            elif self.name == "diamond":
                Line(points=[cx, cy+r*1.05, cx+r*.78, cy, cx, cy-r*1.05, cx-r*.78, cy],
                     close=True, width=self.stroke)
            elif self.name == "club":
                lobe_r = r * .42
                Line(circle=(cx, cy+r*.55, lobe_r), width=self.stroke)
                Line(circle=(cx-r*.55, cy-r*.15, lobe_r), width=self.stroke)
                Line(circle=(cx+r*.55, cy-r*.15, lobe_r), width=self.stroke)
                Line(points=[cx, cy-r*.30, cx-r*.18, cy-r*.95, cx+r*.18, cy-r*.95, cx, cy-r*.30],
                     width=self.stroke)
            elif self.name == "spade":
                Line(bezier=(cx, cy+r*.70, cx-r*1.55, cy+r*.02, cx-r*.90, cy-r*.95, cx, cy-r*.28),
                     width=self.stroke)
                Line(bezier=(cx, cy+r*.70, cx+r*1.55, cy+r*.02, cx+r*.90, cy-r*.95, cx, cy-r*.28),
                     width=self.stroke)
                Line(points=[cx-r*.90, cy-r*.25, cx, cy+r*1.00, cx+r*.90, cy-r*.25],
                     width=self.stroke)
                Line(points=[cx, cy-r*.30, cx-r*.20, cy-r*.90, cx+r*.20, cy-r*.90, cx, cy-r*.30],
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
            else:
                Line(circle=(cx, cy, r), width=self.stroke)


class AppIconButton(ButtonBehavior, FloatLayout, RoundedBG):
    """Tombol ikon vektor; tetap menerima icon_text agar kode lama tidak rusak."""

    icon_text = StringProperty("")

    def __init__(self, icon_text="back", bg_color=None, icon_color=None, size_dp=40, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(size_dp), dp(size_dp))
        self.init_rounded_bg(color=bg_color or AppColors.ELEVATED, radius=dp(12))
        mapping = {"<": "back", ">": "chevron_right", "?": "info"}
        self.icon_name = mapping.get(icon_text, icon_text)
        self._icon = VectorIcon(name=self.icon_name, color=icon_color or AppColors.TEXT,
                                size_hint=(.58, .58), pos_hint={"center_x": .5, "center_y": .5})
        self.add_widget(self._icon)

    def on_press(self):
        (Animation(opacity=.55, duration=.05) + Animation(opacity=1, duration=.10)).start(self)


class SectionHeader(BoxLayout):
    """Header untuk tiap section (judul + optional aksi)."""

    def __init__(self, title="", action_text="", on_action=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(32)
        self.padding = (0, 0)
        from kivy.uix.label import Label
        title_label = Label(
            text=title, color=AppColors.TEXT, font_size=AppTypography.SECTION,
            bold=True, halign="left", valign="middle", size_hint_x=1,
        )
        title_label.bind(size=title_label.setter("text_size"))
        self.add_widget(title_label)
        if action_text and on_action:
            from kivy.uix.label import Label as KLabel

            class _ActionLabel(ButtonBehavior, KLabel):
                pass

            act = _ActionLabel(
                text=action_text, color=AppColors.PRIMARY_LIGHT, font_size=AppTypography.CAPTION,
                bold=True, halign="right", valign="middle", size_hint_x=None, width=dp(90),
            )
            act.bind(size=act.setter("text_size"))
            act.bind(on_release=lambda *_: on_action())
            self.add_widget(act)


class EmptyState(BoxLayout):
    """Tampilan saat data kosong (favorit kosong, hasil pencarian kosong, dsb)."""

    def __init__(self, icon="( )", title="Belum ada data", subtitle="", button_text="", on_button=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.padding = (AppSpacing.XL, AppSpacing.XXL)
        self.spacing = AppSpacing.SM
        from kivy.uix.label import Label
        icon_name = {"\u2661": "heart", "\u2665": "heart", "♡": "heart", "♥": "heart"}.get(icon, "cards")
        icon_wrap = BoxLayout(size_hint_y=None, height=dp(58))
        icon_wrap.add_widget(BoxLayout())
        icon_wrap.add_widget(VectorIcon(
            name=icon_name, color=AppColors.PRIMARY_LIGHT,
            size_hint=(None, None), size=(dp(44), dp(44)),
            pos_hint={"center_y": .5}, stroke=2.0
        ))
        icon_wrap.add_widget(BoxLayout())
        self.add_widget(icon_wrap)
        title_label = Label(text=title, color=AppColors.TEXT, font_size=AppTypography.SECTION,
                             bold=True, size_hint_y=None, height=dp(28))
        self.add_widget(title_label)
        if subtitle:
            sub_label = Label(text=subtitle, color=AppColors.TEXT_SECONDARY, font_size=AppTypography.BODY,
                               size_hint_y=None, height=dp(40), halign="center")
            sub_label.bind(width=lambda *a: setattr(sub_label, "text_size", (sub_label.width, None)))
            self.add_widget(sub_label)
        if button_text and on_button:
            btn = AppButton(text=button_text, size_hint=(None, None), size=(dp(200), dp(44)),
                             pos_hint={"center_x": 0.5})
            btn.bind(on_release=lambda *_: on_button())
            holder = BoxLayout(size_hint_y=None, height=dp(56))
            holder.add_widget(BoxLayout())
            holder.add_widget(btn)
            holder.add_widget(BoxLayout())
            self.add_widget(holder)
        self.bind(minimum_height=self.setter("height"))


class DifficultyBadge(BoxLayout, RoundedBG):
    """Badge kecil untuk menampilkan tingkat kesulitan."""

    def __init__(self, difficulty="Mudah", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(70), dp(24))
        color = AppColors.DIFFICULTY.get(difficulty, AppColors.TEXT_MUTED)
        self.init_rounded_bg(color=(color[0], color[1], color[2], 0.18), radius=AppRadius.PILL)
        from kivy.uix.label import Label
        label = Label(text=difficulty, color=color, font_size=AppTypography.META, bold=True)
        self.add_widget(label)


class CategoryChip(ButtonBehavior, BoxLayout, RoundedBG):
    """Chip kategori yang dapat dipilih (toggle)."""

    def __init__(self, text="", selected=False, on_toggle=None, **kwargs):
        super().__init__(**kwargs)
        self.text_value = text
        self.selected = selected
        self.on_toggle = on_toggle
        self.size_hint = (None, None)
        self.height = dp(34)
        self.padding = (AppSpacing.SM, 0)
        self.width = dp(18) + len(text) * dp(8)
        self.init_rounded_bg(
            color=AppColors.PRIMARY if selected else AppColors.ELEVATED,
            radius=AppRadius.PILL,
            border_color=None if selected else AppColors.BORDER,
        )
        from kivy.uix.label import Label
        self._label = Label(
            text=text, color=AppColors.WHITE if selected else AppColors.TEXT_SECONDARY,
            font_size=AppTypography.CAPTION, bold=selected,
        )
        self.add_widget(self._label)

    def set_selected(self, selected):
        self.selected = selected
        self.set_bg_color(AppColors.PRIMARY if selected else AppColors.ELEVATED)
        self._label.color = AppColors.WHITE if selected else AppColors.TEXT_SECONDARY
        self._label.bold = selected

    def on_press(self):
        if self.on_toggle:
            self.on_toggle(self.text_value)


class MetadataItem(BoxLayout):
    """Menampilkan satu metadata singkat (misal jumlah pemain / durasi) dengan label kecil."""

    def __init__(self, label="", value="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(2)
        from kivy.uix.label import Label
        value_label = Label(text=value, color=AppColors.TEXT, font_size=AppTypography.BODY, bold=True)
        label_label = Label(text=label, color=AppColors.TEXT_MUTED, font_size=AppTypography.META)
        self.add_widget(value_label)
        self.add_widget(label_label)


class FavoriteButton(ButtonBehavior, FloatLayout, RoundedBG):
    """Tombol favorit tanpa Unicode; status disimpan ke LocalStorage."""

    def __init__(self, game_id="", on_change=None, size_dp=40, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.on_change = on_change
        self.size_hint = (None, None)
        self.size = (dp(size_dp), dp(size_dp))
        self.init_rounded_bg(
            color=AppColors.ELEVATED,
            radius=dp(size_dp) / 2,
            border_color=AppColors.BORDER_SOFT,
        )
        self._is_fav = STORAGE.is_favorite(game_id)
        self._icon = VectorIcon(
            name="heart",
            color=self._icon_color(),
            size_hint=(None, None),
            size=(dp(size_dp * .52), dp(size_dp * .52)),
            pos_hint={"center_x": .5, "center_y": .5},
            stroke=1.8,
        )
        self.add_widget(self._icon)

    def _icon_color(self):
        return AppColors.ERROR if self._is_fav else AppColors.TEXT_SECONDARY

    def refresh(self):
        self._is_fav = STORAGE.is_favorite(self.game_id)
        self._icon.set_color(self._icon_color())

    def on_press(self):
        self._is_fav = STORAGE.toggle_favorite(self.game_id)
        self._icon.set_color(self._icon_color())
        anim = (
            Animation(size=(dp(self.width * .65), dp(self.height * .65)), duration=.07)
            + Animation(size=(dp(self.width * .52), dp(self.height * .52)), duration=.09)
        )
        anim.start(self._icon)
        if self.on_change:
            self.on_change(self.game_id, self._is_fav)


class AppSearchBar(BoxLayout, RoundedBG):
    """Search bar modern dengan ikon vektor, tinggi nyaman, dan outline lembut."""

    def __init__(self, hint_text="Cari...", on_text=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(52)
        self.padding = (dp(14), 0, dp(12), 0)
        self.spacing = dp(8)
        self.init_rounded_bg(color=AppColors.ELEVATED, radius=dp(16), border_color=AppColors.BORDER_SOFT)

        icon_wrap = BoxLayout(size_hint=(None, 1), width=dp(26))
        icon_wrap.add_widget(VectorIcon(name="search", color=AppColors.TEXT_MUTED,
                                        size_hint=(None, None), size=(dp(19), dp(19)),
                                        pos_hint={"center_x": .5, "center_y": .5}))
        self.add_widget(icon_wrap)

        self.input = TextInput(
            hint_text=hint_text, multiline=False,
            background_color=AppColors.TRANSPARENT,
            foreground_color=AppColors.TEXT,
            cursor_color=AppColors.PRIMARY_LIGHT,
            hint_text_color=AppColors.TEXT_MUTED,
            font_size=AppTypography.BODY,
            padding=(0, dp(15), 0, 0),
            size_hint=(1, 1),
        )
        if on_text:
            self.input.bind(text=lambda instance, value: on_text(value))
        self.add_widget(self.input)


# ==================================================
# 10. GAME COMPONENTS
# ==================================================
class GameListTile(ButtonBehavior, BoxLayout, RoundedBG):
    """Tile modern untuk daftar permainan di beranda."""

    def __init__(self, game: Game, on_press_game=None, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.on_press_game = on_press_game
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(88)
        self.padding = (dp(12), dp(10), dp(10), dp(10))
        self.spacing = dp(12)
        self.init_rounded_bg(color=AppColors.SURFACE, radius=dp(18), border_color=AppColors.BORDER_SOFT)

        class _Avatar(FloatLayout, RoundedBG):
            pass

        av = _Avatar(size_hint=(None, None), size=(dp(56), dp(56)), pos_hint={"center_y": .5})
        av.init_rounded_bg(color=AppColors.ELEVATED, radius=dp(16))
        av.add_widget(VectorIcon(name="cards", color=AppColors.GOLD,
                                 size_hint=(None, None), size=(dp(30), dp(30)),
                                 pos_hint={"center_x": .5, "center_y": .5}))
        self.add_widget(av)

        from kivy.uix.label import Label
        info = BoxLayout(orientation="vertical", spacing=dp(2), size_hint_x=1)
        name_lbl = Label(text=game.name, color=AppColors.TEXT, font_size=sp(14.5), bold=True,
                         halign="left", valign="bottom", size_hint_y=None, height=dp(28))
        name_lbl.bind(size=name_lbl.setter("text_size"))
        info.add_widget(name_lbl)

        meta_lbl = Label(text=f"{game.category}  •  {game.player_label()}",
                         color=AppColors.TEXT_SECONDARY, font_size=sp(11.5),
                         halign="left", valign="middle", size_hint_y=None, height=dp(20))
        meta_lbl.bind(size=meta_lbl.setter("text_size"))
        info.add_widget(meta_lbl)

        time_lbl = Label(text=game.duration, color=AppColors.TEXT_MUTED, font_size=sp(10.5),
                         halign="left", valign="top", size_hint_y=None, height=dp(18))
        time_lbl.bind(size=time_lbl.setter("text_size"))
        info.add_widget(time_lbl)
        self.add_widget(info)

        right = BoxLayout(orientation="horizontal", size_hint=(None, 1), width=dp(116), spacing=dp(7))
        fav = FavoriteButton(game_id=game.id, size_dp=34)
        right.add_widget(fav)
        diff_col = BoxLayout(orientation="vertical", size_hint_x=None, width=dp(70), spacing=dp(4))
        diff_col.add_widget(BoxLayout())
        diff_col.add_widget(DifficultyBadge(difficulty=game.difficulty))
        chev = BoxLayout(size_hint_y=None, height=dp(18))
        chev.add_widget(BoxLayout())
        chev.add_widget(VectorIcon(name="chevron_right", color=AppColors.TEXT_MUTED,
                                   size_hint=(None, None), size=(dp(16), dp(16))))
        diff_col.add_widget(chev)
        right.add_widget(diff_col)
        self.add_widget(right)

    def on_press(self):
        self.set_bg_color(AppColors.ELEVATED)

    def on_release(self):
        self.set_bg_color(AppColors.SURFACE)
        if self.on_press_game:
            self.on_press_game(self.game.id)


class GameCard(ButtonBehavior, BoxLayout, RoundedBG):
    """Card game dengan tombol favorit yang dapat dipakai langsung."""

    def __init__(self, game: Game, on_press_game=None, on_favorite_change=None, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.on_press_game = on_press_game
        self.on_favorite_change = on_favorite_change
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(132)
        self.padding = (AppSpacing.MD, AppSpacing.SM)
        self.spacing = dp(5)
        self.init_rounded_bg(color=AppColors.SURFACE, radius=AppRadius.MD, border_color=AppColors.BORDER)

        top_row = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
        cat_lbl = Label(text=game.category, color=AppColors.GOLD, font_size=AppTypography.META,
                         bold=True, halign="left", valign="middle")
        cat_lbl.bind(size=cat_lbl.setter("text_size"))
        top_row.add_widget(cat_lbl)
        top_row.add_widget(BoxLayout())

        fav = FavoriteButton(
            game_id=game.id, size_dp=30,
            on_change=self._favorite_changed
        )
        top_row.add_widget(fav)

        badge = DifficultyBadge(difficulty=game.difficulty)
        badge_wrap = BoxLayout(size_hint_x=None, width=dp(70))
        badge_wrap.add_widget(badge)
        top_row.add_widget(badge_wrap)
        self.add_widget(top_row)

        name_lbl = Label(text=game.name, color=AppColors.TEXT, font_size=AppTypography.SECTION,
                          bold=True, halign="left", valign="middle", size_hint_y=None, height=dp(24))
        name_lbl.bind(size=name_lbl.setter("text_size"))
        self.add_widget(name_lbl)

        desc_lbl = Label(text=game.description, color=AppColors.TEXT_SECONDARY, font_size=AppTypography.CAPTION,
                          halign="left", valign="top", size_hint_y=None, height=dp(31))
        desc_lbl.bind(size=lambda *a: setattr(desc_lbl, "text_size", (desc_lbl.width, dp(31))))
        self.add_widget(desc_lbl)

        meta_lbl = Label(
            text=f"{game.player_label()}  ·  {game.duration}",
            color=AppColors.TEXT_MUTED, font_size=AppTypography.META,
            halign="left", valign="middle", size_hint_y=None, height=dp(18)
        )
        meta_lbl.bind(size=meta_lbl.setter("text_size"))
        self.add_widget(meta_lbl)

    def _favorite_changed(self, game_id, is_favorite):
        if self.on_favorite_change:
            self.on_favorite_change(game_id, is_favorite)

    def on_release(self):
        if self.on_press_game:
            self.on_press_game(self.game.id)


class FeaturedGameCard(ButtonBehavior, BoxLayout, RoundedBG):
    """Hero card beranda dengan hierarki visual seperti aplikasi modern."""

    def __init__(self, game: Game, on_press_game=None, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.on_press_game = on_press_game
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(168)
        self.padding = (dp(18), dp(18))
        self.spacing = dp(14)
        self.init_rounded_bg(color=AppColors.STRONG, radius=dp(22), border_color=AppColors.BORDER)

        left = BoxLayout(orientation="vertical", spacing=dp(5), size_hint_x=1)
        from kivy.uix.label import Label
        eyebrow = Label(text="REKOMENDASI HARI INI", color=AppColors.PRIMARY_LIGHT,
                        font_size=sp(10.5), bold=True, halign="left", valign="middle",
                        size_hint_y=None, height=dp(18))
        eyebrow.bind(size=eyebrow.setter("text_size"))
        left.add_widget(eyebrow)

        title = Label(text=game.name, color=AppColors.TEXT, font_size=sp(22), bold=True,
                      halign="left", valign="middle", size_hint_y=None, height=dp(34))
        title.bind(size=title.setter("text_size"))
        left.add_widget(title)

        desc = Label(text=game.description, color=AppColors.TEXT_SECONDARY, font_size=sp(11.5),
                     halign="left", valign="top", size_hint_y=None, height=dp(46))
        desc.bind(size=lambda *a: setattr(desc, "text_size", (desc.width, dp(46))))
        left.add_widget(desc)

        meta = Label(text=f"{game.player_label()}  •  {game.duration}  •  {game.difficulty}",
                     color=AppColors.GOLD_LIGHT, font_size=sp(10.5), bold=True,
                     halign="left", valign="middle", size_hint_y=None, height=dp(20))
        meta.bind(size=meta.setter("text_size"))
        left.add_widget(meta)
        self.add_widget(left)

        class _DeckArt(FloatLayout, RoundedBG):
            pass
        art = _DeckArt(size_hint=(None, 1), width=dp(88))
        art.init_rounded_bg(color=AppColors.ELEVATED, radius=dp(18))
        art.add_widget(VectorIcon(name="cards", color=AppColors.GOLD,
                                  size_hint=(None, None), size=(dp(54), dp(54)),
                                  pos_hint={"center_x": .5, "center_y": .55}))
        art.add_widget(Label(text=game.category.upper(), color=AppColors.TEXT_MUTED, font_size=sp(8.5), bold=True,
                             size_hint=(1, None), height=dp(20), pos_hint={"x":0,"y":.05}))
        self.add_widget(art)

    def on_release(self):
        if self.on_press_game:
            self.on_press_game(self.game.id)


class QuickGuideStep(BoxLayout):
    """Satu langkah dalam Quick Guide dengan nomor."""

    def __init__(self, number, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(40)
        self.spacing = AppSpacing.SM
        from kivy.uix.label import Label

        class _NumBadge(BoxLayout, RoundedBG):
            pass

        badge = _NumBadge(size_hint=(None, None), size=(dp(26), dp(26)))
        badge.init_rounded_bg(color=AppColors.PRIMARY, radius=dp(13))
        badge.add_widget(Label(text=str(number), color=AppColors.WHITE, font_size=AppTypography.CAPTION, bold=True))
        badge_wrap = BoxLayout(size_hint=(None, 1), width=dp(26))
        badge_wrap.add_widget(badge)
        self.add_widget(badge_wrap)

        text_lbl = Label(text=text, color=AppColors.TEXT, font_size=AppTypography.BODY,
                          halign="left", valign="middle")
        text_lbl.bind(width=lambda *a: setattr(text_lbl, "text_size", (text_lbl.width, None)))
        text_lbl.bind(texture_size=lambda *a: setattr(self, "height", max(dp(40), text_lbl.texture_size[1] + dp(10))))
        self.add_widget(text_lbl)


class SpecialCardTile(BoxLayout, RoundedBG):
    """Menampilkan satu kartu spesial dengan penjelasannya."""

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.padding = (AppSpacing.SM, AppSpacing.XS)
        self.spacing = AppSpacing.XS
        self.init_rounded_bg(color=AppColors.SURFACE, radius=AppRadius.SM, border_color=AppColors.BORDER)
        from kivy.uix.label import Label
        # Tentukan ikon suit sesuai kata di awal teks (mis. "Club:", "Heart:"),
        # digambar dengan VectorIcon (bukan karakter Unicode) agar tidak
        # tampil sebagai kotak kosong pada Windows/Android.
        suit_word = text.split(":", 1)[0].strip().lower()
        suit_map = {
            "club": "club", "clubs": "club", "keriting": "club",
            "diamond": "diamond", "diamonds": "diamond", "wajik": "diamond",
            "heart": "heart", "hearts": "heart", "hati": "heart",
            "spade": "spade", "spades": "spade", "sekop": "spade",
        }
        icon_name = suit_map.get(suit_word, "diamond")
        mark_wrap = BoxLayout(size_hint=(None, None), size=(dp(20), dp(20)))
        mark_wrap.add_widget(VectorIcon(name=icon_name, color=AppColors.GOLD, stroke=1.4))
        self.add_widget(mark_wrap)
        lbl = Label(text=text, color=AppColors.TEXT_SECONDARY, font_size=AppTypography.CAPTION,
                    halign="left", valign="middle")
        lbl.bind(width=lambda *a: setattr(lbl, "text_size", (lbl.width, None)))
        lbl.bind(texture_size=lambda *a: setattr(self, "height", max(dp(34), lbl.texture_size[1] + dp(16))))
        self.add_widget(lbl)


class RankingCard(BoxLayout, RoundedBG):
    """Menampilkan urutan ranking / kombinasi kartu."""

    def __init__(self, index, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(34)
        self.padding = (AppSpacing.SM, 0)
        self.spacing = AppSpacing.XS
        self.init_rounded_bg(color=AppColors.STRONG, radius=AppRadius.SM)
        from kivy.uix.label import Label
        num_lbl = Label(text=f"#{index}", color=AppColors.GOLD, font_size=AppTypography.CAPTION, bold=True,
                         size_hint=(None, 1), width=dp(30))
        self.add_widget(num_lbl)
        text_lbl = Label(text=text, color=AppColors.TEXT, font_size=AppTypography.CAPTION,
                          halign="left", valign="middle")
        text_lbl.bind(size=text_lbl.setter("text_size"))
        self.add_widget(text_lbl)


class GameRecommendationCard(ButtonBehavior, BoxLayout, RoundedBG):
    """Hasil rekomendasi dari Game Finder."""

    def __init__(self, game: Game, reason="", on_press_game=None, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.on_press_game = on_press_game
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(128)
        self.padding = (AppSpacing.MD, AppSpacing.SM)
        self.spacing = dp(4)
        self.init_rounded_bg(color=AppColors.ELEVATED, radius=AppRadius.MD, border_color=AppColors.BORDER)
        from kivy.uix.label import Label

        top = BoxLayout(size_hint_y=None, height=dp(24))
        name_lbl = Label(text=game.name, color=AppColors.TEXT, font_size=AppTypography.SECTION, bold=True,
                          halign="left", valign="middle")
        name_lbl.bind(size=name_lbl.setter("text_size"))
        top.add_widget(name_lbl)
        badge_wrap = BoxLayout(size_hint_x=None, width=dp(70))
        badge_wrap.add_widget(DifficultyBadge(difficulty=game.difficulty))
        top.add_widget(badge_wrap)
        self.add_widget(top)

        reason_lbl = Label(text=reason, color=AppColors.GOLD_LIGHT, font_size=AppTypography.CAPTION,
                            halign="left", valign="top", size_hint_y=None, height=dp(32))
        reason_lbl.bind(size=lambda *a: setattr(reason_lbl, "text_size", (reason_lbl.width, dp(32))))
        self.add_widget(reason_lbl)

        meta_lbl = Label(
            text=f"{game.category}  \u00b7  {game.player_label()}  \u00b7  {game.duration}",
            color=AppColors.TEXT_MUTED, font_size=AppTypography.META, halign="left", valign="middle",
            size_hint_y=None, height=dp(20),
        )
        meta_lbl.bind(size=meta_lbl.setter("text_size"))
        self.add_widget(meta_lbl)

    def on_release(self):
        if self.on_press_game:
            self.on_press_game(self.game.id)


class GameFinderStep(BoxLayout):
    """Satu pertanyaan Game Finder dengan pilihan yang mudah dipahami."""

    def __init__(self, title, options, on_select=None, selected=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(8)
        self.size_hint_y = None
        self.selected = selected
        self.on_select = on_select
        self._chips = []

        title_lbl = Label(text=title, color=AppColors.TEXT, font_size=AppTypography.BODY, bold=True,
                           halign="left", valign="middle", size_hint_y=None, height=dp(24))
        title_lbl.bind(size=title_lbl.setter("text_size"))
        self.add_widget(title_lbl)

        chip_row = GridLayout(cols=2, size_hint_y=None, spacing=dp(8), row_default_height=dp(42),
                               row_force_default=True)
        chip_row.bind(minimum_height=chip_row.setter("height"))
        for opt in options:
            chip = self._make_chip(opt)
            self._chips.append(chip)
            chip_row.add_widget(chip)
        self.add_widget(chip_row)
        self.height = dp(24) + dp(8) + chip_row.height + dp(8)
        chip_row.bind(height=lambda *a: setattr(self, "height", dp(24) + dp(8) + chip_row.height + dp(8)))

    def _make_chip(self, opt):
        class _OptChip(ButtonBehavior, BoxLayout, RoundedBG):
            pass

        selected = opt == self.selected
        chip = _OptChip(size_hint_y=None, height=dp(42))
        chip.init_rounded_bg(
            color=(AppColors.PRIMARY[0], AppColors.PRIMARY[1], AppColors.PRIMARY[2], .22) if selected else AppColors.SURFACE,
            radius=dp(13), border_color=AppColors.PRIMARY_LIGHT if selected else AppColors.BORDER
        )
        lbl = Label(text=opt, color=AppColors.WHITE if selected else AppColors.TEXT_SECONDARY,
                    font_size=sp(11.5), bold=selected, halign="center", valign="middle")
        lbl.bind(size=lbl.setter("text_size"))
        chip.add_widget(lbl)
        chip._label = lbl
        chip._value = opt

        def select(*_):
            self.selected = opt
            for c in self._chips:
                is_sel = c._value == opt
                c.set_bg_color((AppColors.PRIMARY[0], AppColors.PRIMARY[1], AppColors.PRIMARY[2], .22)
                               if is_sel else AppColors.SURFACE)
                c._label.color = AppColors.WHITE if is_sel else AppColors.TEXT_SECONDARY
                c._label.bold = is_sel
            if self.on_select:
                self.on_select(opt)

        chip.bind(on_release=select)
        return chip




class FilterSheet(ModalView):
    """Bottom sheet untuk filter: jumlah pemain, durasi, difficulty, kategori."""

    PLAYER_OPTIONS = ["1", "2", "3-4", "5+"]
    DURATION_OPTIONS = ["< 15 menit", "15-30 menit", "30-60 menit", "> 60 menit"]
    DIFFICULTY_OPTIONS = ["Mudah", "Sedang", "Sulit"]

    def __init__(self, current_filters, on_apply=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = Window.height * 0.82
        self.pos_hint = {"bottom": 1}
        self.background_color = (0, 0, 0, 0.5)
        self.on_apply = on_apply
        self.selected = {
            "players": set(current_filters.get("players", set())),
            "duration": set(current_filters.get("duration", set())),
            "difficulty": set(current_filters.get("difficulty", set())),
            "category": set(current_filters.get("category", set())),
        }
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label

        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.SURFACE)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[AppRadius.XL, AppRadius.XL, 0, 0])
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos))
        root.bind(size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(size_hint_y=None, height=dp(52), padding=(AppSpacing.LG, 0))
        title = Label(text="Filter", color=AppColors.TEXT, font_size=AppTypography.SECTION, bold=True,
                      halign="left", valign="middle")
        title.bind(size=title.setter("text_size"))
        header.add_widget(title)
        close_btn = AppIconButton(icon_text="X", size_dp=32)
        close_btn.bind(on_release=lambda *_: self.dismiss())
        close_wrap = BoxLayout(size_hint_x=None, width=dp(32))
        close_wrap.add_widget(close_btn)
        header.add_widget(close_wrap)
        root.add_widget(header)

        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation="vertical", size_hint_y=None, padding=(AppSpacing.LG, AppSpacing.SM),
                             spacing=AppSpacing.LG)
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(self._section("Jumlah Pemain", self.PLAYER_OPTIONS, "players"))
        content.add_widget(self._section("Durasi", self.DURATION_OPTIONS, "duration"))
        content.add_widget(self._section("Difficulty", self.DIFFICULTY_OPTIONS, "difficulty"))
        content.add_widget(self._section("Kategori", CATEGORIES, "category"))

        scroll.add_widget(content)
        root.add_widget(scroll)

        footer = BoxLayout(size_hint_y=None, height=dp(76), padding=(AppSpacing.LG, AppSpacing.SM), spacing=AppSpacing.SM)
        reset_btn = AppButton(text="Reset", bg_color=AppColors.ELEVATED, text_color=AppColors.TEXT)
        reset_btn.bind(on_release=lambda *_: self._reset())
        apply_btn = AppButton(text="Terapkan Filter")
        apply_btn.bind(on_release=lambda *_: self._apply())
        footer.add_widget(reset_btn)
        footer.add_widget(apply_btn)
        root.add_widget(footer)

        self.add_widget(root)

    def _section(self, title, options, key):
        from kivy.uix.label import Label
        wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
        title_lbl = Label(text=title, color=AppColors.TEXT, font_size=AppTypography.BODY, bold=True,
                           halign="left", valign="middle", size_hint_y=None, height=dp(22))
        title_lbl.bind(size=title_lbl.setter("text_size"))
        wrap.add_widget(title_lbl)

        rows = (len(options) + 1) // 2
        grid = GridLayout(cols=2, size_hint_y=None, height=rows * dp(42), spacing=dp(8))
        for opt in options:
            chip = CategoryChip(text=opt, selected=opt in self.selected[key],
                                 on_toggle=lambda val, k=key: self._toggle(k, val))
            chip.size_hint = (1, None)
            chip.height = dp(38)
            grid.add_widget(chip)
        wrap.add_widget(grid)
        wrap.height = dp(22) + AppSpacing.XS + grid.height
        return wrap

    def _toggle(self, key, value):
        s = self.selected[key]
        if value in s:
            s.remove(value)
        else:
            s.add(value)

    def _reset(self):
        for k in self.selected:
            self.selected[k] = set()
        self.dismiss()
        if self.on_apply:
            self.on_apply(self.selected)

    def _apply(self):
        if self.on_apply:
            self.on_apply(self.selected)
        self.dismiss()


# ==================================================
# 11. NAVIGATION
# ==================================================
class BottomNavigation(BoxLayout, RoundedBG):
    """Bottom navigation modern dengan indikator aktif berbentuk pill."""

    ITEMS = [
        ("home", "Beranda", "home"),
        ("explore", "Jelajah", "explore"),
        ("favorite", "Favorit", "heart"),
        ("about", "Tentang", "info"),
    ]

    def __init__(self, on_navigate=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(76)
        self.padding = (dp(10), dp(8), dp(10), dp(8))
        self.spacing = dp(4)
        self.on_navigate = on_navigate
        self.active = "home"
        self.init_rounded_bg(color=AppColors.SURFACE, radius=0, border_color=None)
        self._buttons = {}
        for key, label, icon in self.ITEMS:
            btn = self._make_button(key, label, icon)
            self._buttons[key] = btn
            self.add_widget(btn)
        with self.canvas.before:
            Color(*AppColors.BORDER_SOFT)
            self._top_line = Line(points=[self.x, self.top, self.right, self.top], width=1)
        self.bind(pos=self._update_line, size=self._update_line)

    def _update_line(self, *args):
        self._top_line.points = [self.x, self.top, self.right, self.top]

    def _make_button(self, key, label, icon):
        class _NavBtn(ButtonBehavior, BoxLayout, RoundedBG):
            pass

        active = key == self.active
        btn = _NavBtn(orientation="vertical", padding=(dp(8), dp(5)), spacing=dp(2))
        btn.init_rounded_bg(color=(AppColors.PRIMARY[0], AppColors.PRIMARY[1], AppColors.PRIMARY[2], .14)
                           if active else AppColors.TRANSPARENT, radius=dp(15))
        icon_lbl = VectorIcon(name=icon,
                              color=AppColors.PRIMARY_LIGHT if active else AppColors.TEXT_MUTED,
                              size_hint=(1, .58))
        from kivy.uix.label import Label
        text_lbl = Label(text=label, font_size=sp(10.5),
                         color=AppColors.PRIMARY_LIGHT if active else AppColors.TEXT_MUTED,
                         bold=active, size_hint_y=.42)
        btn.add_widget(icon_lbl)
        btn.add_widget(text_lbl)
        btn._icon_lbl = icon_lbl
        btn._text_lbl = text_lbl
        btn.bind(on_release=lambda *_: self._select(key))
        return btn

    def _select(self, key):
        self.set_active(key)
        if self.on_navigate:
            self.on_navigate(key)

    def set_active(self, key):
        self.active = key
        for k, btn in self._buttons.items():
            active = k == key
            btn.set_bg_color((AppColors.PRIMARY[0], AppColors.PRIMARY[1], AppColors.PRIMARY[2], .14)
                             if active else AppColors.TRANSPARENT)
            btn._icon_lbl.set_color(AppColors.PRIMARY_LIGHT if active else AppColors.TEXT_MUTED)
            btn._text_lbl.color = AppColors.PRIMARY_LIGHT if active else AppColors.TEXT_MUTED
            btn._text_lbl.bold = active


# ==================================================
# 12. SPLASH SCREEN
# ==================================================
class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = FloatLayout()
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg_rect = RoundedRectangle(pos=root.pos, size=root.size, radius=[0])
        root.bind(pos=lambda *a: setattr(self._bg_rect, "pos", root.pos))
        root.bind(size=lambda *a: setattr(self._bg_rect, "size", root.size))

        from kivy.uix.label import Label
        wrap = BoxLayout(orientation="vertical", size_hint=(None, None), size=(dp(280), dp(120)),
                          pos_hint={"center_x": 0.5, "center_y": 0.5}, spacing=AppSpacing.XS)
        title = Label(text=APP_NAME, color=AppColors.TEXT, font_size=AppTypography.HERO, bold=True)
        subtitle = Label(text=APP_TAGLINE, color=AppColors.TEXT_SECONDARY, font_size=AppTypography.CAPTION,
                          halign="center")
        subtitle.bind(width=lambda *a: setattr(subtitle, "text_size", (subtitle.width, None)))
        wrap.add_widget(title)
        wrap.add_widget(subtitle)
        self._title = title
        self._wrap = wrap
        root.add_widget(wrap)
        self.add_widget(root)

    def on_enter(self):
        self._wrap.opacity = 0
        self._wrap.size = (dp(230), dp(120))
        anim = Animation(opacity=1, duration=0.5) & Animation(size=(dp(280), dp(120)), duration=0.5)
        anim.start(self._wrap)
        Clock.schedule_once(self._go_home, 1.3)

    def _go_home(self, *args):
        app = App.get_running_app()
        app.show_main_shell()


# ==================================================
# 13. BERANDA
# ==================================================
class FinderPromoCard(ButtonBehavior, BoxLayout, RoundedBG):
    """Kartu ajakan Game Finder untuk membantu pengguna memilih game."""

    def __init__(self, on_press_finder=None, **kwargs):
        super().__init__(**kwargs)
        self.on_press_finder = on_press_finder
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(116)
        self.padding = (dp(16), dp(14))
        self.spacing = dp(12)
        self.init_rounded_bg(color=AppColors.STRONG, radius=dp(20), border_color=AppColors.BORDER)

        class _FinderArt(FloatLayout, RoundedBG):
            pass

        art = _FinderArt(size_hint=(None, 1), width=dp(68))
        art.init_rounded_bg(color=AppColors.PRIMARY_DARK, radius=dp(17))
        art.add_widget(VectorIcon(name="cards", color=AppColors.GOLD_LIGHT,
                                  size_hint=(None, None), size=(dp(38), dp(38)),
                                  pos_hint={"center_x": .5, "center_y": .56}))
        art.add_widget(Label(text="FINDER", color=AppColors.TEXT_MUTED, font_size=sp(7.5),
                             bold=True, size_hint=(1, None), height=dp(16),
                             pos_hint={"x": 0, "y": .06}))
        self.add_widget(art)

        info = BoxLayout(orientation="vertical", spacing=dp(3), size_hint_x=1)
        title = Label(text="Bingung mau main apa?", color=AppColors.TEXT,
                      font_size=sp(15.5), bold=True, halign="left", valign="middle",
                      size_hint_y=None, height=dp(25))
        title.bind(size=title.setter("text_size"))
        info.add_widget(title)

        desc = Label(text="Jawab beberapa pertanyaan dan KartuPedia akan memilihkan game yang paling cocok.",
                     color=AppColors.TEXT_SECONDARY, font_size=sp(10.5),
                     halign="left", valign="top", size_hint_y=None, height=dp(40))
        desc.bind(width=lambda *a: setattr(desc, "text_size", (desc.width, None)))
        info.add_widget(desc)

        cta = Label(text="Mulai Game Finder  ›", color=AppColors.GOLD_LIGHT,
                    font_size=sp(10.5), bold=True, halign="left", valign="middle",
                    size_hint_y=None, height=dp(20))
        cta.bind(size=cta.setter("text_size"))
        info.add_widget(cta)
        self.add_widget(info)

    def on_release(self):
        if self.on_press_finder:
            self.on_press_finder()


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos),
                  size=lambda *a: setattr(self._bg, "size", root.size))

        # App bar lebih modern: logo kecil + nama aplikasi + badge offline
        header = BoxLayout(size_hint_y=None, height=dp(78), padding=(dp(20), dp(14), dp(20), dp(8)), spacing=dp(10))
        logo = FloatLayout(size_hint=(None, None), size=(dp(42), dp(42)), pos_hint={"center_y": .5})
        with logo.canvas.before:
            Color(*AppColors.PRIMARY)
            logo._bg = RoundedRectangle(pos=logo.pos, size=logo.size, radius=[dp(13)])
        logo.bind(pos=lambda *a: setattr(logo._bg, "pos", logo.pos), size=lambda *a: setattr(logo._bg, "size", logo.size))
        logo.add_widget(VectorIcon(name="cards", color=AppColors.WHITE, size_hint=(.68,.68),
                                   pos_hint={"center_x":.5,"center_y":.5}))
        header.add_widget(logo)

        title_wrap = BoxLayout(orientation="vertical", spacing=0)
        title = Label(text=APP_NAME, color=AppColors.TEXT, font_size=sp(20), bold=True,
                      halign="left", valign="bottom", size_hint_y=.58)
        title.bind(size=title.setter("text_size"))
        subtitle = Label(text="Ensiklopedia permainan kartu", color=AppColors.TEXT_MUTED, font_size=sp(10.5),
                         halign="left", valign="top", size_hint_y=.42)
        subtitle.bind(size=subtitle.setter("text_size"))
        title_wrap.add_widget(title); title_wrap.add_widget(subtitle)
        header.add_widget(title_wrap)

        class _OfflineBadge(BoxLayout, RoundedBG):
            pass
        badge = _OfflineBadge(size_hint=(None,None), size=(dp(64),dp(26)), pos_hint={"center_y":.5}, padding=(dp(8),0))
        badge.init_rounded_bg(color=(AppColors.SUCCESS[0],AppColors.SUCCESS[1],AppColors.SUCCESS[2],.12), radius=dp(13))
        badge.add_widget(Label(text="OFFLINE", color=AppColors.SUCCESS, font_size=sp(8.5), bold=True))
        header.add_widget(badge)
        root.add_widget(header)

        self.scroll = ScrollView(size_hint=(1, 1), bar_width=0)
        self.content = BoxLayout(orientation="vertical", size_hint_y=None,
                                 padding=(dp(20), dp(6), dp(20), dp(34)), spacing=dp(18))
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        self.content.clear_widgets()
        app = App.get_running_app()

        search = AppSearchBar(hint_text="Cari nama permainan, kategori, atau tag...", on_text=self._on_search_text)
        self.content.add_widget(search)

        self.content.add_widget(FinderPromoCard(on_press_finder=app.open_finder))

        featured = random.choice(GAME_OBJECTS) if GAME_OBJECTS else None
        if featured:
            self.content.add_widget(FeaturedGameCard(featured, on_press_game=app.open_game_detail))

        self.content.add_widget(SectionHeader(title="Kategori"))
        cat_scroll = ScrollView(size_hint=(1, None), height=dp(42), do_scroll_y=False, do_scroll_x=True, bar_width=0)
        cat_row = BoxLayout(size_hint=(None, 1), spacing=dp(8))
        cat_row.bind(minimum_width=cat_row.setter("width"))
        for cat in CATEGORIES:
            cat_row.add_widget(CategoryChip(text=cat, selected=False, on_toggle=self._go_category))
        cat_scroll.add_widget(cat_row)
        self.content.add_widget(cat_scroll)

        self.content.add_widget(SectionHeader(title="Populer", action_text="Lihat Semua", on_action=self._go_explore))
        pop_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
        pop_wrap.bind(minimum_height=pop_wrap.setter("height"))
        for g in GAME_OBJECTS[:6]:
            pop_wrap.add_widget(GameListTile(g, on_press_game=app.open_game_detail))
        self.content.add_widget(pop_wrap)

        self.content.add_widget(SectionHeader(title="Baru Dilihat"))
        recent_ids = STORAGE.get_recently_viewed()
        if recent_ids:
            recent_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
            recent_wrap.bind(minimum_height=recent_wrap.setter("height"))
            for gid in recent_ids[:5]:
                g = get_game_by_id(gid)
                if g:
                    recent_wrap.add_widget(GameListTile(g, on_press_game=app.open_game_detail))
            self.content.add_widget(recent_wrap)
        else:
            empty = EmptyState(icon="", title="Belum ada riwayat",
                               subtitle="Permainan yang dibuka akan tersimpan di bagian ini.")
            self.content.add_widget(empty)

    def _on_search_text(self, value):
        app = App.get_running_app()
        app.pending_search_query = value
        if value:
            app.go_to_search(value)

    def _go_category(self, category):
        App.get_running_app().go_to_explore(category=category)

    def _go_explore(self):
        App.get_running_app().go_to_explore()


# ==================================================
# 14. JELAJAH
# ==================================================
class ExploreScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.query = ""
        self.selected_category = None
        self.filters = {"players": set(), "duration": set(), "difficulty": set(), "category": set()}
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos), size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(64),
                            padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, 0), spacing=AppSpacing.XS)
        title = Label(text="Jelajah", color=AppColors.TEXT, font_size=AppTypography.HEADING, bold=True,
                      halign="left", valign="middle", size_hint_y=None, height=dp(30))
        title.bind(size=title.setter("text_size"))
        header.add_widget(title)
        root.add_widget(header)

        search_row = BoxLayout(size_hint_y=None, height=dp(46), padding=(AppSpacing.LG, 0), spacing=AppSpacing.XS)
        self.search_bar = AppSearchBar(hint_text="Cari permainan kartu...", on_text=self._on_search)
        search_row.add_widget(self.search_bar)
        filter_btn = AppIconButton(icon_text="\u2261", size_dp=46)
        filter_btn.bind(on_release=lambda *_: self._open_filter())
        filter_wrap = BoxLayout(size_hint=(None, 1), width=dp(46))
        filter_wrap.add_widget(filter_btn)
        search_row.add_widget(filter_wrap)
        root.add_widget(search_row)

        chip_scroll = ScrollView(size_hint=(1, None), height=dp(48), do_scroll_y=False, do_scroll_x=True, bar_width=0)
        self.chip_row = BoxLayout(size_hint=(None, 1), spacing=AppSpacing.XS,
                                   padding=(AppSpacing.LG, AppSpacing.XS, AppSpacing.LG, AppSpacing.XS))
        self.chip_row.bind(minimum_width=self.chip_row.setter("width"))
        chip_scroll.add_widget(self.chip_row)
        root.add_widget(chip_scroll)

        self.result_label = Label(text="", color=AppColors.TEXT_MUTED, font_size=AppTypography.CAPTION,
                                   halign="left", valign="middle", size_hint_y=None, height=dp(24),
                                   padding=(AppSpacing.LG, 0))
        self.result_label.bind(size=self.result_label.setter("text_size"))
        root.add_widget(self.result_label)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.list_wrap = BoxLayout(orientation="vertical", size_hint_y=None,
                                    padding=(AppSpacing.LG, AppSpacing.XS, AppSpacing.LG, AppSpacing.XXL),
                                    spacing=AppSpacing.SM)
        self.list_wrap.bind(minimum_height=self.list_wrap.setter("height"))
        self.scroll.add_widget(self.list_wrap)
        root.add_widget(self.scroll)
        self.add_widget(root)
        self._build_chips()

    def _build_chips(self):
        self.chip_row.clear_widgets()
        self._chips = {}
        for cat in CATEGORIES:
            chip = CategoryChip(text=cat, selected=(cat == self.selected_category), on_toggle=self._toggle_category)
            self._chips[cat] = chip
            self.chip_row.add_widget(chip)

    def _toggle_category(self, category):
        if self.selected_category == category:
            self.selected_category = None
        else:
            self.selected_category = category
        for cat, chip in self._chips.items():
            chip.set_selected(cat == self.selected_category)
        self.refresh()

    def _on_search(self, value):
        self.query = value
        self.refresh()

    def _open_filter(self):
        sheet = FilterSheet(self.filters, on_apply=self._apply_filters)
        sheet.open()

    def _apply_filters(self, selected):
        self.filters = selected
        self.refresh()

    def set_query(self, query):
        self.query = query
        self.search_bar.input.text = query
        self.refresh()

    def set_category(self, category):
        self.selected_category = category
        for cat, chip in self._chips.items():
            chip.set_selected(cat == self.selected_category)
        self.refresh()

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        app = App.get_running_app()
        categories = set(self.filters.get("category", set()))
        if self.selected_category:
            categories.add(self.selected_category)
        results = filter_games(
            GAME_OBJECTS, query=self.query,
            categories=categories or None,
            player_buckets=self.filters.get("players") or None,
            duration_buckets=self.filters.get("duration") or None,
            difficulties=self.filters.get("difficulty") or None,
        )
        self.result_label.text = f"{len(results)} permainan ditemukan"
        self.list_wrap.clear_widgets()
        if not results:
            self.list_wrap.add_widget(EmptyState(
                icon="\u2205", title="Tidak ada hasil",
                subtitle="Coba ubah kata kunci atau filter pencarian.",
            ))
            return
        for g in results:
            self.list_wrap.add_widget(GameCard(g, on_press_game=app.open_game_detail))


# ==================================================
# 15. SEARCH
# ==================================================
# Search terintegrasi pada ExploreScreen (AppSearchBar + filter_games()).
# HomeScreen mengarahkan pencarian ke ExploreScreen via app.go_to_search().

# ==================================================
# 16. FILTER
# ==================================================
# Filter (jumlah pemain, durasi, difficulty, kategori) ditangani oleh FilterSheet
# dan diterapkan melalui ExploreScreen.filters + filter_games().


# ==================================================
# 17. GAME FINDER
# ==================================================
class GameFinderScreen(Screen):
    """Rekomendasi game berbasis jawaban pengguna, tanpa AI/internet."""

    PLAYER_OPTIONS = ["1 pemain", "2 pemain", "3-4 pemain", "5+ pemain"]
    TIME_OPTIONS = ["< 15 menit", "15-30 menit", "30-60 menit", "> 60 menit"]
    STYLE_OPTIONS = ["Santai", "Strategis", "Cepat"]
    DIFFICULTY_OPTIONS = ["Mudah", "Sedang", "Sulit"]
    MODE_OPTIONS = ["Sendiri", "Kompetitif", "Kerja sama", "Bebas"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answers = {}
        self._build_ui()

    def _build_ui(self):
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos),
                  size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(size_hint_y=None, height=dp(66),
                           padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, 0), spacing=dp(10))
        back_btn = AppIconButton(icon_text="<", size_dp=36)
        back_btn.bind(on_release=lambda *_: App.get_running_app().go_back())
        header.add_widget(back_btn)

        title_wrap = BoxLayout(orientation="vertical", spacing=0)
        title = Label(text="Game Finder", color=AppColors.TEXT, font_size=AppTypography.HEADING,
                      bold=True, halign="left", valign="bottom", size_hint_y=.6)
        title.bind(size=title.setter("text_size"))
        subtitle = Label(text="Cari game berdasarkan kebutuhanmu", color=AppColors.TEXT_MUTED,
                         font_size=sp(9.5), halign="left", valign="top", size_hint_y=.4)
        subtitle.bind(size=subtitle.setter("text_size"))
        title_wrap.add_widget(title)
        title_wrap.add_widget(subtitle)
        header.add_widget(title_wrap)
        root.add_widget(header)

        self.scroll = ScrollView(size_hint=(1, 1), bar_width=0)
        self.content = BoxLayout(orientation="vertical", size_hint_y=None,
                                 padding=(AppSpacing.LG, AppSpacing.SM, AppSpacing.LG, AppSpacing.XXL),
                                 spacing=dp(10))
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)
        self.add_widget(root)
        self._build_form()

    def _build_form(self):
        self.content.clear_widgets()
        self.answers = {}

        class _FinderIntro(FloatLayout, RoundedBG):
            pass

        intro = _FinderIntro(size_hint_y=None, height=dp(92))
        intro.init_rounded_bg(color=AppColors.STRONG, radius=dp(18), border_color=AppColors.BORDER)
        intro.add_widget(VectorIcon(name="cards", color=AppColors.GOLD_LIGHT,
                                    size_hint=(None, None), size=(dp(38), dp(38)),
                                    pos_hint={"x": .06, "center_y": .58}))
        title = Label(text="Temukan permainan yang cocok", color=AppColors.TEXT, font_size=sp(14),
                      bold=True, halign="left", valign="middle", size_hint=(.78, None),
                      height=dp(25), pos_hint={"x": .23, "top": .83})
        title.bind(size=title.setter("text_size"))
        intro.add_widget(title)
        desc = Label(text="Pilih satu jawaban pada setiap pertanyaan. Hasil akan diurutkan berdasarkan kecocokan.",
                     color=AppColors.TEXT_SECONDARY, font_size=sp(10), halign="left", valign="top",
                     size_hint=(.72, None), height=dp(34), pos_hint={"x": .23, "top": .50})
        desc.bind(width=lambda *a: setattr(desc, "text_size", (desc.width, None)))
        intro.add_widget(desc)
        self.content.add_widget(intro)

        questions = [
            ("1. Berapa orang yang akan bermain?", self.PLAYER_OPTIONS, "players"),
            ("2. Berapa banyak waktu yang tersedia?", self.TIME_OPTIONS, "duration"),
            ("3. Gaya bermain yang diinginkan?", self.STYLE_OPTIONS, "style"),
            ("4. Seberapa sulit game yang diinginkan?", self.DIFFICULTY_OPTIONS, "difficulty"),
            ("5. Mode permainan yang dicari?", self.MODE_OPTIONS, "mode"),
        ]
        for title, options, key in questions:
            self.content.add_widget(GameFinderStep(
                title, options,
                on_select=lambda value, k=key: self.answers.__setitem__(k, value),
            ))

        find_btn = AppButton(text="Temukan Rekomendasi", size_hint_y=None, height=dp(52))
        find_btn.bind(on_release=lambda *_: self._find())
        self.content.add_widget(find_btn)

        reset_btn = AppButton(text="Ulangi Jawaban", bg_color=AppColors.ELEVATED, text_color=AppColors.TEXT,
                              size_hint_y=None, height=dp(44))
        reset_btn.bind(on_release=lambda *_: self._build_form())
        self.content.add_widget(reset_btn)

        self.results_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10))
        self.results_wrap.bind(minimum_height=self.results_wrap.setter("height"))
        self.content.add_widget(self.results_wrap)

    def _bucket_to_game_value(self, answer):
        return {
            "1 pemain": "1",
            "2 pemain": "2",
            "3-4 pemain": "3-4",
            "5+ pemain": "5+",
        }.get(answer)

    def _score_game(self, game: Game):
        # Game casino/betting tidak dimasukkan ke hasil rekomendasi untuk penggunaan aplikasi yang aman.
        if game.category == "Casino" or "betting" in game.tags:
            return -999, []

        score = 0
        reasons = []

        players = self._bucket_to_game_value(self.answers.get("players"))
        if players and player_bucket_matches(game, players):
            score += 4
            reasons.append(f"cocok untuk {game.player_label()}")

        duration = self.answers.get("duration")
        if duration and duration_bucket(game.duration_minutes) == duration:
            score += 3
            reasons.append(f"durasi {game.duration}")

        style = self.answers.get("style")
        if style and game.style == style:
            score += 3
            reasons.append(f"gaya {game.style.lower()}")

        difficulty = self.answers.get("difficulty")
        if difficulty and game.difficulty == difficulty:
            score += 2
            reasons.append(f"level {game.difficulty.lower()}")

        mode = self.answers.get("mode")
        if mode == "Sendiri" and game.players_min == 1:
            score += 4
            reasons.append("bisa dimainkan sendiri")
        elif mode == "Kerja sama" and any(t in game.tags for t in ("kooperatif", "tim")):
            score += 4
            reasons.append("memiliki unsur kerja sama/tim")
        elif mode == "Kompetitif" and game.players_max >= 2 and not any(t in game.tags for t in ("kooperatif", "tim")):
            score += 2
            reasons.append("cocok untuk bermain kompetitif")
        elif mode == "Bebas":
            score += 1

        return score, reasons

    def _find(self):
        if not self.answers:
            self.results_wrap.clear_widgets()
            self.results_wrap.add_widget(SectionHeader(title="Pilih jawaban terlebih dahulu"))
            return

        app = App.get_running_app()
        scored = []
        for game in GAME_OBJECTS:
            score, reasons = self._score_game(game)
            if score >= 0:
                scored.append((score, game, reasons))

        scored.sort(key=lambda item: (-item[0], item[1].name))
        top = scored[:5]

        self.results_wrap.clear_widgets()
        self.results_wrap.add_widget(SectionHeader(title="Rekomendasi Untukmu"))

        if not top:
            self.results_wrap.add_widget(EmptyState(
                title="Belum menemukan game",
                subtitle="Coba ubah beberapa jawaban agar hasilnya lebih luas.",
            ))
            return

        best_score = top[0][0]
        for score, game, reasons in top:
            reason_text = " • ".join(reasons[:3]) if reasons else "Pilihan yang cukup sesuai dengan jawabanmu."
            if score == best_score:
                reason_text = "Paling cocok: " + reason_text
            self.results_wrap.add_widget(
                GameRecommendationCard(game, reason=reason_text, on_press_game=app.open_game_detail)
            )

        note = Label(text="Rekomendasi dihitung langsung dari data game di aplikasi dan dapat dicoba ulang kapan saja.",
                     color=AppColors.TEXT_MUTED, font_size=sp(9.5), halign="center", valign="middle",
                     size_hint_y=None, height=dp(34))
        note.bind(width=lambda *a: setattr(note, "text_size", (note.width, None)))
        self.results_wrap.add_widget(note)

    def on_pre_enter(self):
        self._build_form()


# ==================================================
# 18. RANDOM GAME
# ==================================================
class RandomGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_game = None
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos), size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(size_hint_y=None, height=dp(64), padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, 0))
        back_btn = AppIconButton(icon_text="<", size_dp=36)
        back_btn.bind(on_release=lambda *_: App.get_running_app().go_back())
        back_wrap = BoxLayout(size_hint=(None, 1), width=dp(36))
        back_wrap.add_widget(back_btn)
        header.add_widget(back_wrap)
        title = Label(text="Random Game", color=AppColors.TEXT, font_size=AppTypography.HEADING, bold=True,
                      halign="left", valign="middle")
        title.bind(size=title.setter("text_size"))
        header.add_widget(title)
        root.add_widget(header)

        self.card_wrap = BoxLayout(orientation="vertical", padding=(AppSpacing.LG, AppSpacing.SM),
                                    spacing=AppSpacing.LG)
        self.result_holder = BoxLayout(orientation="vertical", size_hint_y=None)
        self.card_wrap.add_widget(self.result_holder)

        roll_btn = AppButton(text="Acak Permainan", size_hint_y=None, height=dp(50))
        roll_btn.bind(on_release=lambda *_: self._roll())
        self.card_wrap.add_widget(roll_btn)
        self.open_btn = AppButton(text="Buka Detail", bg_color=AppColors.ELEVATED, text_color=AppColors.TEXT,
                                   size_hint_y=None, height=dp(50))
        self.open_btn.bind(on_release=lambda *_: self._open_detail())
        self.open_btn.opacity = 0
        self.open_btn.disabled = True
        self.card_wrap.add_widget(self.open_btn)
        self.card_wrap.add_widget(BoxLayout())
        root.add_widget(self.card_wrap)
        self.add_widget(root)

    def _roll(self):
        pool = GAME_OBJECTS
        app = App.get_running_app()
        filters = getattr(app, "random_filters", None)
        if filters:
            pool = filter_games(
                GAME_OBJECTS,
                categories=filters.get("category") or None,
                player_buckets=filters.get("players") or None,
                duration_buckets=filters.get("duration") or None,
                difficulties=filters.get("difficulty") or None,
            ) or GAME_OBJECTS
        self.current_game = random.choice(pool)
        self.result_holder.clear_widgets()
        card = FeaturedGameCard(self.current_game, on_press_game=lambda gid: self._open_detail())
        self.result_holder.add_widget(card)
        self.result_holder.height = card.height
        self.open_btn.opacity = 1
        self.open_btn.disabled = False
        anim = Animation(opacity=0.3, duration=0.08) + Animation(opacity=1, duration=0.18)
        anim.start(card)

    def _open_detail(self):
        if self.current_game:
            App.get_running_app().open_game_detail(self.current_game.id)

    def on_pre_enter(self):
        if not self.current_game:
            self._roll()


# ==================================================
# 19. GAME DETAIL
# ==================================================
class GameDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = None
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos), size=lambda *a: setattr(self._bg, "size", root.size))

        self.header = BoxLayout(size_hint_y=None, height=dp(56), padding=(AppSpacing.MD, 0), spacing=AppSpacing.XS)
        back_btn = AppIconButton(icon_text="<", size_dp=36)
        back_btn.bind(on_release=lambda *_: App.get_running_app().go_back())
        back_wrap = BoxLayout(size_hint=(None, 1), width=dp(36))
        back_wrap.add_widget(back_btn)
        self.header.add_widget(back_wrap)
        self.header.add_widget(BoxLayout())
        self.fav_wrap = BoxLayout(size_hint=(None, 1), width=dp(40))
        self.header.add_widget(self.fav_wrap)
        root.add_widget(self.header)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(orientation="vertical", size_hint_y=None,
                                  padding=(AppSpacing.LG, 0, AppSpacing.LG, AppSpacing.XXL),
                                  spacing=AppSpacing.LG)
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def open_game(self, game_id):
        game = get_game_by_id(game_id)
        if not game:
            return
        self.game = game
        STORAGE.add_recently_viewed(game_id)
        self._render()

    def _favorite_changed(self):
        app = App.get_running_app()
        try:
            app.main_shell.favorite_screen.refresh()
        except Exception:
            pass

    def _label(self, text, color=None, size=None, bold=False, height=None):
        from kivy.uix.label import Label
        lbl = Label(text=text, color=color or AppColors.TEXT, font_size=size or AppTypography.BODY,
                    bold=bold, halign="left", valign="top", size_hint_y=None)
        lbl.bind(width=lambda *a: setattr(lbl, "text_size", (lbl.width, None)))
        lbl.bind(texture_size=lambda *a: setattr(lbl, "height", lbl.texture_size[1]))
        return lbl

    def _section_block(self, title, body_widget):
        wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
        wrap.bind(minimum_height=wrap.setter("height"))
        wrap.add_widget(SectionHeader(title=title))
        wrap.add_widget(body_widget)
        return wrap

    def _render(self):
        game = self.game
        self.fav_wrap.clear_widgets()
        fav_btn = FavoriteButton(
            game_id=game.id, size_dp=40,
            on_change=lambda *_: self._favorite_changed()
        )
        self.fav_wrap.add_widget(fav_btn)

        self.content.clear_widgets()

        cat_lbl = self._label(game.category.upper(), color=AppColors.GOLD, size=AppTypography.META, bold=True)
        cat_lbl.height = dp(18)
        self.content.add_widget(cat_lbl)

        name_lbl = self._label(game.name, color=AppColors.TEXT, size=AppTypography.HERO, bold=True)
        self.content.add_widget(name_lbl)

        desc_lbl = self._label(game.description, color=AppColors.TEXT_SECONDARY, size=AppTypography.BODY)
        self.content.add_widget(desc_lbl)

        meta_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=AppSpacing.LG)
        meta_row.add_widget(MetadataItem(label="Pemain", value=game.player_label()))
        meta_row.add_widget(MetadataItem(label="Durasi", value=game.duration))
        diff_col = BoxLayout(orientation="vertical", spacing=dp(2))
        diff_badge_wrap = BoxLayout(size_hint_y=None, height=dp(24))
        diff_badge_wrap.add_widget(DifficultyBadge(difficulty=game.difficulty))
        diff_col.add_widget(diff_badge_wrap)
        diff_col.add_widget(self._label("Difficulty", color=AppColors.TEXT_MUTED, size=AppTypography.META, height=dp(16)))
        meta_row.add_widget(diff_col)
        self.content.add_widget(meta_row)

        if game.about:
            self.content.add_widget(self._section_block("Tentang", self._label(game.about, color=AppColors.TEXT_SECONDARY)))
        if game.objective:
            self.content.add_widget(self._section_block("Tujuan", self._label(game.objective, color=AppColors.TEXT_SECONDARY)))
        if game.setup:
            self.content.add_widget(self._section_block("Persiapan", self._label(game.setup, color=AppColors.TEXT_SECONDARY)))

        if game.how_to_play:
            steps_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
            steps_wrap.bind(minimum_height=steps_wrap.setter("height"))
            for i, step in enumerate(game.how_to_play, start=1):
                steps_wrap.add_widget(QuickGuideStep(i, step))
            self.content.add_widget(self._section_block("Cara Bermain", steps_wrap))

        if game.special_cards:
            special_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
            special_wrap.bind(minimum_height=special_wrap.setter("height"))
            for sc in game.special_cards:
                special_wrap.add_widget(SpecialCardTile(sc))
            self.content.add_widget(self._section_block("Kartu Khusus", special_wrap))

        if game.ranking:
            ranking_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6))
            ranking_wrap.bind(minimum_height=ranking_wrap.setter("height"))
            for i, r in enumerate(game.ranking, start=1):
                ranking_wrap.add_widget(RankingCard(i, r))
            self.content.add_widget(self._section_block("Ranking / Kombinasi", ranking_wrap))

        if game.scoring:
            self.content.add_widget(self._section_block("Scoring", self._label(game.scoring, color=AppColors.TEXT_SECONDARY)))

        if game.tips:
            tips_text = "\n".join(f"\u2022 {t}" for t in game.tips)
            self.content.add_widget(self._section_block("Tips", self._label(tips_text, color=AppColors.TEXT_SECONDARY)))

        if game.variations:
            var_text = "\n".join(f"\u2022 {v}" for v in game.variations)
            self.content.add_widget(self._section_block("Variasi", self._label(var_text, color=AppColors.TEXT_SECONDARY)))

        if game.quick_guide:
            qg_wrap = BoxLayout(orientation="vertical", size_hint_y=None, spacing=AppSpacing.XS)
            qg_wrap.bind(minimum_height=qg_wrap.setter("height"))
            for i, step in enumerate(game.quick_guide, start=1):
                qg_wrap.add_widget(QuickGuideStep(i, step))
            self.content.add_widget(self._section_block("Panduan Cepat", qg_wrap))


# ==================================================
# 20. FAVORIT
# ==================================================
class FavoriteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos), size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(size_hint_y=None, height=dp(72), padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, 0), spacing=dp(8))
        title_box = BoxLayout(orientation="vertical", spacing=dp(1))
        title = Label(text="Favorit", color=AppColors.TEXT, font_size=AppTypography.HEADING, bold=True,
                      halign="left", valign="bottom", size_hint_y=None, height=dp(34))
        title.bind(size=title.setter("text_size"))
        self.count_label = Label(text="", color=AppColors.TEXT_MUTED, font_size=AppTypography.META,
                                 halign="left", valign="top", size_hint_y=None, height=dp(18))
        self.count_label.bind(size=self.count_label.setter("text_size"))
        title_box.add_widget(title)
        title_box.add_widget(self.count_label)
        header.add_widget(title_box)
        root.add_widget(header)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(orientation="vertical", size_hint_y=None,
                                  padding=(AppSpacing.LG, AppSpacing.SM, AppSpacing.LG, AppSpacing.XXL),
                                  spacing=AppSpacing.SM)
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        app = App.get_running_app()
        self.content.clear_widgets()
        fav_ids = STORAGE.get_favorites()
        games = [g for g in GAME_OBJECTS if g.id in fav_ids]
        self.count_label.text = f"{len(games)} permainan tersimpan" if games else "Belum ada permainan tersimpan"
        if not games:
            self.content.add_widget(EmptyState(
                icon="heart", title="Belum ada permainan favorit.",
                subtitle="Tekan ikon hati pada kartu atau halaman detail untuk menyimpan permainan.",
                button_text="Jelajahi Permainan", on_button=lambda: app.go_to_explore(),
            ))
            return
        for g in games:
            self.content.add_widget(GameCard(
                g, on_press_game=app.open_game_detail,
                on_favorite_change=self._favorite_changed
            ))

    def _favorite_changed(self, game_id, is_favorite):
        if not is_favorite:
            Clock.schedule_once(lambda dt: self.refresh(), 0)


# ==================================================
# 21. RECENTLY VIEWED
# ==================================================
# Recently Viewed ditampilkan pada HomeScreen (section "Baru Dilihat"),
# didukung oleh LocalStorage.add_recently_viewed() / get_recently_viewed().


# ==================================================
# 22. TENTANG
# ==================================================
class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        from kivy.uix.label import Label
        root = BoxLayout(orientation="vertical")
        with root.canvas.before:
            Color(*AppColors.BG)
            self._bg = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, "pos", root.pos), size=lambda *a: setattr(self._bg, "size", root.size))

        header = BoxLayout(size_hint_y=None, height=dp(64), padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, 0))
        title = Label(text="Tentang", color=AppColors.TEXT, font_size=AppTypography.HEADING, bold=True,
                      halign="left", valign="middle")
        title.bind(size=title.setter("text_size"))
        header.add_widget(title)
        root.add_widget(header)

        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation="vertical", size_hint_y=None,
                             padding=(AppSpacing.LG, AppSpacing.MD, AppSpacing.LG, AppSpacing.XXL),
                             spacing=AppSpacing.LG)
        content.bind(minimum_height=content.setter("height"))

        logo_wrap = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(120), spacing=AppSpacing.XS)

        class _LogoCircle(BoxLayout, RoundedBG):
            pass

        logo = _LogoCircle(size_hint=(None, None), size=(dp(72), dp(72)), pos_hint={"center_x": 0.5})
        logo.init_rounded_bg(color=AppColors.PRIMARY, radius=dp(36))
        logo.add_widget(Label(text="K", color=AppColors.WHITE, font_size=sp(30), bold=True))
        logo_row = BoxLayout(size_hint_y=None, height=dp(72))
        logo_row.add_widget(BoxLayout())
        logo_row.add_widget(logo)
        logo_row.add_widget(BoxLayout())
        logo_wrap.add_widget(logo_row)

        name_lbl = Label(text=APP_NAME, color=AppColors.TEXT, font_size=AppTypography.HEADING, bold=True,
                          size_hint_y=None, height=dp(30))
        logo_wrap.add_widget(name_lbl)
        content.add_widget(logo_wrap)

        tagline_lbl = Label(text=APP_TAGLINE, color=AppColors.GOLD_LIGHT, font_size=AppTypography.BODY,
                             halign="center", size_hint_y=None, height=dp(24))
        tagline_lbl.bind(width=lambda *a: setattr(tagline_lbl, "text_size", (tagline_lbl.width, None)))
        content.add_widget(tagline_lbl)

        desc_text = (
            "KartuPedia adalah ensiklopedia dan panduan permainan kartu offline. "
            "Aplikasi ini membantu kamu menemukan permainan kartu baru, memahami "
            "aturan mainnya secara lengkap, dan memilih permainan yang sesuai "
            "dengan jumlah pemain, waktu, serta gaya bermainmu. KartuPedia bukan "
            "aplikasi untuk memainkan game secara langsung, melainkan panduan "
            "referensi yang bisa diakses kapan saja tanpa koneksi internet."
        )
        desc_lbl = Label(text=desc_text, color=AppColors.TEXT_SECONDARY, font_size=AppTypography.BODY,
                          halign="left", valign="top", size_hint_y=None)
        desc_lbl.bind(width=lambda *a: setattr(desc_lbl, "text_size", (desc_lbl.width, None)))
        desc_lbl.bind(texture_size=lambda *a: setattr(desc_lbl, "height", desc_lbl.texture_size[1]))
        content.add_widget(desc_lbl)

        info_card = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(90),
                               padding=AppSpacing.MD, spacing=dp(6))

        class _InfoCard(BoxLayout, RoundedBG):
            pass

        info_card = _InfoCard(orientation="vertical", size_hint_y=None, height=dp(90),
                               padding=AppSpacing.MD, spacing=dp(6))
        info_card.init_rounded_bg(color=AppColors.SURFACE, radius=AppRadius.MD, border_color=AppColors.BORDER)
        version_lbl = Label(text=f"Versi Aplikasi: {APP_VERSION}", color=AppColors.TEXT, font_size=AppTypography.CAPTION,
                             halign="left", valign="middle", size_hint_y=None, height=dp(20))
        version_lbl.bind(size=version_lbl.setter("text_size"))
        offline_lbl = Label(text="Status: Panduan Permainan Kartu Offline", color=AppColors.TEXT_SECONDARY,
                             font_size=AppTypography.CAPTION, halign="left", valign="middle",
                             size_hint_y=None, height=dp(20))
        offline_lbl.bind(size=offline_lbl.setter("text_size"))
        total_lbl = Label(text=f"Total Permainan: {len(GAME_OBJECTS)} game", color=AppColors.TEXT_SECONDARY,
                           font_size=AppTypography.CAPTION, halign="left", valign="middle",
                           size_hint_y=None, height=dp(20))
        total_lbl.bind(size=total_lbl.setter("text_size"))
        info_card.add_widget(version_lbl)
        info_card.add_widget(offline_lbl)
        info_card.add_widget(total_lbl)
        content.add_widget(info_card)

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)


# ==================================================
# 23. MAIN APP
# ==================================================
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


# ==================================================
# 24. ENTRY POINT
# ==================================================
if __name__ == "__main__":
    KartuPediaApp().run()
