import csv
import math
import os

from awarded_movie import AwardedMovie
from movie import Movie
from oscar_info import OscarInfo

import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

from pathlib import Path
from typing import Iterable, List, Collection, Type, TypeVar, Callable

source_root, _ = os.path.split(__file__)
data_folder = os.path.abspath(os.path.join(source_root, "..", "data"))
result_folder = os.path.abspath(os.path.join(source_root, "..", "result"))

movie_data_file = os.path.join(data_folder, "movies.csv")
oscars_data_file = os.path.join(data_folder, "the_oscar_award.csv")
awarded_movies_result_file = os.path.join(result_folder, "awarded_movies.csv")
awarded_movies_visualization_file = os.path.join(result_folder, "awarded_movies_visualization.png")

_T = TypeVar('_T')


def _read_csv(file_path: str, expected_headers: Iterable[str], target_type: Type[_T], predicate: Callable[[_T], bool],
              encoding="utf-8", delimiter=",") -> Collection[_T]:
    """
    Generic function to deserialize a CSV file into a collection of instances of a specifiable model class. The model class
    has to provide a constructor that accepts string parameters representing the columns of a row in the CSV file.

    :param file_path: the file path to the CSV file to be read
    :param expected_headers: The headers the CSV file is expected to exhibit. If diverging headers are encountered,
     an exception with information about the headers that were found in the file is thrown.
    :param target_type: The type (i. e. class) into which CSV entries are deserialized. The class is expected to provide a constructor
    that takes the columns' values as string arguments and constructs an instance from them. If such a constructor is not available, a
    runtime error will ensue. If the constructor invocation itself fails - e. g. due to a string -> int parsing error - a warning is
    printed to stdout and the corresponding row is skipped, i. e. execution continues normally.
    :param predicate: A row entry read from the CSV is added to the return value only if the predicate, invoked with the deserialized
    model instance as argument, evaluates to true.
    :param encoding: The encoding to be used when reading the file.
    :param delimiter: a one-character string to be used as the column separator
    :return: Returns a collection of instances of the generic type parameter that were successfully deserialized from the specified
    CSV file and also satisfied the given predicate.
    :rtype: Collection[_T]
    """
    try:
        with open(file_path, encoding=encoding) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            return_value: List[_T] = []

            headers = next(csv_reader)
            if headers != expected_headers:
                raise Exception(f"Unexpected CSV headers. Check if '{file_path}' is the correct file.\n"
                                f"Expected: {expected_headers}\nActual:   {headers}")

            for row in csv_reader:
                try:
                    # as per the precondition formulated in the documentation, the model classes provide constructors that
                    # take the string value of each column as parameters and try to parse them into the correct data types
                    new_entry: _T = target_type(*row)
                except Exception as ex:
                    print(f"Skipping entry {row} because it cannot be deserialized.\n  Error: {ex}")

                if predicate(new_entry):
                    return_value.append(new_entry)

            return return_value
    except FileNotFoundError as ex:
        print(f"Could not read CSV file at \"{file_path}\".\n  Error: {ex}")
        print(f"Aborting because the experiment cannot be conducted if at least one data set cannot be read.")
        exit(1)


def read_oscar_data() -> Collection[OscarInfo]:
    """
    Parses the CSV dataset with Oscar nomination and winners from 1928 until 2020, applies a filter by year and category and deserializes the
    entries satisfying the criteria into OscarInfo model instances.

    :return: Returns a collection of OscarInfo instances that represents information from the Oscar award dataset describing Oscar winners between
    1986 and 2016 (both inclusively) from the category "Best Picture".
    :rtype: Collection[OscarInfo]
    """

    def is_relevant(oscar_info: OscarInfo) -> bool:
        # we are only interested in oscar infos that represent the winners of a "Best Picture" award between 1986 and 2016 (both inclusively)
        return (1986 <= oscar_info.year_film <= 2016) and (oscar_info.category.lower() == "best picture") and (oscar_info.winner is True)

    expected_headers = ["year_film", "year_ceremony", "ceremony", "category", "name", "film", "winner"]

    return _read_csv(oscars_data_file, expected_headers, OscarInfo, is_relevant)


def read_movie_data() -> Collection[Movie]:
    """
    Parses the CSV dataset with IMDb information about movies from 1986 to 2016 and deserializes it into Movie model instances.

    :return: Returns a collection of Movie instances that represents the raw information of the IMDb movie dataset.
    :rtype: Collection[Movie]
    """

    def is_relevant(_: Movie) -> bool:
        # all movie entries are relevant
        return True

    expected_headers = ["budget", "company", "country", "director", "genre", "gross", "name", "rating",
                        "released", "runtime", "score", "star", "votes", "writer", "year"]

    return _read_csv(movie_data_file, expected_headers, Movie, is_relevant)


