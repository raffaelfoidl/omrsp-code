class OscarInfo:
    """
    Bundles information about an Oscar winning or nominated movie and the award itself.
    """

    year_film: int
    """The release year of the movie."""

    year_ceremony: int
    """The year of the Oscar ceremony the movie was awarded at."""

    ceremony: int
    """The number of the Oscar ceremony."""

    category: str
    """The Oscar category the movie is nominated for."""

    name: str
    """The person directly addressed by the nomination of the movie."""

    film: str
    """The title of the movie."""

    winner: bool
    """If `True`, the movie won the award in the given category and year. If `False`, the movie was only nominated."""

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
