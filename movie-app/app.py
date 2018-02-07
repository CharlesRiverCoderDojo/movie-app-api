from chalice import Chalice
from chalicelib.model import db
from chalicelib.model import Movie
import string

from chalice import BadRequestError
# add error handling to return true or false (can put in the model)

app = Chalice(app_name='movie-app')
app.debug = True

m = Movie()

# @app.route('/movies/{search}', methods=['GET'])
# def find_movie(search):
#   if len(search) >= 3:
#     try:
#       # still need to add search for substring - this only works to find a specific movie
#       m = Movie()
#       search_string = search.replace("_", " ").title()
#       m.find_movie(search_string)
#       # return {"search": search_string}
#     except KeyError:
#       raise BadRequestError("Unknown city movie")

# create one movie for a user
@app.route('/user/{user_id}/movie', methods=['POST'])
def add_movie(user_id):
  request = app.current_request
  movie_title = request.json_body['movie_title']
  if len(movie_title) <= 3:
    raise BadRequestError("Unknown city movie")
  m.create_movie(movie_title, user_id)
  return {"search": movie_title, "user": user_id}

# delete one movie for a user
@app.route('/user/{user_id}/{movie_id}', methods=['DELETE'])
def delete_movie(movie_id, user_id):
  m.delete_movie(movie_id, user_id)
  return {"deleted": movie_id}

@app.route('/user/{user_id}/movies', methods=['GET'])
def get_all_movies(user_id):
 r = m.show_all_movies(user_id)
 return(r)

def main():
  db.connect()
  db.create_tables([Movie], safe = True)

if __name__ == '__main__':
  main()
