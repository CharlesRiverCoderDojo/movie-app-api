from peewee import *
import psycopg2
from imdb import IMDb

db = PostgresqlDatabase('movieapp', user='postgres', password='postgres')

class BaseModel(Model):
    class Meta:
        database = db

class Movie(BaseModel):
    # def __init__(self):
    #     print ("in init")
    ia = IMDb()
    id = PrimaryKeyField()
    movie_id = IntegerField(null = False)
    title = CharField(null = False)
    plot = TextField()
    user_id = IntegerField(null = False)

    def find_movie(self, query):
        movie = self.ia.search_movie( query )
        print(movie)

    def create_movie(self, movie_name, user_id):
        movie = self.ia.search_movie( movie_name )
        self.movie_id = movie[0].movieID
        movie_obj = self.ia.get_movie(self.movie_id)

        self.title = movie_obj['title']
        self.plot = movie_obj['plot']
        Movie.create(title = self.title, movie_id = self.movie_id, plot = self.plot, user_id = user_id)

    def delete_movie(self, movie_name):
        query = Movie.delete().where(Movie.title == movie_name).execute()

    # def show_one_movie(self, movie_name):
    #     query = Movie.select(Movie.id, Movie.title, Movie.movie_id, Movie.plot).where(Movie.title == movie_name).execute()
    #     print(query)

    def show_all_movies():
        query = Movie.select(Movie.id, Movie.title, Movie.movie_id, Movie.plot).execute()
        print(query)
