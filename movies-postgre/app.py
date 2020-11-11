import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Add user to the app.
7) Search for a movie.
8) Exit

Your selection: """
welcome = "Welcome to the watchlist app!"


print(welcome)
database.create_tables()

# creating functions'''


def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")

    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)


def print_movies_list(heading, movies):
    print(f"--{heading} movies--")
    for _id, title, release_date in movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        human_date = movie_date.strftime("%b %d %Y")
        print(f"{_id}: {title} (on- {human_date})")
    print("---- \n")


def prompt_watch_movie():
    username = input("Username: ")
    movie_id = input("Movie ID: ")
    database.watch_movie(username, movie_id)


def prompt_show_watched_movies():
    username = input("Username: ")
    movies = database.get_watched_movies(username)
    if movies:
        print_movies_list(f"{username}'s watched", movies)
    else:
        print(f"{username} has watched no movies")    


def prompt_search_movie():
    term = input("Enter the partial movie title: ")
    movies_list = database.search_movies(term)
    print_movies_list("Founded", movies_list)


# Start program...
    

while (user_input := input(menu)) != "8":
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        movies = database.get_movies(True)
        print_movies_list("Upcomming", movies)
    elif user_input == "3":
        movies = database.get_movies()
        print_movies_list("All", movies)
    elif user_input == "4":
        prompt_watch_movie()
    elif user_input == "5":
        prompt_show_watched_movies()       
    elif user_input == "6":
        username = input("Username: ")
        database.add_user(username)
    elif user_input == '7':
        prompt_search_movie()
    else:
        print("Invalid input, please try again!")
