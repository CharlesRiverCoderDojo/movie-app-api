from chalice import Chalice
from chalicelib.model import db
from chalicelib.model import Movie
import string

from chalice import BadRequestError

app = Chalice(app_name='movie-app')
app.debug = True

@app.route('/movies/{search}', methods=['GET'])
def find_movie(search):
  if len(search) >= 3:
    try:
      # still need to add search for substring - this only works to find a specific movie
      m = Movie()
      search_string = search.replace("_", " ").title()
      m.find_movie(search_string)
      # return {"search": search_string}
    except KeyError:
      raise BadRequestError("Unknown city movie")

@app.route('/user/{user_id}/{movie_title}', methods=['POST', 'DELETE'])
def add_or_delete_movie(movie_title, user_id):
  request = app.current_request
  if len(movie_title) <= 3:
    raise BadRequestError("Unknown city movie")
  if request.method == 'POST':
    m = Movie()
    search_string = movie_title.replace("_", " ").title()
    m.create_movie(search_string, user_id)
    return {"search": search_string, "user": user_id}
  elif request.method == 'DELETE':
    m = Movie()
    search_string = movie_title.replace("_", " ").title()
    m.delete_movie(search_string, user_id)
    return {"deleted": search_string}

# @app.route('user/movies')

def main():
  db.connect()
  db.create_tables([Movie], safe = True)

if __name__ == '__main__':
  main()
