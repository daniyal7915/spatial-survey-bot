import os
import psycopg2
from engine.utils.utils import credentials


class Tables:
    cred = credentials(os.environ['DATABASE_URL'])
    connection = psycopg2.connect(database=cred['NAME'], user=cred['USER'], password=cred['PASSWORD'],
                                  host=cred['HOST'], port=cred['PORT'])
    cursor = connection.cursor()

    def __init__(self, db=''):
        self.db = db

    def create(self):
        self.cursor.execute(f"create table if not exists {self.db}user_state (user_id int PRIMARY KEY, user_name text, "
                            f"user_state int, survey text)")
        self.cursor.execute(f"create table if not exists {self.db}features (id serial PRIMARY KEY, user_id int, "
                            f"user_name text, survey text, entr_time timestamp, photo text, video text, "
                            f"point geometry(POINT, 4326), polygon geometry(POLYGON, 4326), poly_points text, "
                            f"q_count int, ans_check int)")
        self.cursor.execute(f"create table if not exists {self.db}questions (id serial PRIMARY KEY, survey text, "
                            f"author int, question text)")
        self.cursor.execute(f"create table if not exists {self.db}answers (id serial PRIMARY KEY, f_id int, "
                            f"q_id int, answer text)")
        self.connection.commit()

    def drop(self):
        self.cursor.execute(f"drop table if exists {self.db}user_state")
        self.cursor.execute(f"drop table if exists {self.db}features")
        self.cursor.execute(f"drop table if exists {self.db}questions")
        self.cursor.execute(f"drop table if exists {self.db}answers")
        self.connection.commit()