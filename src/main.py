import os
import re
from multiprocessing.pool import Pool

import imdb


MIN_RATING = 6.0

ia = imdb.IMDb()


def get_directory_list():
    for (_, dirnames, _) in os.walk('.'):
        return dirnames


def parse_filename(name: str):
    pattern = re.compile(r'(.*?) \((\d{4})\)')
    result = pattern.match(name)
    if result is None:
        raise Exception
    title, year = result.groups()
    return (title, int(year))


def get_film_rating(title, year) -> float:
    imdb_movie_results = [movie for movie in ia.search_movie(title)
                          if 'year' in movie and movie['year'] == year]
    if not imdb_movie_results:
        raise Exception

    movie = ia.get_movie(imdb_movie_results[0].getID())

    if 'rating' not in movie:
        raise Exception

    return float(movie['rating'])


def process_directory(directory):
    try:
        title, year = parse_filename(directory)
        rating = get_film_rating(title, year)
        print(f'{title} {rating}')
    except Exception:
        rating = 0.0
        print(f'{directory} [Error]')
    return (directory, rating)


def save_data(data):
    with open('bad_movies.txt', 'w') as ptr:
        ptr.write('\n'.join(data))


def main():
    directory_list = get_directory_list()

    with Pool(5) as p:
        results = p.map(process_directory, directory_list)

    bad_movies = [",".join([directory, str(rating)]) for directory, rating in results
                  if rating < MIN_RATING]
    save_data(bad_movies)


if __name__ == '__main__':
    main()
