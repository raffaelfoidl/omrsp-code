from datetime import datetime


class Movie:
    budget: float
    company: str
    country: str
    director: str
    genre: str
    gross_revenue: float
    name: str
    rating: str
    released: datetime
    runtime: int
    score: float
    star: str
    votes: int
    writer: str
    year: int

    def __init__(self, budget: str, company: str, country: str, director: str, genre: str, gross_revenue: str, name: str,
                 rating: str, released: str, runtime: str, score: str, star: str, votes: str, writer: str,
                 year: str) -> None:
        self.budget = float(budget)
        self.company = company
        self.country = country
        self.director = director
        self.genre = genre
        self.gross_revenue = float(gross_revenue)
        self.name = name
        self.rating = rating
        self.released = self._parse_date(released)
        self.runtime = int(runtime)
        self.score = float(score)
        self.star = star
        self.votes = int(votes)
        self.writer = writer
        self.year = int(year)

    @staticmethod
    def _parse_date(date_string: str) -> datetime:
        valid_formats = ["%Y-%m-%d", "%Y-%m", "%Y"]

        for current_format in valid_formats:
            try:
                return datetime.strptime(date_string, current_format)
            except ValueError:
                pass

        raise Exception(f"Could not parse date \"{date_string}\" using any of the formats {valid_formats}.")

    def __str__(self) -> str:
        return f"[{self.budget}; {self.company}; {self.country}; {self.director}; {self.genre}; {self.gross_revenue}; {self.name}; {self.rating}; " \
               f"{self.released}; {self.runtime}; {self.score}; {self.star}; {self.votes}; {self.writer}; {self.year}]"
