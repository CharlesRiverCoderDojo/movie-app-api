from peewee import *
import psycopg2
from imdb import IMDb

db = PostgresqlDatabase('movieapp', user='postgres', password='postgres')

class BaseModel(Model):
    class Meta:
        database = db

class Movie(BaseModel):
    ia = IMDb()
    id = PrimaryKeyField()
    movie_id = IntegerField(null = False)
    title = CharField(null = False)
    plot = TextField()

    def create_movie(self, movie_name):
        movie = self.ia.search_movie( movie_name )
        self.movie_id = movie[0].movieID
        movie_obj = self.ia.get_movie(movie_id)

        title = movie_obj['title']
        plot = movie_obj['plot']
        Movie.create(title = title, movie_id = movie_id, plot = plot)

    def delete_movie(self, movie_name):
        query = Movie.delete().where(Movie.title == movie_name).execute()

    def show_one_movie(self, movie_name):
        query = Movie.select(Movie.id, Movie.title, Movie.movie_id, Movie.plot).where(Movie.title == movie_name).execute()
        print(query)

    def show_all_movies():
        query = Movie.select(Movie.id, Movie.title, Movie.movie_id, Movie.plot).execute()
        print(query)
