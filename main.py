import kivy

kivy.require("2.3.0")

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


# ============================================================
# DATABASE GAME
# ============================================================

GAMES = [

    {
        "name": "Regicide",
        "category": "Kooperatif",
        "players": "1-4 pemain",
        "duration": "20-40 menit",
        "difficulty": "Menengah",
        "deck": "52 kartu",
        "featured": True,
        "description":
            "Permainan kartu kooperatif di mana pemain bekerja sama "
            "untuk mengalahkan seluruh musuh kerajaan.",
        "goal":
            "Kalahkan seluruh 12 kartu musuh yang terdiri dari "
            "Jack, Queen, dan King.",
        "setup": [
            "Pisahkan Jack, Queen, dan King sebagai kartu musuh.",
            "Kocok kartu lainnya sebagai deck pemain.",
            "Bagikan kartu sesuai jumlah pemain.",
            "Buka musuh satu per satu."
        ],
        "rules": [
            "Pemain memainkan satu kartu dari tangan.",
            "Nilai kartu menentukan jumlah damage.",
            "Suit memberikan kemampuan khusus.",
            "Setelah menyerang, musuh melakukan serangan.",
            "Pemain harus bertahan dari damage musuh.",
            "Kalahkan seluruh musuh untuk memenangkan permainan."
        ],
        "special": [
            "Hearts dapat memulihkan damage.",
            "Diamonds memungkinkan pemain menarik kartu.",
            "Clubs meningkatkan damage.",
            "Spades mengurangi damage musuh."
        ],
        "score":
            "Pemain menang apabila seluruh 12 musuh berhasil "
            "dikalahkan.",
        "tips":
            "Gunakan kemampuan suit pada saat yang tepat dan "
            "diskusikan strategi dengan pemain lain."
    },

    {
        "name": "Blackjack",
        "category": "Casino",
        "players": "2+ pemain",
        "duration": "5-20 menit",
        "difficulty": "Mudah",
        "deck": "52 kartu",
        "featured": True,
        "description":
            "Permainan kartu dengan tujuan mendapatkan nilai "
            "sedekat mungkin dengan 21 tanpa melewatinya.",
        "goal":
            "Mendapatkan nilai lebih tinggi daripada dealer "
            "tanpa melebihi 21.",
        "setup": [
            "Tentukan seorang dealer.",
            "Setiap pemain mendapatkan dua kartu.",
            "Dealer mendapatkan dua kartu.",
            "Salah satu kartu dealer biasanya terbuka."
        ],
        "rules": [
            "Hit untuk mengambil kartu tambahan.",
            "Stand untuk berhenti mengambil kartu.",
            "Jika total lebih dari 21, pemain bust.",
            "Dealer menjalankan aturan dealer.",
            "Bandingkan nilai akhir pemain dengan dealer."
        ],
        "special": [
            "Ace bernilai 1 atau 11.",
            "Jack bernilai 10.",
            "Queen bernilai 10.",
            "King bernilai 10."
        ],
        "score":
            "Pemain menang jika nilainya lebih dekat ke 21 "
            "daripada dealer.",
        "tips":
            "Pertimbangkan risiko melewati 21 sebelum mengambil "
            "kartu tambahan."
    },

    {
        "name": "Texas Hold'em",
        "category": "Poker",
        "players": "2-10 pemain",
        "duration": "20-90 menit",
        "difficulty": "Menengah",
        "deck": "52 kartu",
        "featured": True,
        "description":
            "Varian poker yang menggunakan kartu pribadi dan "
            "kartu komunitas untuk membentuk kombinasi terbaik.",
        "goal":
            "Membentuk kombinasi lima kartu terbaik.",
        "setup": [
            "Setiap pemain mendapatkan dua kartu pribadi.",
            "Siapkan lima kartu komunitas.",
            "Tentukan dealer dan blind."
        ],
        "rules": [
            "Pre-flop menggunakan dua kartu pribadi.",
            "Flop membuka tiga kartu komunitas.",
            "Turn membuka kartu komunitas keempat.",
            "River membuka kartu komunitas kelima.",
            "Pemain yang tersisa melakukan showdown."
        ],
        "special": [
            "Pair",
            "Two Pair",
            "Three of a Kind",
            "Straight",
            "Flush",
            "Full House",
            "Four of a Kind",
            "Straight Flush",
            "Royal Flush"
        ],
        "score":
            "Kombinasi lima kartu terbaik memenangkan pot.",
        "tips":
            "Perhatikan kemungkinan kombinasi dari kartu komunitas, "
            "bukan hanya kartu pribadi."
    },

    {
        "name": "Hearts",
        "category": "Trick Taking",
        "players": "4 pemain",
        "duration": "20-40 menit",
        "difficulty": "Mudah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan trick-taking di mana pemain berusaha "
            "mendapatkan poin sesedikit mungkin.",
        "goal":
            "Memiliki total poin paling rendah.",
        "setup": [
            "Bagikan seluruh kartu.",
            "Lakukan passing kartu sesuai variasi permainan."
        ],
        "rules": [
            "Ikuti suit kartu pertama jika memungkinkan.",
            "Kartu tertinggi dari suit tersebut memenangkan trick.",
            "Kartu Hearts memberikan poin.",
            "Queen of Spades memberikan penalti besar."
        ],
        "special": [
            "Setiap Hearts bernilai 1 poin.",
            "Queen of Spades bernilai 13 poin."
        ],
        "score":
            "Pemain dengan total poin paling sedikit menjadi pemenang.",
        "tips":
            "Hindari mengambil trick yang berisi banyak Hearts."
    },

    {
        "name": "Spades",
        "category": "Trick Taking",
        "players": "4 pemain",
        "duration": "30-60 menit",
        "difficulty": "Menengah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan trick-taking berbasis bid dengan Spades "
            "sebagai trump.",
        "goal":
            "Mencapai target skor dengan memenuhi jumlah trick "
            "yang telah di-bid.",
        "setup": [
            "Bagikan seluruh kartu.",
            "Pemain melakukan bid.",
            "Pemain biasanya bermain dalam pasangan."
        ],
        "rules": [
            "Setiap pemain menentukan jumlah trick.",
            "Pemain harus mengikuti suit jika memiliki suit tersebut.",
            "Spades berfungsi sebagai trump.",
            "Pasangan berusaha memenuhi total bid."
        ],
        "special": [
            "Spades adalah trump.",
            "Jumlah bid memengaruhi skor."
        ],
        "score":
            "Skor dihitung berdasarkan bid dan trick yang berhasil.",
        "tips":
            "Jangan melakukan bid terlalu tinggi jika kartu tidak "
            "mendukung."
    },

    {
        "name": "Crazy Eights",
        "category": "Shedding",
        "players": "2-8 pemain",
        "duration": "10-20 menit",
        "difficulty": "Mudah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan shedding sederhana dengan kartu 8 sebagai "
            "kartu khusus.",
        "goal":
            "Menjadi pemain pertama yang menghabiskan semua kartu.",
        "setup": [
            "Bagikan kartu kepada pemain.",
            "Buka satu kartu awal.",
            "Sisa kartu menjadi draw pile."
        ],
        "rules": [
            "Mainkan kartu dengan rank atau suit yang sama.",
            "Jika tidak memiliki kartu yang cocok, ambil kartu.",
            "Kartu 8 dapat digunakan sebagai kartu khusus.",
            "Pemain pertama yang kehabisan kartu menang."
        ],
        "special": [
            "Kartu 8 dapat digunakan untuk mengganti suit."
        ],
        "score":
            "Pemain pertama yang menghabiskan semua kartu menang.",
        "tips":
            "Simpan kartu 8 untuk situasi ketika pilihan kartu "
            "lain terbatas."
    },

    {
        "name": "Go Fish",
        "category": "Set Collection",
        "players": "2-6 pemain",
        "duration": "10-20 menit",
        "difficulty": "Sangat mudah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan sederhana untuk mengumpulkan empat kartu "
            "dengan rank yang sama.",
        "goal":
            "Mengumpulkan set kartu sebanyak mungkin.",
        "setup": [
            "Bagikan kartu awal.",
            "Sisa kartu menjadi draw pile."
        ],
        "rules": [
            "Minta pemain lain rank tertentu.",
            "Jika mereka memiliki kartu tersebut, kartu diberikan.",
            "Jika tidak, pemain mengatakan Go Fish.",
            "Ambil kartu dari draw pile.",
            "Lengkapi set empat kartu."
        ],
        "special": [
            "Suit tidak menjadi faktor utama."
        ],
        "score":
            "Set lengkap bernilai satu poin.",
        "tips":
            "Ingat kartu yang pernah diminta oleh pemain lain."
    },

    {
        "name": "War",
        "category": "Perbandingan",
        "players": "2 pemain",
        "duration": "10-30 menit",
        "difficulty": "Sangat mudah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan perbandingan kartu sederhana yang sangat "
            "mudah dipelajari.",
        "goal":
            "Mendapatkan seluruh kartu lawan.",
        "setup": [
            "Bagikan seluruh deck secara merata."
        ],
        "rules": [
            "Kedua pemain membuka kartu teratas.",
            "Kartu dengan rank lebih tinggi menang.",
            "Jika rank sama, terjadi War.",
            "Permainan berlanjut sampai salah satu pemain memiliki "
            "seluruh kartu."
        ],
        "special": [
            "Suit biasanya tidak digunakan."
        ],
        "score":
            "Pemain yang memiliki seluruh kartu menjadi pemenang.",
        "tips":
            "Cocok untuk pemain yang baru mengenal permainan kartu."
    },

    {
        "name": "Solitaire",
        "category": "Solo",
        "players": "1 pemain",
        "duration": "5-30 menit",
        "difficulty": "Menengah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan kartu solo klasik dengan tujuan menyusun "
            "seluruh kartu ke foundation.",
        "goal":
            "Memindahkan seluruh kartu ke foundation dari Ace "
            "hingga King.",
        "setup": [
            "Buat tujuh kolom tableau.",
            "Letakkan kartu dengan jumlah berbeda.",
            "Buka kartu teratas.",
            "Sisa kartu menjadi stock."
        ],
        "rules": [
            "Susun kartu secara menurun.",
            "Warna harus bergantian.",
            "King dapat ditempatkan pada kolom kosong.",
            "Foundation dimulai dari Ace.",
            "Susun setiap suit sampai King."
        ],
        "special": [
            "Foundation terpisah untuk setiap suit."
        ],
        "score":
            "Menang apabila seluruh kartu masuk ke foundation.",
        "tips":
            "Jangan terburu-buru memindahkan kartu jika langkah "
            "tersebut justru mengurangi pilihan."
    },

    {
        "name": "Gin Rummy",
        "category": "Rummy",
        "players": "2 pemain",
        "duration": "15-30 menit",
        "difficulty": "Menengah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan rummy dua pemain yang berfokus pada "
            "pembentukan set dan run.",
        "goal":
            "Membentuk kombinasi kartu dan meminimalkan kartu "
            "yang tidak tergabung.",
        "setup": [
            "Bagikan 10 kartu kepada setiap pemain.",
            "Siapkan stock dan discard pile."
        ],
        "rules": [
            "Ambil kartu.",
            "Bentuk set atau run.",
            "Buang satu kartu.",
            "Pemain dapat melakukan knock sesuai aturan."
        ],
        "special": [
            "Set memiliki rank yang sama.",
            "Run memiliki suit yang sama dan berurutan."
        ],
        "score":
            "Skor berasal dari kartu yang tidak tergabung "
            "dan bonus tertentu.",
        "tips":
            "Perhatikan kartu yang dibuang lawan."
    },

    {
        "name": "Rummy",
        "category": "Rummy",
        "players": "2-6 pemain",
        "duration": "20-60 menit",
        "difficulty": "Menengah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan dari kelompok Rummy yang berfokus pada "
            "pembentukan meld.",
        "goal":
            "Membentuk kombinasi kartu dan menghabiskan kartu "
            "di tangan.",
        "setup": [
            "Bagikan kartu sesuai variasi.",
            "Siapkan stock dan discard pile."
        ],
        "rules": [
            "Ambil kartu.",
            "Bentuk meld.",
            "Tambahkan kartu ke meld jika memungkinkan.",
            "Buang satu kartu."
        ],
        "special": [
            "Set menggunakan rank yang sama.",
            "Run menggunakan suit yang sama."
        ],
        "score":
            "Kartu yang tersisa menjadi penalti.",
        "tips":
            "Jangan menyimpan terlalu banyak kartu yang sulit "
            "dikombinasikan."
    },

    {
        "name": "Old Maid",
        "category": "Pairing",
        "players": "2-8 pemain",
        "duration": "10-20 menit",
        "difficulty": "Sangat mudah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan mencocokkan pasangan kartu sambil "
            "menghindari kartu yang tidak memiliki pasangan.",
        "goal":
            "Tidak memegang kartu tanpa pasangan pada akhir permainan.",
        "setup": [
            "Siapkan pasangan kartu.",
            "Sisakan satu kartu tanpa pasangan.",
            "Bagikan seluruh kartu."
        ],
        "rules": [
            "Buang pasangan yang dimiliki.",
            "Ambil kartu secara acak dari pemain lain.",
            "Jika membentuk pasangan, buang pasangan tersebut.",
            "Permainan berakhir ketika pasangan habis."
        ],
        "special": [
            "Satu kartu tidak memiliki pasangan."
        ],
        "score":
            "Pemain yang memegang kartu tanpa pasangan kalah.",
        "tips":
            "Jangan memberikan petunjuk tentang kartu yang sedang "
            "kamu pegang."
    },

    {
        "name": "Memory Match",
        "category": "Memory",
        "players": "1+ pemain",
        "duration": "5-20 menit",
        "difficulty": "Mudah",
        "deck": "Kartu berpasangan",
        "featured": False,
        "description":
            "Permainan memori untuk menemukan pasangan kartu "
            "yang sama.",
        "goal":
            "Mengumpulkan pasangan kartu sebanyak mungkin.",
        "setup": [
            "Letakkan semua kartu menghadap ke bawah.",
            "Susun menjadi grid."
        ],
        "rules": [
            "Balik dua kartu.",
            "Jika sama, ambil pasangan.",
            "Jika berbeda, tutup kembali.",
            "Lanjutkan sampai semua kartu ditemukan."
        ],
        "special": [
            "Tidak menggunakan suit khusus."
        ],
        "score":
            "Satu pasangan bernilai satu poin.",
        "tips":
            "Ingat posisi kartu yang pernah dibuka."
    },

    {
        "name": "President",
        "category": "Shedding",
        "players": "3-8 pemain",
        "duration": "15-30 menit",
        "difficulty": "Mudah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan shedding cepat di mana pemain berusaha "
            "menghabiskan kartu secepat mungkin.",
        "goal":
            "Menjadi pemain pertama yang menghabiskan seluruh kartu.",
        "setup": [
            "Bagikan seluruh kartu.",
            "Tentukan pemain pertama."
        ],
        "rules": [
            "Mainkan satu atau beberapa kartu dengan rank sama.",
            "Pemain berikutnya harus memainkan rank lebih tinggi.",
            "Pemain dapat melakukan pass.",
            "Jika semua pass, tumpukan dibersihkan."
        ],
        "special": [
            "Beberapa variasi memiliki rank khusus."
        ],
        "score":
            "Urutan pemain selesai menentukan posisi.",
        "tips":
            "Simpan kartu tinggi untuk mengendalikan bagian akhir."
    },

    {
        "name": "Spoons",
        "category": "Refleks",
        "players": "3-13 pemain",
        "duration": "10-20 menit",
        "difficulty": "Mudah",
        "deck": "52 kartu",
        "featured": False,
        "description":
            "Permainan cepat yang menggabungkan pengumpulan set "
            "dan refleks.",
        "goal":
            "Mendapatkan empat kartu dengan rank yang sama "
            "dan mengambil sendok.",
        "setup": [
            "Letakkan sendok di tengah.",
            "Jumlah sendok satu lebih sedikit dari pemain.",
            "Bagikan empat kartu."
        ],
        "rules": [
            "Ambil satu kartu.",
            "Teruskan satu kartu ke pemain berikutnya.",
            "Cari empat rank yang sama.",
            "Jika mendapat empat kartu sama, ambil sendok.",
            "Pemain lain harus segera mengambil sendok."
        ],
        "special": [
            "Suit tidak menjadi faktor utama."
        ],
        "score":
            "Pemain yang tidak mendapatkan sendok mendapat penalti.",
        "tips":
            "Perhatikan gerakan pemain lain, bukan hanya kartu sendiri."
    }
]


