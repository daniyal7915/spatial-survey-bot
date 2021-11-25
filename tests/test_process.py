from unittest import mock, TestCase, main
from engine.process import State, Survey, PointPolygon, QuestionAnswer, Coord, Media, Delete, CreateWebMap, \
    CreateGJsonShp, GeoJson, Shp
from engine.utils.tables import Tables
from engine.utils.answers import answers
from tests.utils.set import SetTestData
from tests.utils.utils import ShpProcess, MockResponse, Message
from tests.utils.data import Data, Result


tables = Tables('test_')
tables.drop()
tables.create()

connection = tables.connection
cursor = tables.cursor

state, delete, survey = State('test_'), Delete('test_'), Survey('test_')
coord, media, qa = Coord('test_'), Media('test_'), QuestionAnswer('test_')
pp, webmap, gjson_shp = PointPolygon(), CreateWebMap('test_'), CreateGJsonShp('test_')
gjson, shp = GeoJson('test_'), Shp('test_')


class TestState(TestCase, Message, Result):
    def test_states(self):
        self.assertEqual(state.states, self.result_states)

    def test_show_state_init(self):
        self.num = 1

        self.assertEqual(state.show_state(self.message), self.result_states['INIT'])

    def test_show_state(self):
        self.num = 2

        cursor.execute(f"insert into test_user_state values({self.message.from_user.id},"
                       f"'{self.message.from_user.first_name}', {self.data_states['RESULT']})")
        connection.commit()

        self.assertEqual(state.show_state(self.message), self.result_states['RESULT'])

    def test_save_state(self):
        self.num = 3

        cursor.execute(f"insert into test_user_state values({self.message.from_user.id}, "
                       f"'{self.message.from_user.first_name}', {self.data_states['TRANSIT']})")
        connection.commit()

        state.save_state(self.message, self.data_states['SUBMIT'])

        cursor.execute(f'select user_state from test_user_state where user_id = {self.message.from_user.id}')
        self.assertEqual(cursor.fetchall()[0][0], self.result_states['SUBMIT'])


class SurveyTest(TestCase, Message):
    def test_save_survey(self):
        self.num = 4

        cursor.execute(f"insert into test_user_state values({self.message.from_user.id}, "
                       f"'{self.message.from_user.first_name}')")
        connection.commit()

        survey.save_survey(self.message)

        cursor.execute(f"select survey from test_user_state where user_id = {self.message.from_user.id}")
        self.assertEqual(cursor.fetchall()[0][0], self.message.text)

    def test_get_survey(self):
        self.num = 5

        cursor.execute(f"insert into test_user_state(user_id, survey) values({self.message.from_user.id}, "
                       f"'{self.message.survey}')")
        connection.commit()

        self.assertEqual(survey.get_survey(self.message), self.message.text)

    @mock.patch('engine.process.Survey.get_survey')
    def test_get_author(self, get_survey):
        self.num = 6

        get_survey.return_value = self.message.survey

        cursor.execute(f"insert into test_questions(survey, author) values('{self.message.survey}', "
                       f"{self.message.from_user.id})")
        connection.commit()

        self.assertEqual(survey.get_author(self.message), self.message.from_user.id)

    def test_survey_initial(self):
        self.num = 7

        self.assertEqual(survey.survey_initial(self.message), answers['SURVEY_SAVED'] % self.message.survey)

        cursor.execute(f"select survey, author, question from test_questions where id = (select max(id) from "
                       f"test_questions where survey = '{self.message.survey}')")
        self.assertEqual(cursor.fetchall()[0], (self.message.survey, self.message.from_user.id, None))

    @mock.patch('engine.process.Survey.get_survey')
    def test_survey_next(self, get_survey):
        self.num = 8

        get_survey.return_value = self.message.survey

        cursor.execute(f"insert into test_questions(survey, author, question) values('{self.message.survey}', "
                       f"{self.message.from_user.id}, 'question{self.num}')")
        connection.commit()

        survey.survey_next(self.message)

        cursor.execute(f"select survey, author, question from test_questions where id = (select max(id) from "
                       f"test_questions where survey = '{self.message.survey}')")
        self.assertEqual(cursor.fetchall()[0], (self.message.survey, self.message.from_user.id, None))

    def test_survey_check(self):
        self.num = 9

        cursor.execute(f"insert into test_questions(survey, author, question) values('{self.message.survey}', "
                       f"{self.message.from_user.id}, 'question{self.num}')")
        connection.commit()

        self.assertTrue(survey.survey_check(self.message))

        cursor.execute(f"delete from test_questions where survey = '{self.message.survey}'")
        connection.commit()

        self.assertFalse(survey.survey_check(self.message))


