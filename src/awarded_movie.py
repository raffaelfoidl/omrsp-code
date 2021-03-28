class AwardedMovie:
    year: int
    movie: str
    score: float
    gross: float

    def __init__(self, year: int, movie: str, score: float, gross: float) -> None:
        self.year = year
        self.movie = movie
        self.score = score
        self.gross = gross

    def __str__(self) -> str:
        return f"[{self.year}, {self.movie}, {self.score}, {self.gross}]"

    def serialize(self):
        return [self.year, self.movie, self.score, self.gross]
