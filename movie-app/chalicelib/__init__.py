# from peewee import *
# import psycopg2
#
# db = PostgresqlDatabase('movieapp', user='postgres', password='postgres')
#
# class BaseModel(Model):
#     class Meta:
#         database = db
#
# def main():
#     db.connect()
#     db.create_tables([Movie], safe = True)
#     # create_movie("Evita")
#     # delete_movie("A League of Their Own")
#     # show_one_movie("The Matrix")
#     # show_all_movies()
#
# if __name__ == '__main__':
#     main()