class PointPolygonTest(TestCase, Data, Result):
    def test_point(self):
        self.assertEqual(pp.point(self.data_point), self.result_point)

    def test_polygon(self):
        self.assertEqual(pp.polygon(self.data_polygon), self.result_polygon)


class QuestionAnswerTest(TestCase, Message, Result):
    @mock.patch('engine.process.Survey.get_survey')
    def test_ans_check_(self, get_survey):
        self.num = 10

        get_survey.return_value = self.message.survey

        cursor.execute(f"insert into test_features(user_id, survey, ans_check) values({self.message.from_user.id}, "
                       f"'{self.message.survey}', {self.data_ans_check[0]})")
        connection.commit()

        self.assertTrue(qa.ans_check(self.message))

        cursor.execute(f"delete from test_features where survey = '{self.message.survey}'")
        cursor.execute(f"insert into test_features(user_id, survey, ans_check) values({self.message.from_user.id}, "
                       f"'{self.message.survey}', {self.data_ans_check[1]})")
        connection.commit()

        self.assertFalse(qa.ans_check(self.message))

    @mock.patch('engine.process.Survey.get_survey')
    def test_init_row(self, get_survey):
        self.num = 11

        get_survey.return_value = self.message.survey

        qa.init_row(self.message)

        cursor.execute(f"select user_id, user_name, survey from test_features where id = (select max(id) from "
                       f"test_features where survey = '{self.message.survey}')")
        self.assertEqual(cursor.fetchall()[0], (self.message.from_user.id, self.message.from_user.first_name,
                                                self.message.survey))

    @mock.patch('engine.process.Survey.get_survey')
    def test_question_insert(self, get_survey):
        self.num = 12
        self.text = f'question{self.num}'

        get_survey.return_value = self.message.survey

        cursor.execute(f"insert into test_questions (id, survey, author) values (default, '{self.message.survey}',"
                       f"{self.message.from_user.id})")
        connection.commit()

        self.assertEqual(qa.question_insert(self.message), answers['Q_SAVED'] % self.message.text)

        cursor.execute(f"select question from test_questions where id = (select max(id) from "
                       f"test_questions where survey = '{self.message.survey}')")
        self.assertEqual(cursor.fetchall()[0][0], self.message.text)

    @mock.patch('engine.process.Survey.get_survey')
    def test_question_null(self, get_survey):
        self.num = 13
        self.text = f'question{self.num}'

        get_survey.return_value = self.message.survey

        cursor.execute(f"insert into test_questions (id, survey, author, question) values (default, "
                       f"'{self.message.survey}', {self.message.from_user.id}, '{self.message.text}')")
        connection.commit()

        qa.question_null(self.message)

        cursor.execute(f"select question from test_questions where id = (select max(id) from "
                       f"test_questions where survey = '{self.message.survey}')")
        self.assertFalse(cursor.fetchall()[0][0])

    @mock.patch('engine.process.Survey.get_survey')
    def test_get_question(self, get_survey):
        self.num = 14

        get_survey.return_value = self.message.survey

        for i in range(1, 3):
            cursor.execute(f"insert into test_questions (id, survey, author, question) values (default, "
                           f"'{self.message.survey}',{self.message.from_user.id}, 'question{self.num}_{i}')")
            cursor.execute(f"insert into test_features (id, user_id, q_count) values (default, "
                           f"{self.message.from_user.id}, {self.data_get_question})")
        connection.commit()

        self.assertEqual(qa.get_question(self.message), f'question{self.num}_1')

        cursor.execute(f"select q_count from test_features where id = (select max(id) from "
                       f"test_features where user_id = {self.message.from_user.id})")
        self.assertEqual(cursor.fetchall()[0][0], self.result_count)

    def test_get_q_count(self):
        self.num = 15

        cursor.execute(f"insert into test_features (id, user_id, q_count) values (default, "
                       f"{self.message.from_user.id}, {self.data_get_q_count[0]})")
        cursor.execute(f"insert into test_features (id, user_id, q_count) values (default, "
                       f"{self.message.from_user.id}, {self.data_get_q_count[1]})")
        connection.commit()

        self.assertEqual(qa.get_q_count(self.message), self.result_get_q_count)

    def test_set_ans_check(self):
        self.num = 16

        cursor.execute(f"insert into test_features (id, user_id, ans_check) values (default, "
                       f"{self.message.from_user.id}, {self.data_set_ans_check})")
        cursor.execute(f"insert into test_features (id, user_id) values (default, {self.message.from_user.id})")
        connection.commit()

        qa.set_ans_check(self.message)

        cursor.execute(f"select ans_check from test_features where id = (select max(id) from "
                       f"test_features where user_id = {self.message.from_user.id})")
        self.assertEqual(cursor.fetchall()[0][0], self.result_set_ans_check)

    @mock.patch('engine.process.QuestionAnswer.get_q_count')
    @mock.patch('engine.process.Survey.get_survey')
    def test_answer_insert(self, get_survey, q_count):
        self.num = 17
        self.text = f'answer{self.num}'

        q_count.side_effect = self.data_answer_insert[0]
        get_survey.return_value = self.message.survey

        cursor.execute(f"insert into test_features (id, user_id, survey) values (default, {self.message.from_user.id}, "
                       f"'{self.message.survey}')")
        for i in range(1, 4):
            cursor.execute(f"insert into test_questions (id, survey, author, question) values (default, "
                           f"'{self.message.survey}',{self.message.from_user.id}, 'question{self.num}_{i}')")
        connection.commit()

        self.assertEqual(qa.answer_insert(self.message, self.data_answer_insert[1][0]),
                         answers['ANS_NEXT_Q'] % f'question{self.num}_{self.result_answer_insert[0]}')
        self.assertEqual(qa.answer_insert(self.message, self.data_answer_insert[1][1]),
                         answers['ANS_NEXT_Q'] % f'question{self.num}_{self.result_answer_insert[1]}')
        self.assertEqual(qa.answer_insert(self.message, self.data_answer_insert[1][2]),
                         answers['ALL_ANSWERED'])


