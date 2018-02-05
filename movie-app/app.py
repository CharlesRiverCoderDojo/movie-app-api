from chalice import Chalice
from chalicelib.model import db

app = Chalice(app_name='movie-app')
app.debug = True

@app.route('/')
def index():
    return {'stuff': 'worthingld'}

def main():
    db.connect()
    db.create_tables([Movie], safe = True)
    # create_movie("Evita")
    # delete_movie("A League of Their Own")
    # show_one_movie("The Matrix")
    # show_all_movies()

if __name__ == '__main__':
    main()