def match_awarded_movies(oscar_infos: Iterable[OscarInfo], movies: Iterable[Movie]) -> Collection[AwardedMovie]:
    """
    Matches the information gathered from the Oscar dataset with the one gathered from the IMDb movie dataset. Two entries are
    defined to be "matching" if the title and year of the film described are equal in both datasets - i. e. film identity is
    defined by the name and finalization/release year.

    :param oscar_infos: relevant oscar award information to be taken into consideration for the matching
    :param movies: movie data with IMDb information (gross revenue, user score) to be matched with the oscar infos
    :return: Returns a collection of AwardedMovie model instances that represents the processed data gathered by means of the matching.
    :rtype: Collection[AwardedMovie]
    """
    awarded_movies: List[AwardedMovie] = []

    for oscar_info in oscar_infos:
        def is_match(movie: Movie):
            # we consider a movie equal if the name and year are equal
            return (oscar_info.film.lower() == movie.name.lower()) and (oscar_info.year_film in [movie.year, movie.released.year])

        matched_movie: Movie = next(filter(is_match, movies), None)
        if matched_movie is not None:
            awarded_movies.append(AwardedMovie(oscar_info.year_film, oscar_info.film, matched_movie.score, matched_movie.gross_revenue))
        else:
            print(f"Could not find match for film \"{oscar_info.film}\" ({oscar_info.year_film}).")

    return awarded_movies


def write_awarded_movies_to_file(awarded_movies: Iterable[AwardedMovie]) -> None:
    """
    Creates a CSV file within the local result folder that contains all movies that could be matched. More precisely,
    the CSV file will contain the name, IMDb score, gross revenue in the USA of all films that have been awarded the
    Oscar in the category "Best Picture" from 1986 to 2016 (both inclusively).

    :param awarded_movies: the movies that were matched successfully between the two datasets (Oscar awards, IMDb data)
    :rtype: None
    """
    with open(awarded_movies_result_file, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["year", "movie", "score", "gross_revenue"])  # header row
        csv_rows = map(lambda movie: movie.serialize(), awarded_movies)
        csv_writer.writerows(csv_rows)


def visualize_awarded_movies(awarded_movies: Iterable[AwardedMovie]) -> None:
    """
    Creates a PNG image within the local result folder that represents a visualization of the output of the data processing.
    It is a plot that juxtaposes the gross revenue of all movies that won the Best Picture Oscar between 1986 and 2016 along
    with their respective IMDb user score.

    :param awarded_movies: the movies that were matched successfully between the two datasets (Oscar awards, IMDb data)
    :rtype: None
    """

    def label_in_millions(value, _):
        return f'{value * 1e-6:1.0f} M'

    def next_hundred_million(value):
        return math.ceil(value / 100_000_000) * 100_000_000

    # prepare data: year and film on the x-axis, gross revenue and IMDb user score on the y-axes
    x_labels = np.array(list(map(lambda movie: f"{movie.year}: {movie.movie}", awarded_movies)))
    y_values_revenue = np.array(list(map(lambda movie: movie.gross_revenue, awarded_movies)))
    y_values_score = np.array(list(map(lambda movie: movie.score, awarded_movies)))

    # general plot setup
    fig, ax1 = plt.subplots(figsize=(10, 10))
    plt.xticks(rotation=270)
    plt.suptitle("Gross Revenue vs. IMDb Score of Oscar Best Picture Winners\n(1986-2016)", fontsize=16, weight="bold")
    millions_formatter = ticker.FuncFormatter(label_in_millions)

    # x-axis: display all years and movies
    ax1.set_xlabel('Oscar Years and Films', weight="bold", labelpad=5)
    ax1.xaxis.set_major_locator(ticker.FixedLocator(x_labels))
    ax1.set_xticks(np.arange(len(x_labels)))
    ax1.set_xticklabels(x_labels)

    # first y-axis: display gross revenue in millions
    ax1.set_ylabel('Gross Revenue in the USA\n(in Millions)', weight="bold", labelpad=10)
    ax1.set_ylim([0, next_hundred_million(max(y_values_revenue))])  # so that the highest y-value is not "glued" to the top of the diagram
    ax1.yaxis.set_major_formatter(millions_formatter)  # so that numbers representing axis labels are not too big
    ax1.plot(x_labels, y_values_revenue, color='tab:green', marker=".")

    # second y-axis: display IMDb user score
    ax2 = ax1.twinx()  # the second y-axis should share the x-axis with the first y-axis
    ax2.set_ylabel('IMDb User Score', weight="bold", labelpad=7)
    ax2.set_ylim([0, 10])
    ax2.yaxis.set_major_locator(ticker.FixedLocator(np.arange(0, 11)))  # display all numbers between 0 and 10
    ax2.plot(x_labels, y_values_score, color='tab:blue', marker=".")

    fig.tight_layout()
    fig.savefig(awarded_movies_visualization_file)


if __name__ == '__main__':
    print(f"Ensuring result directory \"{result_folder}\" exists...", end="")
    Path(result_folder).mkdir(parents=True, exist_ok=True)
    print("Done.")

    oscar_data: Collection[OscarInfo] = read_oscar_data()
    print(f"Filtered {len(oscar_data)} oscar information entries from \"{oscars_data_file}\".")

    movie_data: Collection[Movie] = read_movie_data()
    print(f"Read {len(movie_data)} movie information entries from \"{movie_data_file}\".")

    matched_movies: Collection[AwardedMovie] = match_awarded_movies(oscar_data, movie_data)
    print(f"Matched {len(matched_movies)} movies with awards.")

    write_awarded_movies_to_file(matched_movies)
    print(f"Wrote result of data processing to file \"{awarded_movies_result_file}\".")

    visualize_awarded_movies(matched_movies)
    print(f"Saved plot of processed data to file \"{awarded_movies_visualization_file}\".")