# ============================================================
# KV
# ============================================================

KV = """

#:import dp kivy.metrics.dp


<MainScreen>:

    BoxLayout:

        orientation: "vertical"

        canvas.before:

            Color:
                rgba: 0.025, 0.027, 0.035, 1

            Rectangle:
                pos: self.pos
                size: self.size


        # ====================================================
        # HEADER
        # ====================================================

        BoxLayout:

            orientation: "vertical"

            size_hint_y: None

            height: dp(105)

            padding: dp(28), dp(20), dp(28), dp(8)


            Label:

                text: "KartuPedia"

                font_size: "31sp"

                bold: True

                color: 0.94, 0.95, 0.98, 1

                halign: "left"

                valign: "bottom"

                text_size: self.size


            Label:

                text: "Panduan permainan kartu dalam satu tempat."

                font_size: "13sp"

                color: 0.48, 0.51, 0.59, 1

                halign: "left"

                valign: "top"

                text_size: self.size


        # ====================================================
        # SEARCH
        # ====================================================

        BoxLayout:

            size_hint_y: None

            height: dp(52)

            padding: dp(28), dp(4), dp(28), dp(4)

            spacing: dp(10)

            canvas.before:

                Color:
                    rgba: 0.065, 0.068, 0.09, 1

                RoundedRectangle:

                    pos: self.pos

                    size: self.size

                    radius: [dp(14)]


            # Label kecil

            Label:

                text: "CARI"

                size_hint_x: None

                width: dp(34)

                font_size: "9sp"

                bold: True

                color: 0.46, 0.56, 0.76, 1

                halign: "center"

                valign: "middle"

                text_size: self.size


            # Input pencarian

            TextInput:

                id: search

                hint_text: "Cari permainan..."

                hint_text_color: 0.36, 0.39, 0.47, 1

                foreground_color: 0.90, 0.91, 0.95, 1

                background_color: 0, 0, 0, 0

                cursor_color: 0.55, 0.66, 0.88, 1

                selection_color: 0.25, 0.35, 0.55, 0.35

                font_size: "13sp"

                multiline: False

                padding: dp(0), dp(12), dp(0), dp(8)

                write_tab: False

                on_text:

                    root.search_games(self.text)


        # ====================================================
        # MAIN CONTENT SCROLL
        # ====================================================

        ScrollView:

            id: main_scroll

            do_scroll_x: False

            bar_width: dp(3)

            scroll_type: ["bars", "content"]


            BoxLayout:

                orientation: "vertical"

                spacing: dp(18)

                padding: dp(28), dp(14), dp(28), dp(35)

                size_hint_y: None

                height: self.minimum_height


                # ============================================
                # FEATURED HEADER
                # ============================================

                BoxLayout:

                    size_hint_y: None

                    height: dp(32)


                    Label:

                        text: "Permainan unggulan"

                        font_size: "19sp"

                        bold: True

                        color: 0.92, 0.93, 0.97, 1

                        halign: "left"

                        text_size: self.size


                    Label:

                        text: "Mulai dari sini"

                        size_hint_x: None

                        width: dp(100)

                        font_size: "11sp"

                        color: 0.43, 0.47, 0.56, 1

                        halign: "right"

                        text_size: self.size


                # ============================================
                # FEATURED
                # ============================================

                FeaturedCard:

                    id: featured_card


                # ============================================
                # LIST HEADER
                # ============================================

                BoxLayout:

                    size_hint_y: None

                    height: dp(32)


                    Label:

                        text: "Semua permainan"

                        font_size: "19sp"

                        bold: True

                        color: 0.92, 0.93, 0.97, 1

                        halign: "left"

                        text_size: self.size


                    Label:

                        id: result_count

                        text: ""

                        size_hint_x: None

                        width: dp(100)

                        font_size: "11sp"

                        color: 0.43, 0.47, 0.56, 1

                        halign: "right"

                        text_size: self.size


                # ============================================
                # CATEGORIES
                # ============================================

                ScrollView:

                    size_hint_y: None

                    height: dp(38)

                    do_scroll_x: True

                    do_scroll_y: False

                    bar_width: 0


                    GridLayout:

                        id: categories

                        rows: 1

                        spacing: dp(8)

                        size_hint_x: None

                        width: self.minimum_width


                # ============================================
                # GAME LIST
                # ============================================

                GridLayout:

                    id: game_list

                    cols: 1

                    spacing: dp(10)

                    size_hint_y: None

                    height: self.minimum_height


# ============================================================
# DETAIL SCREEN
# ============================================================

<DetailScreen>:

    BoxLayout:

        orientation: "vertical"

        canvas.before:

            Color:
                rgba: 0.025, 0.027, 0.035, 1

            Rectangle:
                pos: self.pos
                size: self.size


        # ====================================================
        # TOP BAR
        # ====================================================

        BoxLayout:

            size_hint_y: None

            height: dp(68)

            padding: dp(20), dp(14)

            spacing: dp(14)


            Button:

                text: "<  Kembali"

                size_hint_x: None

                width: dp(110)

                background_normal: ""

                background_color: 0.075, 0.08, 0.105, 1

                color: 0.82, 0.84, 0.90, 1

                font_size: "13sp"

                on_release:
                    app.root.current = "main"


            Label:

                text: "DETAIL PERMAINAN"

                font_size: "10sp"

                bold: True

                color: 0.40, 0.44, 0.52, 1

                halign: "left"

                valign: "middle"

                text_size: self.size


        # ====================================================
        # DETAIL CONTENT
        # ====================================================

        ScrollView:

            do_scroll_x: False

            bar_width: dp(3)


            BoxLayout:

                id: detail_content

                orientation: "vertical"

                spacing: dp(18)

                padding: dp(28), dp(20), dp(28), dp(40)

                size_hint_y: None

                height: self.minimum_height
"""


