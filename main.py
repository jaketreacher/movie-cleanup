import os
import re
import imdb
from multiprocessing.pool import Pool

THRESHOLD = 6.0
PROG = re.compile(r'(.*?) \((\d{4})\)')
ia = imdb.IMDb()


class MovieNotFound(Exception):
    pass


class MovieHasNoRating(Exception):
    pass


def get_directory_list():
    for (dirpath, dirnames, filenames) in os.walk('.'):
        return dirnames


def parse_filename(name):
    title, year = PROG.match(name).groups()
    return (title, int(year))


def get_film_rating(title, year):
    movie_list = [movie for movie in ia.search_movie(title) if 'year' in movie and movie['year'] == year]
    if not movie_list:
        raise MovieNotFound
    movie = ia.get_movie(movie_list[0].getID())
    if 'rating' not in movie:
        raise MovieHasNoRating
    return movie['rating']


def process_directory(directory):
    title, year = parse_filename(directory)
    try:
        rating = get_film_rating(title, year)
        print(f'{title} {rating}')
    except (MovieNotFound, MovieHasNoRating):
        rating = 0.0
        print(f'{title} [Error]')
    return (directory, rating)


def save_data(data):
    with open('bad_movies.txt', 'w') as ptr:
        ptr.writelines(data)


def main():
    directory_list = get_directory_list()
    bad_movies = []
    with Pool(5) as p:
        results = p.map(process_directory, directory_list)
    bad_movies = [directory for directory, rating in results if rating < THRESHOLD]
    save_data(bad_movies)


if __name__ == '__main__':
    main()
