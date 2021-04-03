from typing import List


class AwardedMovie:
    """
    Represents an instance of output data, i. e. one result row. It juxtaposes the revenue and IMDb score of a "Best Picture" winning movie
    from a specific year.
    """

    year: int
    """The release year of the movie."""

    movie: str
    """The title of the movie."""

    score: float
    """The IMDb user score of the movie."""

    gross_revenue: float
    """The gross revenue the movie generated in the USA."""

    def __init__(self, year: int, movie: str, score: float, gross_revenue: float) -> None:
        self.year = year
        self.movie = movie
        self.score = score
        self.gross_revenue = gross_revenue

    def __str__(self) -> str:
        return f"[{self.year}, {self.movie}, {self.score}, {self.gross_revenue}]"

    def serialize(self) -> List:
        """
        Creates a list containing the attribute values of this `AwardedMovie` instance in the order it should be serialized to a file.

        **returns:** A list in the form `[year, movie, score, gross_revenue]`
        **return type:** `List`
        """
        return [self.year, self.movie, self.score, self.gross_revenue]
