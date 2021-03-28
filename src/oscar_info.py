class OscarInfo:
    year_film: int
    year_ceremony: int
    ceremony: int
    category: str
    name: str
    film: str
    winner: bool

    def __init__(self, year_film: str, year_ceremony: str, ceremony: str, category: str, name: str, film: str,
                 winner: str) -> None:
        self.year_film = int(year_film)
        self.year_ceremony = int(year_ceremony)
        self.ceremony = int(ceremony)
        self.category = category
        self.name = name
        self.film = film
        self.winner = winner.lower() == "true"

    def __str__(self) -> str:
        return f"[{self.year_film}; {self.year_ceremony}; {self.ceremony}; {self.category}; {self.name}; {self.film}; {self.winner}]"
