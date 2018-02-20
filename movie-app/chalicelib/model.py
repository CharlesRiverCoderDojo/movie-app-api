from peewee import *
import psycopg2
import pprint
from imdb import IMDb

from chalice import BadRequestError

db = PostgresqlDatabase('movieapp', user='postgres', password='postgres')
pp = pprint.PrettyPrinter(indent=4)

class BaseModel(Model):
  class Meta:
    database = db

class Movie(BaseModel):
  ia = IMDb()
  id = PrimaryKeyField()
  movie_id = IntegerField(null = False)
  title = CharField(null = False)
  plot = TextField()
  user_id = IntegerField(null = False)

  def find_movie(self, query):
    try:
      movies = self.ia.search_movie( query )
      final = []
      for movie in movies:
        final.append({
          'title': movie.get('title'),
          'year': movie.get('year')
        })
      return(final)
    except KeyError:
      raise BadRequestError("Unknown movie '%s', please enter a different movie title" % (query))

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

  def show_popular_movies(self):
    results = Movie.select(fn.COUNT(Movie.movie_id).alias('count'), Movie.title, Movie.movie_id).group_by(Movie.movie_id, Movie.title).order_by(SQL('count').desc()).limit(10)
    final = []
    for result in results:
      final.append({
        'id': result.count,
        'title': result.title,
        'movie_id': result.movie_id,
      })
    return(final)