class CoordTest(TestCase, Message, Result):
    def test_get_poly_points(self):
        self.num = 18

        cursor.execute(f"insert into test_features (id, user_id, poly_points) values (default, "
                       f"{self.message.from_user.id}, '{self.data_get_pp}')")
        connection.commit()

        self.assertEqual(coord.get_poly_points(self.message), self.result_get_pp)

    @mock.patch('engine.process.Coord.get_poly_points')
    def test_append_poly_points(self, poly_points):
        self.num = 19

        poly_points.side_effect = self.data_append_pp[0]

        lat = self.data_append_pp[1]
        long = self.data_append_pp[2]

        cursor.execute(f"insert into test_features (id, user_id) values (default, {self.message.from_user.id})")
        connection.commit()

        coord.append_poly_points(self.message, lat, long)

        cursor.execute(f"select poly_points from test_features where id = (select max(id) from test_features where "
                       f"user_id = {self.message.from_user.id})")
        self.assertEqual(cursor.fetchall()[0][0], self.result_append_pp[0])

        coord.append_poly_points(self.message, lat, long)

        cursor.execute(f"select poly_points from test_features where id = (select max(id) from test_features where "
                       f"user_id = {self.message.from_user.id})")
        self.assertEqual(cursor.fetchall()[0][0], self.result_append_pp[1])

    @mock.patch('engine.process.Coord.get_poly_points')
    def test_get_count(self, poly_points):
        poly_points.side_effect = self.data_get_count

        self.assertEqual(coord.get_count(self.message), self.result_get_count[0])
        self.assertEqual(coord.get_count(self.message), self.result_get_count[1])

    def test_point_manual(self):
        self.num = 20

        data = self.data_point_polygon_manual
        lat, long = int(data[2][:3]), int(data[2][-3:])
        time = self.data_time

        cursor.execute(f"insert into test_features (id, user_id) values (default, {self.message.from_user.id})")
        connection.commit()

        for i in range(len(data)):
            self.text = data[i]
            if i in [0, 1]:
                self.assertEqual(coord.point_manual(self.message), answers['FOLLOW_TEMPLATE'])
            elif i == 2:
                self.assertEqual(coord.point_manual(self.message), answers['POINT_MEDIA'] % (lat, long))

                cursor.execute(
                    f"select ST_AsText(point), to_char(entr_time, 'YYYY') from test_features where id = "
                    f"(select max(id) from test_features where user_id = {self.message.from_user.id})")
                self.assertEqual(cursor.fetchall()[0], (f'POINT({long} {lat})', time))
            elif i == 3:
                self.assertEqual(coord.point_manual(self.message), answers['INVALID_COORD'])
            elif i == 4:
                self.assertEqual(coord.point_manual(self.message), answers['INVALID_LAT'])
            else:
                self.assertEqual(coord.point_manual(self.message), answers['INVALID_LONG'])

    def test_point_location(self):
        self.num = 21

        cursor.execute(f"insert into test_features (id, user_id) values (default, {self.message.from_user.id})")
        connection.commit()

        self.assertEqual(coord.point_location(self.message), answers['POINT_MEDIA'] % (self.message.location.latitude,
                                                                                       self.message.location.longitude))

        cursor.execute(f"select ST_AsText(point), to_char(entr_time, 'YYYY') from test_features where id = "
                       f"(select max(id) from test_features where user_id = {self.message.from_user.id})")
        self.assertEqual(cursor.fetchall()[0], self.result_point_manual)

    @mock.patch('engine.process.Coord.append_poly_points')
    def test_polygon_manual(self, poly_points):
        self.num = 22

        poly_points.return_value = True

        data = self.data_point_polygon_manual

        for i in range(len(data)):
            self.text = data[i]
            if i in [0, 1]:
                self.assertEqual(coord.polygon_manual(self.message), answers['FOLLOW_TEMPLATE'])
            elif i == 2:
                self.assertEqual(coord.polygon_manual(self.message), answers['VERTEX_DONE'])
            elif i == 3:
                self.assertEqual(coord.polygon_manual(self.message), answers['INVALID_COORD'])
            elif i == 4:
                self.assertEqual(coord.polygon_manual(self.message), answers['INVALID_LAT'])
            else:
                self.assertEqual(coord.polygon_manual(self.message), answers['INVALID_LONG'])

    @mock.patch('engine.process.Coord.append_poly_points')
    def test_polygon_location(self, poly_points):
        self.num = 23

        poly_points.return_value = True

        self.assertEqual(coord.polygon_location(self.message), answers['VERTEX_DONE'])

    def test_polygon_create(self):
        self.num = 24

        cursor.execute(f"insert into test_features (id, user_id) values (default, {self.message.from_user.id})")
        connection.commit()

        self.assertEqual(coord.polygon_create(self.message, self.data_polygon_create.split(',')),
                         answers['POLYGON_MEDIA'])

        cursor.execute(f"select ST_AsText(polygon), to_char(entr_time, 'YYYY') from test_features where id = "
                       f"(select max(id) from test_features where user_id = {self.message.from_user.id})")
        self.assertEqual(cursor.fetchall()[0], self.result_polygon_create)


