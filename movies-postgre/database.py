import os
import datetime
import psycopg2

from dotenv import load_dotenv

load_dotenv()

# Creating Queries...

CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

CREATE_USER_TABLE = """CREATE TABLE IF NOT EXISTS users (
    user_name TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(user_name),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
INSERT_USER = "INSERT INTO users (user_name) VALUES (%s);"
DELETE_MOVIE = "DELETE FROM movies WHERE title = %s;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
SELECT_WATCHED_MOVIES = """
SELECT movies.id, movies.title, movies.release_timestamp
FROM movies
JOIN watched ON movies.id = watched.movie_id
JOIN users ON watched.user_username = users.user_name
WHERE users.user_name = %s;
"""
INSERT_WATCHED_MOVIES = "INSERT INTO watched (user_username, movie_id) VALUES(%s, %s);"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 WHERE title = %s;"
SEARCH_MOVIES = " SELECT * FROM movies WHERE title LIKE %s;"
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"

connection = psycopg2.connect(os.environ["DATABASE_URL"])


# Creating functions...

def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USER_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            cursor.execute(CREATE_RELEASE_INDEX)


def add_user(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username, ))


def add_movie(title, release_timestamp):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIE, (title, release_timestamp))


def get_movies(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,)) #take care of the tupple
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def search_movies(search_str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIES, (f"%{search_str}%", ))
            return cursor.fetchall()


def watch_movie(watcher_name, movie_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIES, (watcher_name, movie_id))


def get_watched_movies(watcher_name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (watcher_name, ))
            return cursor.fetchall()
