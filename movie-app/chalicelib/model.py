from peewee import *
import psycopg2
import pprint
from imdb import IMDb

db = PostgresqlDatabase('movieapp', user='postgres', password='postgres')
pp = pprint.PrettyPrinter(indent=4)

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
        movies = self.ia.search_movie( query )
        # pp.pprint(movies)
        final = []
        for movie in movies:
          # print("Hello", movie)
          # pp.pprint(movie['year'] || '')
          final.append({
            'title': movie.get('title'),
            'year': movie.get('year')
          })
        return(final)

    def create_movie(self, movie_name, user_id):
        movie = self.ia.search_movie( movie_name )
        self.movie_id = movie[0].movieID
        movie_obj = self.ia.get_movie(self.movie_id)

        title = movie_obj['title']
        plot = movie_obj['plot']
        Movie.create(title = title, movie_id = movie_id, plot = plot, user_id = user_id)

    def delete_movie(self, movie_id, user_id):
        query = Movie.delete().where(Movie.movie_id == int(movie_id), Movie.user_id == int(user_id)).execute()

    def show_all_movies(self, user_id):
        # query = Movie.select()
        results = Movie.select(Movie.id, Movie.title, Movie.movie_id, Movie.plot).where(Movie.user_id == user_id)
        final = []
        for result in results:
            final.append({
                'id': result.id,
                'title': result.title,
                'movie_id': result.movie_id,
                'plot': result.plot
            })
        return(final)

m = Movie()
m.find_movie("Footloose")