class MediaTest(TestCase, Message, Result):
    def test_save_media(self):
        self.num = 25
        path = self.data_save_media

        cursor.execute(f"insert into test_features (id, user_id) values (default, {self.message.from_user.id})")
        connection.commit()

        self.assertEqual(media.save_media(self.message, path, 'photo'), answers['MEDIA_SAVED'] % ('photo', 'photo',
                                                                                                  'video'))

        cursor.execute(f"select photo from test_features where id = (select max(id) from test_features where "
                       f"user_id = {self.message.from_user.id})")
        self.assertEqual(cursor.fetchall()[0][0], self.result_save_media)

        self.assertEqual(media.save_media(self.message, path, 'video'), answers['MEDIA_SAVED'] % ('video', 'video',
                                                                                                  'photo'))

        cursor.execute(f"select video from test_features where id = (select max(id) from test_features where "
                       f"user_id = {self.message.from_user.id})")
        self.assertEqual(cursor.fetchall()[0][0], self.result_save_media)

        self.assertEqual(media.save_media(self.message, None, 'photo'), answers['MEDIA_NS'] % ('photo', 'photo',
                                                                                               'video'))
        self.assertEqual(media.save_media(self.message, None, 'video'), answers['MEDIA_NS'] % ('video', 'video',
                                                                                               'photo'))

    @mock.patch('requests.post')
    @mock.patch('urllib.request.urlopen')
    def test_media_path(self, urlopen, post):
        token = self.data_media_path[0]
        file_info = self.data_media_path[1]
        m_type = self.data_media_path[2]

        mocked = mock.MagicMock()
        mocked.__enter__.return_value = mocked

        urlopen.return_value = mocked

        mocked.getcode.return_value = 200
        post.return_value = MockResponse(200)
        self.assertEqual(media.media_path(token, file_info, m_type), self.result_media_path)

        mocked.getcode.return_value = 200
        post.return_value = MockResponse()
        self.assertFalse(media.media_path(token, file_info, m_type))

        mocked.getcode.return_value = 404
        post.return_value = MockResponse(200)
        self.assertFalse(media.media_path(token, file_info, m_type))


