import os
from peewee import *
import psycopg2
import pprint
import omdb

omdb.set_default('apikey', 'bdcbcc1')
# from imdb import IMDb

from chalice import BadRequestError

pp = pprint.PrettyPrinter(indent=4)

class BaseModel(Model):
  class Meta:
    database = db

class Movie(BaseModel):
  # ia = IMDb()
  id = PrimaryKeyField()
  movie_id = CharField(null = False)
  title = CharField(null = False)
  plot = TextField()
  user_id = IntegerField(null = False)

  def find_movie(self, query):
    try:
      movies = omdb.search_movie(query)
      final = []
      for movie in movies:
        final.append({
          'title': movie.get('title'),
          'year': movie.get('year'),
          'imdb_id': movie.get('imdb_id')
        })
      return(final)
    except KeyError:
      raise BadRequestError("Unknown movie '%s', please enter a different movie title" % (query))

  def create_movie(self, movie_id, user_id):
    movie = omdb.imdbid(movie_id)
    Movie.create(title = movie['title'], movie_id = movie['imdb_id'], plot = movie['plot'], user_id = user_id)

  def delete_movie(self, movie_id, user_id):
    query = Movie.delete().where(Movie.movie_id == str(movie_id), Movie.user_id == int(user_id)).execute()

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

db.connect()
db.create_tables([Movie], safe = True)

m = Movie()
# print(m.create_movie('tt0133093', 5))
print(m.show_popular_movies())
