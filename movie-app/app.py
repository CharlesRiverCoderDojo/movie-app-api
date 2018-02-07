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

@app.route('/movies/{user_id}/{search}', methods=['GET'])
def add_movie(search, user_id):
  if len(search) >= 3:
    try:
      # still need to add search for substring - this only works to find a specific movie
      m = Movie()
      search_string = search.replace("_", " ").title()
      m.create_movie(search_string, user_id)
      return {"search": search_string, "user": user_id}
    except KeyError:
      raise BadRequestError("Unknown city movie")

@app.route('/my_movies/{name}', methods=['DELETE'])
def delete_movie(name):
  return "stuff"
    # request = app.current_request

def main():
  db.connect()
  db.create_tables([Movie], safe = True)
    # create_movie("Evita")
    # delete_movie("A League of Their Own")
    # show_one_movie("The Matrix")
    # show_all_movies()

if __name__ == '__main__':
  main()
