from peewee import *
import psycopg2
from imdb import IMDb

db = PostgresqlDatabase('movieapp', user='postgres', password='postgres')
ia = IMDb()

class BaseModel(Model):
    class Meta:
        database = db

class Movie(BaseModel):
    id = PrimaryKeyField()
    title = CharField(null = False)
    movie_id = IntegerField(null = False)
    plot = TextField()

def create_movie(movie_name):
    movie = ia.search_movie( movie_name )
    movie_id = movie[0].movieID
    movie_obj = ia.get_movie(movie_id)

    title = movie_obj['title']
    plot = movie_obj['plot']
    Movie.create(title = title, movie_id = movie_id, plot = plot)

def delete_movie(movie_name):
    query = Movie.delete().where(Movie.title == movie_name).execute()

def show_one_movie(movie_name):
    query = Movie.select(Movie.id, Movie.title, Movie.movie_id, Movie.plot).where(Movie.title == movie_name).execute()
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