class CreateWebMapTest(TestCase, SetTestData, Result):
    @mock.patch('engine.process.PointPolygon.polygon')
    @mock.patch('engine.process.PointPolygon.point')
    @mock.patch('engine.process.Survey.get_survey')
    def test_source(self, get_survey, point, polygon):
        self.num = 26

        self.set_test_data()

        polygon.side_effect = self.data_double_polygon
        point.side_effect = self.data_double_point
        get_survey.return_value = self.message.survey

        self.assertEqual(webmap.source(f"'{self.message.survey}'"), self.result_source_webmap)

    def test_geom_extent(self):
        self.num = 29

        self.set_test_data()

        self.assertEqual(webmap.geom_extent(f"'{self.message.survey}'"), self.result_extent)

    def test_map_center(self):
        self.assertEqual(webmap.map_center(self.data_map_center[0]), self.result_triple_map_center[0])
        self.assertEqual(webmap.map_center(self.data_map_center[1]), self.result_triple_map_center[1])
        self.assertEqual(webmap.map_center(self.data_map_center[2]), self.result_triple_map_center[2])

    @mock.patch('engine.process.CreateWebMap.map_center')
    @mock.patch('engine.process.Survey.get_survey')
    def test_adjust(self, get_survey, map_center):
        self.num = 32

        self.set_test_data()

        map_center.side_effect = self.data_triple_map_center
        get_survey.return_value = self.message.survey

        self.assertEqual(webmap.adjust(f"'{self.message.survey}'", self.data_adjust[0], self.data_adjust[1]),
                         self.result_triple_map_center[0])
        self.assertEqual(webmap.adjust(f"'{self.message.survey}'", self.data_adjust[0], None),
                         self.result_triple_map_center[1])
        self.assertEqual(webmap.adjust(f"'{self.message.survey}'", None, self.data_adjust[1]),
                         self.result_triple_map_center[2])

    def test_distance(self):
        adjust = self.data_triple_map_center

        for i in range(len(adjust)):
            self.assertEqual(webmap.distance(adjust[i]), self.result_distance[i])

    def test_get_scale(self):
        distance = self.data_get_scale

        for i in range(len(distance)):
            self.assertEqual(webmap.get_scale(distance[i]), self.result_get_scale[i])

    @mock.patch('engine.process.CreateWebMap.get_scale')
    @mock.patch('engine.process.CreateWebMap.source')
    @mock.patch('engine.process.CreateWebMap.distance')
    @mock.patch('engine.process.CreateWebMap.adjust')
    @mock.patch('engine.process.CreateWebMap.geom_extent')
    @mock.patch('engine.process.Survey.get_survey')
    def test_create(self, get_survey, geom_extent, adjust, distance, source, get_scale):
        self.num = 35

        get_scale.return_value = self.data_scale
        source.return_value = self.data_webmap
        distance.return_value = self.data_distance
        adjust.return_value = self.data_triple_map_center[0]
        geom_extent.return_value = self.data_extent
        get_survey.return_value = self.message.survey

        self.assertEqual(webmap.create(self.message).getvalue(), self.result_webmap)


