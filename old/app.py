from chalice import Chalice
from peewee import *
import psycopg2
from imdb import IMDb

app = Chalice(app_name='movie-app')
db = PostgresqlDatabase('movieapp', user='postgres', password='postgres')
ia = IMDb()

class BaseModel(Model):
    class Meta:
        database = db

class Movie(BaseModel):
    id = PrimaryKeyField()
    movie_id = IntegerField(null = False)
    title = CharField(null = False)
    plot = TextField()

def create_movie(movie_name):
    movie = ia.search_movie( movie_name )
    # error message if nothing found
    movie_id = movie[0].movieID
    movie_obj = ia.get_movie(movie_id)

    title = movie_obj['title']
    plot = movie_obj['plot']
    Movie.create(title = title, movie_id = movie_id, plot = plot)

def delete_movie(movie_name):
    query = Movie.delete().where(Movie.title == movie_name).execute()

def show_one_movie(movie_name):
    query = Movie.select(Movie.id, Movie.title, Movie.movie_id, Movie.plot).where(Movie.title == movie_name).execute()
    # Can you just return Movie.where? and get the entire object?
    print(query)

def show_all_movies():
    query = Movie.select(Movie.id, Movie.title, Movie.movie_id, Movie.plot).execute()
    print(query)

def main():
    db.connect()
    db.create_tables([Movie], safe = True)
    create_movie("Evita")
    # delete_movie("A League of Their Own")
    # show_one_movie("The Matrix")
    # show_all_movies()

if __name__ == '__main__':
    main()


@app.route('/')
def index():
    return {'hello': 'world'}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
