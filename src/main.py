import csv
import os
from typing import Iterable, List, Collection, Type, TypeVar, Callable

from src.awarded_movie import AwardedMovie
from src.movie import Movie
from src.oscar_info import OscarInfo

source_root, _ = os.path.split(__file__)
data_folder = os.path.abspath(os.path.join(source_root, "..", "data"))
result_folder = os.path.abspath(os.path.join(source_root, "..", "result"))

movie_data_file = os.path.join(data_folder, "movies.csv")
oscars_data_file = os.path.join(data_folder, "the_oscar_award.csv")
awarded_movies_result_file = os.path.join(result_folder, "awarded_movies.csv")

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
    with open(file_path, encoding=encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        return_value: List[_T] = []

        headers = next(csv_reader)
        if headers != expected_headers:
            raise Exception(f"Unexpected CSV headers. Check if '{oscars_data_file}' is the correct file.\n"
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


def read_oscar_data() -> Collection[OscarInfo]:
    """
    Parses the CSV dataset with Oscar nomination and winners from 1928 until 2020 and deserializes it into OscarInfo model instances.

    :return: Returns a collection of OscarInfo instances that represents the raw information of the Oscar award dataset.
    :rtype: Collection[OscarInfo]
    """

    def is_relevant(oscar_info: OscarInfo) -> bool:
        # we are only interested in oscar infos that represent the winners of a "Best Picture" award between 1986 and 2016 (both inclusively)
        return (1986 <= oscar_info.year_film <= 2016) and (oscar_info.category.lower() == "best picture") and (oscar_info.winner is True)

    expected_headers = ["year_film", "year_ceremony", "ceremony", "category", "name", "film", "winner"]

    return _read_csv(oscars_data_file, expected_headers, OscarInfo, is_relevant)


def read_movie_data() -> Collection[Movie]:
    """
    Parses the CSV dataset with IMDB information about movies from 1986 to 2016 and deserializes it into Movie model instances.

    :return: Returns a collection of Movie instances that represents the raw information of the IMDB movie dataset.
    :rtype: Collection[Movie]
    """

    # noinspection PyUnusedLocal
    def is_relevant(movie: Movie) -> bool:
        # all movie entries are relevant
        return True

    expected_headers = ["budget", "company", "country", "director", "genre", "gross", "name", "rating",
                        "released", "runtime", "score", "star", "votes", "writer", "year"]

    return _read_csv(movie_data_file, expected_headers, Movie, is_relevant)


def match_awarded_movies(oscar_infos: Iterable[OscarInfo], movies: Iterable[Movie]) -> Collection[AwardedMovie]:
    """
    Matches the information gathered from the Oscar dataset with the one gathered from the IMDB movie dataset. Two entries are
    defined to be "matching" if the title and year of the film described are equal in both datasets - i. e. film identity is
    defined by the name and finalization/release year.

    :param oscar_infos: relevant oscar award information to be taken into consideration for the matching
    :param movies: movie data with IMDB information (gross revenue, user score) to be matched with the oscar infos
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
            awarded_movies.append(AwardedMovie(oscar_info.year_film, oscar_info.film, matched_movie.score, matched_movie.gross))
        else:
            print(f"Could not find match for film \"{oscar_info.film}\" ({oscar_info.year_film}).")

    return awarded_movies


def write_awarded_movies_to_file(awarded_movies: Iterable[AwardedMovie]) -> None:
    """
    Creates a CSV file with in the local result folder that contains all movies that could be matched. More precisely,
    the CSV file will contain the name, IMDB score, gross revenue in the USA of all films that have been awarded the
    Oscar in the category "Best Picture" from 1986 to 2016 (both inclusively).

    :param awarded_movies: the movies that were matched successfully  between the two datasets (Oscar awards, IMDB data)
    :rtype: None
    """
    with open(awarded_movies_result_file, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["year", "movie", "score", "gross"])  # header row
        csv_rows = map(lambda movie: movie.serialize(), awarded_movies)
        csv_writer.writerows(csv_rows)


if __name__ == '__main__':
    oscar_data: Collection[OscarInfo] = read_oscar_data()
    print(f"Filtered {len(oscar_data)} oscar information entries.")

    movie_data: Collection[Movie] = read_movie_data()
    print(f"Read {len(movie_data)} movie information entries.")

    matched_movies: Collection[AwardedMovie] = match_awarded_movies(oscar_data, movie_data)
    print(f"Matched {len(matched_movies)} movies with awards.")

    write_awarded_movies_to_file(matched_movies)
    print(f"Wrote to file {awarded_movies_result_file}.")