class CreateGJsonShpTest(TestCase, SetTestData, Result):
    @mock.patch('engine.process.Survey.get_survey')
    def test_ques_ans(self, get_survey):
        self.num = 38

        self.set_test_data()

        get_survey.return_value = self.message.survey

        self.assertEqual(gjson_shp.ques_ans(f"'{self.message.survey}'"), self.result_ques_ans)

    @mock.patch('engine.process.CreateGJsonShp.ques_ans')
    @mock.patch('engine.process.Shp.geom_shp')
    @mock.patch('engine.process.GeoJson.geom_gjson')
    @mock.patch('engine.process.Survey.get_survey')
    def test_create(self, get_survey, geom_gjson, geom_shp, ques_ans):
        self.num = 41

        ques_ans.return_value = {}
        geom_shp.side_effect = self.data_gjson_shp[0]
        geom_gjson.side_effect = self.data_gjson_shp[1]
        get_survey.return_value = self.message.survey

        self.assertEqual(gjson_shp.create(self.message, 'shapefile'), self.result_gjson_shp[0])
        self.assertEqual(gjson_shp.create(self.message, 'geojson'), self.result_gjson_shp[1])


class GeoJsonTest(TestCase, SetTestData, Result):
    @mock.patch('engine.process.PointPolygon.polygon')
    @mock.patch('engine.process.PointPolygon.point')
    @mock.patch('engine.process.Survey.get_survey')
    def test_gjson(self, get_survey, point, polygon):
        self.num = 44

        self.set_test_data()

        polygon.side_effect = self.data_quad_polygon
        point.side_effect = self.data_quad_point
        get_survey.return_value = self.message.survey

        self.assertEqual(gjson.gjson('point', f"'{self.message.survey}'", self.data_question, self.data_double_answer,
                                     self.data_count), self.result_gjson_point)
        self.assertEqual(gjson.gjson('polygon', f"'{self.message.survey}'", self.data_question, self.data_double_answer,
                                     self.data_count), self.result_gjson_polygon)

    @mock.patch('engine.process.GeoJson.gjson')
    def test_geom_gjson(self, geojson):
        self.num = 47

        geojson.side_effect = [self.data_geom_gjson_point, self.data_geom_gjson_polygon]

        self.assertEqual(gjson.geom_gjson(self.message, 'point', f"'{self.message.survey}'",
                                          self.data_ques_ans).getvalue(), self.result_geom_gjson_point)
        self.assertEqual(gjson.geom_gjson(self.message, 'polygon', f"'{self.message.survey}'",
                                          self.data_ques_ans).getvalue(), self.result_geom_gjson_polygon)


class ShpTest(TestCase, SetTestData, ShpProcess, Result):
    @mock.patch('engine.process.PointPolygon.polygon')
    @mock.patch('engine.process.PointPolygon.point')
    @mock.patch('engine.process.Survey.get_survey')
    def test_shp(self, get_survey, point, polygon):
        self.num = 50

        self.set_test_data()

        polygon.side_effect = self.data_quad_polygon
        point.side_effect = self.data_quad_point
        get_survey.return_value = self.message.survey

        output = self.shp_value(shp.shp('point', f"'{self.message.survey}'", self.data_question,
                                        self.data_double_answer, self.data_count))
        self.assertEqual(output, self.result_shp_point)

        output = self.shp_value(shp.shp('polygon', f"'{self.message.survey}'", self.data_question,
                                        self.data_double_answer, self.data_count))
        self.assertEqual(output, self.result_shp_polygon)

    @mock.patch('engine.process.Shp.shp')
    @mock.patch('engine.process.Survey.get_survey')
    def test_geom_shp(self, get_survey, shapefile):
        self.num = 53

        shapefile.side_effect = [self.shp_bytes(self.data_geom_shp_point), self.shp_bytes(self.data_geom_shp_polygon)]
        get_survey.return_value = self.message.survey

        output = shp.geom_shp(self.message, 'point', f"'{self.message.survey}'", self.data_ques_ans)
        for i in range(len(output)):
            output[i] = output[i].getvalue()
        self.assertEqual(output, self.result_geom_shp_point)

        output = shp.geom_shp(self.message, 'polygon', f"'{self.message.survey}'", self.data_ques_ans)
        for i in range(len(output)):
            output[i] = output[i].getvalue()
        self.assertEqual(output, self.result_geom_shp_polygon)


