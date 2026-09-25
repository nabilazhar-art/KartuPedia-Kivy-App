"""Model data: representasi satu permainan kartu."""


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
        self.tutorial_youtube_id = data.get("tutorial_youtube_id", "")

    @property
    def tutorial_url(self):
        """Link YouTube lengkap untuk video tutorial (kosong kalau tidak ada)."""
        if not self.tutorial_youtube_id:
            return ""
        return f"https://youtu.be/{self.tutorial_youtube_id}"

    @property
    def tutorial_thumbnail_url(self):
        """URL thumbnail video (dari CDN img.youtube.com, kosong kalau tidak ada video)."""
        if not self.tutorial_youtube_id:
            return ""
        return f"https://img.youtube.com/vi/{self.tutorial_youtube_id}/hqdefault.jpg"

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
