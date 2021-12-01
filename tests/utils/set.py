from engine.utils.tables import Tables
from tests.utils.utils import Message


# The database connection in the testing mode
tables = Tables('test_')
connection = tables.connection
cursor = tables.cursor


class SetTestData(Message):
    """Fill up test tables with data required
       for testing in test_process.py"""
    user_id = 0
    survey = None

    def set_questions(self):
        cursor.execute(f"insert into test_questions (id, survey, author, question) values (default, {self.survey}, "
                       f"{self.user_id}, 'question{self.user_id}_1')")
        cursor.execute(f"insert into test_questions (id, survey, author, question) values (default, {self.survey}, "
                       f"{self.user_id}, 'question{self.user_id}_2')")
        connection.commit()

    def set_features_answers(self):
        user_id = [self.user_id, self.user_id, self.user_id + 1, self.user_id + 2]
        user_name = [f'Name{user_id[0]}', f'Name{user_id[1]}', f'Name{user_id[2]}', f'Name{user_id[3]}']
        time = '2021-11-20 22:45:00'
        photo = [f'https://telegra.ph/test_path_photo{user_id[0]}', 'null',
                 f'https://telegra.ph/test_path_photo{user_id[2]}',
                 f'https://telegra.ph/test_path_photo{user_id[3]}']
        video = [f'https://telegra.ph/test_path_video{user_id[0]}', 'null',
                 f'https://telegra.ph/test_path_video{user_id[2]}',
                 f'https://telegra.ph/test_path_video{user_id[3]}']
        point = ["ST_GeomFromText('POINT(45 45)', 4326)", "ST_GeomFromText('POINT(-45 -45)', 4326)", 'null', 'null']
        polygon = ['null', 'null', "ST_GeomFromText('POLYGON((30 30, -30 -30, 10 20, 30 30))', 4326)",
                   "ST_GeomFromText('POLYGON((40 10, -40 -10, 70 20, 40 10))', 4326)"]

        cursor.execute(f"select id, question from test_questions where survey = {self.survey} order by id")
        questions = cursor.fetchall()

        for i in range(len(user_id)):
            cursor.execute(f"insert into test_features (id, user_id, user_name, survey, entr_time, photo, video, "
                           f"point, polygon, q_count, ans_check) values (default, {user_id[i]}, '{user_name[i]}', "
                           f"{self.survey}, '{time}', '{photo[i]}', '{video[i]}', {point[i]}, {polygon[i]}, 2, 1)")
            for j in range(2):
                cursor.execute(f"select q_count from test_features where id = (select max(id) from test_features where "
                               f"user_id = {user_id[i]})")
                q_count = cursor.fetchall()[0][0]
                cursor.execute(f"insert into test_answers (id, f_id, q_id, answer) values (default, "
                               f"(select max(id) from test_features where user_id = {user_id[i]}), "
                               f"{questions[q_count * (- 1)][0]}, 'answer{user_id[i]}_{j+1}')")
                if q_count > 1:
                    cursor.execute(f"update test_features set q_count = {q_count - 1} where id = (select max(id) from "
                                   f"test_features where user_id = {user_id[i]})")
        connection.commit()

    def correct_features(self):
        cursor.execute(f"update test_features set photo = null, video = null where photo = 'null' or video = 'null'")
        connection.commit()

    def set_test_data(self):
        self.user_id = self.num
        self.survey = f"'{self.message.survey}'"
        self.set_questions()
        self.set_features_answers()
        self.correct_features()