class DeleteTest(TestCase, Message, Result):
    @mock.patch('engine.process.Survey.get_survey')
    def test_del_question(self, get_survey):
        self.num = 54

        get_survey.return_value = self.message.survey

        for i in range(1, 3):
            cursor.execute(f"insert into test_questions(survey, author, question) values('{self.message.survey}', "
                           f"{self.message.from_user.id}, 'question{self.num}_{i}')")
        connection.commit()

        delete.del_question(self.message)

        cursor.execute(f"select * from test_questions where survey = '{self.message.survey}'")
        self.assertFalse(cursor.fetchall())

    def test_check_ans(self):
        self.num = 55

        cursor.execute(f"insert into test_features (id, user_id, ans_check) values (default, "
                       f"{self.message.from_user.id}, {self.data_ans_check[0]})")
        connection.commit()

        self.assertEqual(delete.check_ans(self.message), self.result_ans_check[0])

        cursor.execute(f"update test_features set ans_check = {self.data_ans_check[1]} where id = "
                       f"(select max(id) from test_features where user_id = {self.message.from_user.id})")
        connection.commit()

        self.assertFalse(delete.check_ans(self.message))

    def test_del_row(self):
        self.num = 56

        cursor.execute(f"insert into test_features (id, user_id) values (default, {self.message.from_user.id})")
        cursor.execute(f"insert into test_answers (id, f_id) values (default, (select max(id) from test_features where "
                       f"user_id = {self.message.from_user.id}))")
        connection.commit()

        cursor.execute(f"select max(id) from test_features where user_id = {self.message.from_user.id}")
        f_id = cursor.fetchall()[0][0]

        delete.del_row(self.message)

        cursor.execute(f"select * from test_answers where f_id = {f_id}")
        self.assertFalse(cursor.fetchall())

        cursor.execute(f"select * from test_features where id = {f_id}")
        self.assertFalse(cursor.fetchall())

    @mock.patch('engine.process.Survey.get_survey')
    def test_del_data(self, get_survey):
        self.num = 57

        get_survey.return_value = self.message.survey

        for i in range(3):
            cursor.execute(f"insert into test_features (id, user_id, survey, ans_check) values "
                           f"(default, {self.message.from_user.id}, '{self.message.survey}', {self.data_ans_check[0]})")
            cursor.execute(f"insert into test_answers (id, f_id) values (default, (select max(id) from "
                           f"test_features where user_id = {self.message.from_user.id}))")
        connection.commit()

        cursor.execute(f"select id from test_features where survey = '{self.message.survey}' and "
                       f"ans_check = {self.data_ans_check[0]}")
        id_list = cursor.fetchall()

        delete.del_data(self.message)

        for elem in id_list:
            cursor.execute(f"select * from test_answers where f_id = {elem[0]}")
            self.assertFalse(cursor.fetchall())

        cursor.execute(f"select * from test_features where survey = '{self.message.survey}' and ans_check = "
                       f"{self.data_ans_check[0]}")
        self.assertFalse(cursor.fetchall())

    def test_del_feature(self):
        self.num = 58

        cursor.execute(f"insert into test_features (id, user_id) values (default, {self.message.from_user.id})")
        connection.commit()

        cursor.execute(f"select max(id) from test_features where user_id = {self.message.from_user.id}")
        max_id = cursor.fetchall()[0][0]

        delete.del_feature(self.message)

        cursor.execute(f"select * from test_features where id = {max_id}")
        self.assertFalse(cursor.fetchall())


if __name__ == "__main__":
    main()