# ============================================================
# FEATURED CARD
# ============================================================

class FeaturedCard(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.game = None

        self.orientation = "horizontal"

        self.size_hint_y = None

        self.height = dp(175)

        self.padding = dp(24)

        self.spacing = dp(20)

        with self.canvas.before:

            Color(
                rgba=(0.075, 0.09, 0.14, 1)
            )

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(18)]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # LEFT

        left = BoxLayout(
            orientation="vertical",
            spacing=dp(3)
        )

        self.category = Label(
            text="",
            font_size="10sp",
            bold=True,
            color=(0.48, 0.60, 0.82, 1),
            size_hint_y=None,
            height=dp(18),
            halign="left"
        )

        self.title = Label(
            text="",
            font_size="25sp",
            bold=True,
            color=(0.95, 0.96, 0.99, 1),
            size_hint_y=None,
            height=dp(36),
            halign="left"
        )

        self.description = Label(
            text="",
            font_size="13sp",
            color=(0.65, 0.68, 0.76, 1),
            halign="left",
            valign="top"
        )

        self.description.bind(
            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None)
            )
        )

        left.add_widget(self.category)
        left.add_widget(self.title)
        left.add_widget(self.description)

        # RIGHT

        right = BoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=dp(145),
            spacing=dp(8)
        )

        self.meta = Label(
            text="",
            font_size="11sp",
            color=(0.52, 0.56, 0.65, 1),
            halign="right",
            valign="top"
        )

        self.meta.bind(
            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None)
            )
        )

        self.learn_button = Button(
            text="Pelajari",
            size_hint_y=None,
            height=dp(40),
            background_normal="",
            background_color=(0.24, 0.34, 0.53, 1),
            color=(0.94, 0.95, 0.99, 1),
            font_size="12sp"
        )

        self.learn_button.bind(
            on_release=self.open_game
        )

        right.add_widget(self.meta)
        right.add_widget(self.learn_button)

        self.add_widget(left)
        self.add_widget(right)

    def set_game(self, game):

        self.game = game

        self.category.text = game["category"].upper()
        self.title.text = game["name"]
        self.description.text = game["description"]

        self.meta.text = (
            f"{game['players']}\n"
            f"{game['duration']}\n"
            f"{game['difficulty']}"
        )

    def open_game(self, *args):

        if self.game:

            App.get_running_app().open_game(
                self.game
            )

    def update_background(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size


# ============================================================
# GAME LIST CARD
# ============================================================

class GameListCard(BoxLayout):

    def __init__(self, game, **kwargs):

        super().__init__(**kwargs)

        self.game = game

        self.orientation = "horizontal"

        self.size_hint_y = None

        self.height = dp(92)

        self.padding = dp(18), dp(12)

        self.spacing = dp(16)

        with self.canvas.before:

            Color(
                rgba=(0.055, 0.058, 0.075, 1)
            )

            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(13)]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # ACCENT

        with self.canvas.after:

            Color(
                rgba=(0.35, 0.48, 0.75, 1)
            )

            self.accent = RoundedRectangle(
                pos=(self.x, self.y + dp(16)),
                size=(dp(3), self.height - dp(32)),
                radius=[dp(2)]
            )

        self.bind(
            pos=self.update_accent,
            size=self.update_accent
        )

        # LEFT

        left = BoxLayout(
            orientation="vertical",
            spacing=dp(2)
        )

        title = Label(
            text=game["name"],
            font_size="17sp",
            bold=True,
            color=(0.91, 0.92, 0.96, 1),
            size_hint_y=None,
            height=dp(24),
            halign="left"
        )

        category = Label(
            text=game["category"],
            font_size="11sp",
            color=(0.43, 0.53, 0.72, 1),
            size_hint_y=None,
            height=dp(18),
            halign="left"
        )

        description = Label(
            text=game["description"],
            font_size="11sp",
            color=(0.51, 0.54, 0.62, 1),
            halign="left",
            valign="top"
        )

        description.bind(
            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None)
            )
        )

        left.add_widget(title)
        left.add_widget(category)
        left.add_widget(description)

        # MIDDLE

        middle = BoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=dp(120),
            spacing=dp(2)
        )

        difficulty = Label(
            text=game["difficulty"],
            font_size="11sp",
            bold=True,
            color=(0.67, 0.70, 0.78, 1),
            size_hint_y=None,
            height=dp(20),
            halign="right"
        )

        players = Label(
            text=game["players"],
            font_size="10sp",
            color=(0.46, 0.49, 0.56, 1),
            size_hint_y=None,
            height=dp(17),
            halign="right"
        )

        duration = Label(
            text=game["duration"],
            font_size="10sp",
            color=(0.46, 0.49, 0.56, 1),
            size_hint_y=None,
            height=dp(17),
            halign="right"
        )

        middle.add_widget(difficulty)
        middle.add_widget(players)
        middle.add_widget(duration)

        # BUTTON

        button = Button(
            text="Pelajari",
            size_hint_x=None,
            width=dp(92),
            size_hint_y=None,
            height=dp(38),
            background_normal="",
            background_color=(0.075, 0.09, 0.13, 1),
            color=(0.66, 0.74, 0.88, 1),
            font_size="11sp"
        )

        button.bind(
            on_release=self.open_game
        )

        self.add_widget(left)
        self.add_widget(middle)
        self.add_widget(button)

    def update_background(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size

    def update_accent(self, *args):

        self.accent.pos = (
            self.x,
            self.y + dp(16)
        )

        self.accent.size = (
            dp(3),
            self.height - dp(32)
        )

    def open_game(self, *args):

        App.get_running_app().open_game(
            self.game
        )


# ============================================================
# MAIN SCREEN
# ============================================================

class MainScreen(Screen):

    categories = [
        "Semua",
        "Kooperatif",
        "Casino",
        "Poker",
        "Trick Taking",
        "Shedding",
        "Rummy",
        "Solo",
        "Memory",
        "Refleks",
        "Pairing",
        "Perbandingan",
        "Set Collection"
    ]

    selected_category = "Semua"
    search_text = ""

    def on_enter(self):

        self.build_featured()
        self.build_categories()
        self.refresh_games()

    # ========================================================
    # FEATURED
    # ========================================================

    def build_featured(self):

        featured_games = [
            game for game in GAMES
            if game["featured"]
        ]

        if featured_games:

            self.ids.featured_card.set_game(
                featured_games[0]
            )

    # ========================================================
    # CATEGORY
    # ========================================================

    def build_categories(self):

        container = self.ids.categories

        container.clear_widgets()

        for category in self.categories:

            selected = (
                category == self.selected_category
            )

            button = Button(
                text=category,
                size_hint=(None, None),
                size=(dp(105), dp(36)),
                background_normal="",
                background_color=(
                    (0.22, 0.31, 0.48, 1)
                    if selected
                    else (0.055, 0.058, 0.075, 1)
                ),
                color=(
                    (0.90, 0.92, 0.98, 1)
                    if selected
                    else (0.49, 0.52, 0.60, 1)
                ),
                font_size="10sp"
            )

            button.bind(
                on_release=lambda btn:
                self.select_category(
                    btn.text
                )
            )

            container.add_widget(button)

    def select_category(self, category):

        self.selected_category = category

        self.build_categories()

        self.refresh_games()

    # ========================================================
    # SEARCH
    # ========================================================

    def search_games(self, text):

        self.search_text = (
            text.lower().strip()
        )

        self.refresh_games()

    # ========================================================
    # REFRESH GAME LIST
    # ========================================================

    def refresh_games(self):

        container = self.ids.game_list

        container.clear_widgets()

        results = []

        for game in GAMES:

            text = (
                game["name"]
                + " "
                + game["category"]
                + " "
                + game["description"]
            ).lower()

            search_match = (
                self.search_text == ""
                or self.search_text in text
            )

            category_match = (
                self.selected_category == "Semua"
                or game["category"]
                == self.selected_category
            )

            if search_match and category_match:

                results.append(game)

        self.ids.result_count.text = (
            f"{len(results)} permainan"
        )

        for game in results:

            container.add_widget(
                GameListCard(game)
            )

        if not results:

            empty = Label(
                text=(
                    "Permainan tidak ditemukan.\n\n"
                    "Coba gunakan kata kunci lain."
                ),
                font_size="13sp",
                color=(0.45, 0.48, 0.56, 1),
                halign="center",
                valign="middle",
                size_hint_y=None,
                height=dp(130)
            )

            empty.bind(
                size=lambda instance, value:
                setattr(
                    instance,
                    "text_size",
                    value
                )
            )

            container.add_widget(empty)


# ============================================================
# DETAIL SCREEN
# ============================================================

class DetailScreen(Screen):

    def show_game(self, game):

        container = self.ids.detail_content

        container.clear_widgets()

        # ====================================================
        # HERO
        # ====================================================

        hero = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(150),
            spacing=dp(3)
        )

        category = Label(
            text=game["category"].upper(),
            font_size="10sp",
            bold=True,
            color=(0.45, 0.58, 0.82, 1),
            size_hint_y=None,
            height=dp(20),
            halign="left"
        )

        title = Label(
            text=game["name"],
            font_size="30sp",
            bold=True,
            color=(0.94, 0.95, 0.98, 1),
            size_hint_y=None,
            height=dp(42),
            halign="left"
        )

        description = Label(
            text=game["description"],
            font_size="14sp",
            color=(0.59, 0.63, 0.71, 1),
            halign="left",
            valign="top"
        )

        description.bind(
            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None)
            )
        )

        hero.add_widget(category)
        hero.add_widget(title)
        hero.add_widget(description)

        container.add_widget(hero)

        # ====================================================
        # INFO
        # ====================================================

        info = GridLayout(
            cols=4,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(78)
        )

        info.add_widget(
            self.create_info(
                "PEMAIN",
                game["players"]
            )
        )

        info.add_widget(
            self.create_info(
                "DURASI",
                game["duration"]
            )
        )

        info.add_widget(
            self.create_info(
                "KESULITAN",
                game["difficulty"]
            )
        )

        info.add_widget(
            self.create_info(
                "DECK",
                game["deck"]
            )
        )

        container.add_widget(info)

        # ====================================================
        # SECTIONS
        # ====================================================

        container.add_widget(
            self.create_section(
                "Tujuan",
                game["goal"]
            )
        )

        container.add_widget(
            self.create_section(
                "Persiapan",
                self.numbered_list(
                    game["setup"]
                )
            )
        )

        container.add_widget(
            self.create_section(
                "Cara Bermain",
                self.numbered_list(
                    game["rules"]
                )
            )
        )

        container.add_widget(
            self.create_section(
                "Kartu Khusus",
                self.bullet_list(
                    game["special"]
                )
            )
        )

        container.add_widget(
            self.create_section(
                "Penilaian",
                game["score"]
            )
        )

        container.add_widget(
            self.create_section(
                "Tips",
                game["tips"]
            )
        )

    # ========================================================
    # INFO BOX
    # ========================================================

    def create_info(self, title, value):

        box = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(2)
        )

        with box.canvas.before:

            Color(
                rgba=(0.055, 0.058, 0.075, 1)
            )

            bg = RoundedRectangle(
                pos=box.pos,
                size=box.size,
                radius=[dp(11)]
            )

        box.bind(
            pos=lambda instance, value:
            setattr(bg, "pos", instance.pos),
            size=lambda instance, value:
            setattr(bg, "size", instance.size)
        )

        title_label = Label(
            text=title,
            font_size="8sp",
            bold=True,
            color=(0.38, 0.42, 0.50, 1),
            size_hint_y=None,
            height=dp(17),
            halign="left"
        )

        value_label = Label(
            text=value,
            font_size="11sp",
            bold=True,
            color=(0.82, 0.84, 0.90, 1),
            halign="left",
            valign="top"
        )

        value_label.bind(
            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None)
            )
        )

        box.add_widget(title_label)
        box.add_widget(value_label)

        return box

    # ========================================================
    # SECTION
    # ========================================================

    def create_section(self, title, text):

        box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(18),
            spacing=dp(7)
        )

        with box.canvas.before:

            Color(
                rgba=(0.055, 0.058, 0.075, 1)
            )

            bg = RoundedRectangle(
                pos=box.pos,
                size=box.size,
                radius=[dp(13)]
            )

        box.bind(
            pos=lambda instance, value:
            setattr(bg, "pos", instance.pos),
            size=lambda instance, value:
            setattr(bg, "size", instance.size)
        )

        heading = Label(
            text=title,
            font_size="17sp",
            bold=True,
            color=(0.91, 0.92, 0.96, 1),
            size_hint_y=None,
            height=dp(27),
            halign="left"
        )

        content = Label(
            text=text,
            font_size="13sp",
            color=(0.61, 0.64, 0.71, 1),
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        content.bind(
            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None)
            )
        )

        def update_height(instance, value):

            box.height = (
                heading.height
                + content.height
                + dp(43)
            )

        content.bind(
            texture_size=update_height
        )

        box.add_widget(heading)
        box.add_widget(content)

        return box

    # ========================================================
    # LIST FORMAT
    # ========================================================

    def numbered_list(self, items):

        return "\n".join(
            f"{index + 1}. {item}"
            for index, item in enumerate(items)
        )

    def bullet_list(self, items):

        return "\n".join(
            f"- {item}"
            for item in items
        )


# ============================================================
# APP
# ============================================================

class CardGameApp(App):

    title = "KartuPedia"

    def build(self):

        Builder.load_string(KV)

        manager = ScreenManager()

        manager.add_widget(
            MainScreen(
                name="main"
            )
        )

        manager.add_widget(
            DetailScreen(
                name="detail"
            )
        )

        return manager

    def open_game(self, game):

        detail_screen = (
            self.root.get_screen("detail")
        )

        detail_screen.show_game(game)

        self.root.current = "detail"


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    CardGameApp().run()