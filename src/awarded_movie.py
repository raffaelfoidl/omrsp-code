class AwardedMovie:
    year: int
    movie: str
    score: float
    gross_revenue: float

    def __init__(self, year: int, movie: str, score: float, gross_revenue: float) -> None:
        self.year = year
        self.movie = movie
        self.score = score
        self.gross_revenue = gross_revenue

    def __str__(self) -> str:
        return f"[{self.year}, {self.movie}, {self.score}, {self.gross_revenue}]"

    def serialize(self):
        return [self.year, self.movie, self.score, self.gross_revenue]
