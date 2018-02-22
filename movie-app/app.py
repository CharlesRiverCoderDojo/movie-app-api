from chalice import Chalice
from chalicelib.model import db
from chalicelib.model import Movie
import string

app = Chalice(app_name='movie-app')
app.debug = True

m = Movie()

# query to find movie titles that match string
@app.route('/movies', methods=['GET'], cors=True)
def find_movie():
  request = app.current_request
  q = request.query_params['q']
  movie = m.find_movie(q)
  return(movie)

# create one movie for a user
@app.route('/user/{user_id}/movie', methods=['POST'], cors=True)
def add_movie(user_id):
  request = app.current_request
  movie_id = request.json_body['imdbid']
  if movie_id is None:
    raise BadRequestError("Unknown movie")
  m.create_movie(movie_id, user_id)
  return {"search": movie_id, "user": user_id}

# delete one movie for a user
@app.route('/user/{user_id}/{movie_id}', methods=['DELETE'], cors=True)
def delete_movie(movie_id, user_id):
  m.delete_movie(movie_id, user_id)
  return {"deleted": movie_id}

# get all movies for a given user
@app.route('/user/{user_id}/movies', methods=['GET'], cors=True)
def get_all_movies(user_id):
 r = m.show_all_movies(user_id)
 return(r)

# get popular movies ranked by number of times saved in database, irrespective of user
@app.route('/popular-movies', methods=['GET'], cors=True)
def get_popular_movies():
  p = m.show_popular_movies()
  return(p)
