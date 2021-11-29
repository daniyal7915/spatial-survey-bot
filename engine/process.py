import io
import shapefile
import json
import datetime
import requests
import urllib.request
from engine.utils.tables import Tables
from engine.utils.utils import ProcessData
from engine.utils.answers import answers
from templates import map_template
from tests.utils.utils import TestID

tables = Tables()
connection = tables.connection
cursor = tables.cursor


class State:
    states = ProcessData().states

    def __init__(self, db=''):
        self.db = db

    def show_state(self, message):
        cursor.execute(f'select exists(select 1 from {self.db}user_state where user_id = {message.from_user.id} '
                       f'limit 1)')
        if not cursor.fetchall()[0][0]:
            cursor.execute(f"insert into {self.db}user_state values({message.from_user.id},"
                           f"'{message.from_user.first_name}', {self.states['INIT']})")
            connection.commit()

        cursor.execute(f'select user_state from {self.db}user_state where user_id = {message.from_user.id}')
        return cursor.fetchall()[0][0]

    def save_state(self, message, current_state):
        cursor.execute(f'update {self.db}user_state set user_state = {current_state} where '
                       f'user_id = {message.from_user.id}')
        connection.commit()


class Survey(ProcessData):
    def __init__(self, db=''):
        self.db = db

    def save_survey(self, message):
        if len(message.text) > 25:
            return True
        else:
            cursor.execute(f"update {self.db}user_state set survey = '{self.sub(message.text.lower())}' where "              
                           f"user_id = {message.from_user.id}")
            connection.commit()

    def get_survey(self, message):
        cursor.execute(f"select survey from {self.db}user_state where user_id = {message.from_user.id}")
        return cursor.fetchall()[0][0]

    def get_author(self, message):
        cursor.execute(f"select author from {self.db}questions where survey = '{self.get_survey(message)}'")
        return cursor.fetchall()[0][0]

    def survey_initial(self, message):
        cursor.execute(f"insert into {self.db}questions (id, survey, author) values (default, "
                       f"'{self.sub(message.text.lower())}', {message.from_user.id})")
        connection.commit()

        return answers['SURVEY_SAVED'] % self.sub(message.text)

    def survey_next(self, message):
        cursor.execute(f"select question from {self.db}questions where id = (select max(id) from {self.db}questions "
                       f"where survey = '{self.get_survey(message)}')")
        if cursor.fetchall()[0][0]:
            cursor.execute(f"insert into {self.db}questions (id, survey, author) values (default, "
                           f"'{self.get_survey(message)}', {message.from_user.id})")
            connection.commit()

    def survey_check(self, message):
        if len(message.text) > 25:
            return

        cursor.execute(f"select exists (SELECT 1 FROM {self.db}questions WHERE "
                       f"survey = '{self.sub(message.text.lower())}' LIMIT 1)")
        return cursor.fetchall()[0][0]


class PointPolygon:
    def point(self, row):
        transit, result = row[6:-1].split(' '), []

        result.append(float(transit[0]))
        result.append(float(transit[1]))

        return result

    def polygon(self, row):
        transit, result = row[9:-2].split(','), []

        for elem in transit:
            temp1 = []
            temp2 = elem.split(' ')
            temp1.append(float(temp2[0]))
            temp1.append(float(temp2[1]))
            result.append(temp1)

        return result


class QuestionAnswer(Survey, PointPolygon):
    def __init__(self, db=''):
        super().__init__(db)
        self.db = db

    def ans_check(self, message):
        cursor.execute(f"select exists(select 1 from {self.db}features where ans_check = 1 and "
                       f"survey = '{self.get_survey(message)}'limit 1)")
        return cursor.fetchall()[0][0]

    def init_row(self, message):
        cursor.execute(f"insert into {self.db}features (id, user_id, user_name, survey) values (default, "
                       f"{message.from_user.id}, '{message.from_user.first_name}', '{self.get_survey(message)}')")
        connection.commit()

    def question_insert(self, message):
        if len(message.text) > 50:
            return answers['LONG']

        cursor.execute(f"select question from {self.db}questions where id = (select max(id) from {self.db}questions "
                       f"where survey = '{self.get_survey(message)}')")
        if cursor.fetchall()[0][0] is None:
            cursor.execute(f"update {self.db}questions set question = '{self.sub(message.text)}' "
                           f"where id = (select max(id) from {self.db}questions where "
                           f"survey = '{self.get_survey(message)}')")
            connection.commit()
            return answers['Q_SAVED'] % self.sub(message.text)

    def question_null(self, message):
        cursor.execute(f"update {self.db}questions set question = null where id = (select max(id) from "
                       f"{self.db}questions where survey = '{self.get_survey(message)}')")
        connection.commit()

    def get_question(self, message):
        cursor.execute(f"select id, question from {self.db}questions where survey = '{self.get_survey(message)}' "
                       f"order by id")
        result = cursor.fetchall()

        cursor.execute(f"update {self.db}features set q_count = {len(result)} where id = (select max(id) from "
                       f"{self.db}features where user_id = {message.from_user.id})")
        connection.commit()

        return result[0][1]

    def get_q_count(self, message):
        cursor.execute(f"select q_count from {self.db}features where id = (select max(id) from {self.db}features where "
                       f"user_id = {message.from_user.id})")
        return cursor.fetchall()[0][0]

    def set_ans_check(self, message):
        cursor.execute(f"update {self.db}features set ans_check = 1 where id = (select max(id) from {self.db}features "
                       f"where user_id = {message.from_user.id})")
        connection.commit()

    def answer_insert(self, message, ans_num=''):
        if len(message.text) > 255:
            return answers['LONG']
        else:
            q_count = self.get_q_count(message)
            cursor.execute(f"select id, question from {self.db}questions where survey = '{self.get_survey(message)}' "
                           f"order by id")
            result = cursor.fetchall()
            cursor.execute(f"insert into {self.db}answers (id, f_id, q_id, answer) values (default, "
                           f"(select max(id) from {self.db}features where user_id = {message.from_user.id}),"
                           f"{result[q_count * (- 1)][0]}, '{self.sub(message.text)}{ans_num}')")
            connection.commit()
            if q_count > 1:
                cursor.execute(
                    f"update {self.db}features set q_count = {q_count - 1} where id = (select max(id) from "
                    f"{self.db}features where user_id = {message.from_user.id})")
                connection.commit()
                return answers['ANS_NEXT_Q'] % result[(q_count - 1) * (-1)][1]
            else:
                return answers['ALL_ANSWERED']


class Coord:
    def __init__(self, db=''):
        self.db = db

    def get_poly_points(self, message):
        cursor.execute(f"select poly_points from {self.db}features where id = (select max(id) from "
                       f"{self.db}features where user_id = {message.from_user.id})")
        return cursor.fetchall()[0][0]

    def append_poly_points(self, message, lat, long):
        if self.get_poly_points(message):
            concat = self.get_poly_points(message) + f",{long} {lat}"
            cursor.execute(
                f"update {self.db}features set poly_points = '{concat}' where id = (select max(id) from "
                f"{self.db}features where user_id = {message.from_user.id})")
            connection.commit()
        else:
            cursor.execute(f"update {self.db}features set poly_points = '{long} {lat}' where id = (select max(id) from "
                           f"{self.db}features where user_id = {message.from_user.id})")
            connection.commit()

    def get_count(self, message):
        if self.get_poly_points(message):
            return len(self.get_poly_points(message).split(','))
        else:
            return 0

    def point_manual(self, message):
        if len(message.text) > 25:
            return answers['LONG']
        else:
            try:
                lat, long = message.text.lower().split(',')
                lat, long = float(lat), float(long)
                if -90 <= lat <= 90 and -180 <= long <= 180:
                    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(f"update {self.db}features set point = ST_GeomFromText("
                                   f"'POINT({long} {lat})',4326), entr_time = '{time}'"
                                   f"where id = (select max(id) from {self.db}features where "
                                   f"user_id = {message.from_user.id})")
                    connection.commit()
                    return answers['POINT_MEDIA'] % (lat, long)
                elif not -90 <= lat <= 90 and not -180 <= long <= 180:
                    return answers['INVALID_COORD']
                elif not -90 <= lat <= 90:
                    return answers['INVALID_LAT']
                else:
                    return answers['INVALID_LONG']
            except ValueError:
                return answers['FOLLOW_TEMPLATE']

    def point_location(self, message):
        lat = message.location.latitude
        long = message.location.longitude
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(f"update {self.db}features set point = ST_GeomFromText("
                       f"'POINT({long} {lat})',4326), entr_time = '{time}'"
                       f"where id = (select max(id) from {self.db}features where user_id = {message.from_user.id})")
        connection.commit()

        return answers['POINT_MEDIA'] % (lat, long)

    def polygon_manual(self, message):
        if len(message.text) > 25:
            return answers['LONG']
        else:
            try:
                lat, long = message.text.lower().split(',')
                lat, long = float(lat), float(long)
                if -90 <= lat <= 90 and -180 <= long <= 180:
                    self.append_poly_points(message, lat, long)
                    return answers['VERTEX_DONE']
                elif not -90 <= lat <= 90 and not -180 <= long <= 180:
                    return answers['INVALID_COORD']
                elif not -90 <= lat <= 90:
                    return answers['INVALID_LAT']
                else:
                    return answers['INVALID_LONG']
            except ValueError:
                return answers['FOLLOW_TEMPLATE']

    def polygon_location(self, message):
        lat = message.location.latitude
        long = message.location.longitude

        self.append_poly_points(message, lat, long)

        return answers['VERTEX_DONE']

    def polygon_create(self, message, poly_points):
        if poly_points[0] != poly_points[-1]:
            poly_points.append(poly_points[0])

        vertices = ','.join(poly_points)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(f"update {self.db}features set polygon = ST_GeomFromText("
                       f"'POLYGON(({vertices}))',4326), entr_time ='{time}'"
                       f"where id = (select max(id) from {self.db}features where user_id = {message.from_user.id})")
        connection.commit()

        return answers['POLYGON_MEDIA']


class Media:
    def __init__(self, db=''):
        self.db = db

    def save_media(self, message, path, media):
        other_media = 'photo'

        if media == 'photo':
            other_media = 'video'

        if path:
            cursor.execute(f"update {self.db}features set {media} = 'https://telegra.ph{path}' "
                           f"where id = (select max(id) from {self.db}features where user_id = {message.from_user.id})")
            connection.commit()
            return answers['MEDIA_SAVED'] % (media, media, other_media)
        else:
            return answers['MEDIA_NS'] % (media, media, other_media)

    def media_path(self, token, file_info, m_type):
        try:
            with urllib.request.urlopen(f'https://api.telegram.org/file/bot{token}/{file_info.file_path}') as get:
                if get.getcode() == 200:
                    post = requests.post('https://telegra.ph/upload', files={'file': ('file', get, m_type)})
                    if post.status_code == 200:
                        return post.json()[0]['src']
        except:
            pass


class Shp(PointPolygon, TestID):
    def __init__(self, db=''):
        self.db = db

    datum = ProcessData().datum

    def shp(self, geom_type, survey, question, answer, count):
        shp = {'shp': io.BytesIO(), 'shx': io.BytesIO(), 'dbf': io.BytesIO(), 'check': None}
        transit = []

        with shapefile.Writer(dbf=shp['dbf'], shp=shp['shp'], shx=shp['shx']) as w:
            w.field('ID')
            w.field('USER_NAME')
            w.field('SURVEY')
            w.field('TIME')
            w.field('PHOTO')
            w.field('VIDEO')

            for i in range(count):
                w.field(f"QUEST_{i + 1}")
                w.field(f"ANS_{i + 1}")

            cursor.execute(f"select id, user_name, survey, to_char(entr_time, 'DD-Mon-YYYY HH24:MI:SS'), "
                           f"photo, video, st_astext({geom_type}) from {self.db}features where "
                           f"survey = {survey} and ans_check = 1 order by id")
            for line in cursor.fetchall():
                elems = []
                for i in range(7):
                    elems.append(line[i])
                for j in range(count):
                    elems.append(question[j][0])
                    elems.append(answer[0][0])
                    del answer[0]
                transit.append(elems)

            if self.db == 'test_':
                transit = self.transit_process(transit)

            for row in transit:
                if row[6]:
                    shp['check'] = 1
                    if geom_type == 'point':
                        point_res = self.point(row[6])
                        w.point(point_res[0], point_res[1])
                    else:
                        w.poly([self.polygon(row[6])])
                    del row[6]
                    w.record(*row)

        return shp

    def geom_shp(self, call, geom_type, survey, data):
        output = []

        result = self.shp(geom_type, survey, data['question'], data['answer'], data['count'])

        if result['check'] == 1:
            shp = io.BytesIO(result['shp'].getvalue())
            shx = io.BytesIO(result['shx'].getvalue())
            dbf = io.BytesIO(result['dbf'].getvalue())
            prj = io.BytesIO(self.datum.encode('utf-8'))
            shp.name = f'{call.from_user.first_name}_{geom_type}.shp'
            shx.name = f'{call.from_user.first_name}_{geom_type}.shx'
            dbf.name = f'{call.from_user.first_name}_{geom_type}.dbf'
            prj.name = f'{call.from_user.first_name}_{geom_type}.prj'
            output.append(shp)
            output.append(shx)
            output.append(dbf)
            output.append(prj)

        return output


class GeoJson(PointPolygon, TestID):
    def __init__(self, db=''):
        self.db = db

    def gjson(self, geom_type, survey, question, answer, count):
        source = {'result': {"type": "FeatureCollection", "name": "Places",
                  "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": []},
                  'check': 0}

        cursor.execute(f"select id, user_name, survey, entr_time, photo, video, st_astext({geom_type})"
                       f" from {self.db}features where survey = {survey} and ans_check = 1 order by id")
        fetched = cursor.fetchall()

        for i in range(len(fetched)):
            row = fetched[i]
            elem = {"id": row[0], "user_name": f"{row[1]}", "survey": f"{row[2]}", "entr_time": f"{row[3]}",
                    "photo": f"{row[4]}", "video": f"{row[5]}"}
            if self.db == 'test_':
                elem = self.elem_process(elem, i)
            for j in range(count):
                elem[f"quest_{j + 1}"] = f"{question[j][0]}"
                elem[f"ans_{j + 1}"] = f"{answer[0][0]}"
                del answer[0]
            if row[6]:
                source['check'] = 1
                if geom_type == 'point':
                    source['result']["features"].append({"type": "Feature", "properties": elem,
                                                         "geometry": {"type": "Point",
                                                                      "coordinates": self.point(row[6])}})
                elif geom_type == 'polygon':
                    source['result']["features"].append({"type": "Feature", "properties": elem,
                                                         "geometry": {"type": "MultiPolygon",
                                                                      "coordinates": [[self.polygon(row[6])]]}})
        return source

    def geom_gjson(self, call, geom_type, survey, data):
        result = self.gjson(geom_type, survey, data['question'], data['answer'], data['count'])

        if result['check'] == 1:
            output = io.BytesIO(json.dumps(result['result']).encode('utf-8'))
            output.name = f'{call.from_user.first_name}_{geom_type}.geojson'
            return output


class CreateGJsonShp(Survey, GeoJson, Shp):
    def __init__(self, db=''):
        super().__init__(db)
        self.db = db

    def ques_ans(self, survey):
        ques_ans = {'question': None, 'answer': [], 'count': None}

        cursor.execute(f"select question from {self.db}questions where survey = {survey} order by id")
        ques_ans['question'] = cursor.fetchall()

        ques_ans['count'] = len(ques_ans['question'])

        cursor.execute(f"select id from {self.db}features where survey = {survey} and ans_check = 1 order by id")
        for elem in cursor.fetchall():
            cursor.execute(f"select answer from {self.db}answers where f_id = {elem[0]} order by id")
            for line in cursor.fetchall():
                ques_ans['answer'].append(line)

        return ques_ans

    def create(self, call, data_type):
        output = []
        survey = f"'{self.get_survey(call)}'"

        point_output = None
        polygon_output = None

        if data_type == 'shapefile':
            point_output = self.geom_shp(call, 'point', survey, self.ques_ans(survey))
            polygon_output = self.geom_shp(call, 'polygon', survey, self.ques_ans(survey))
        elif data_type == 'geojson':
            point_output = self.geom_gjson(call, 'point', survey, self.ques_ans(survey))
            polygon_output = self.geom_gjson(call, 'polygon', survey, self.ques_ans(survey))

        if point_output:
            output.append(point_output)

        if polygon_output:
            output.append(polygon_output)

        return output


class CreateWebMap(Survey, PointPolygon, ProcessData):
    def __init__(self, db=''):
        super().__init__(db)
        self.db = db

    def source(self, survey):
        source = {'point': {"type": "FeatureCollection", "name": "Places",
                            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
                            "features": []},
                  'polygon': {"type": "FeatureCollection", "name": "Places",
                              "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
                              "features": []}}

        cursor.execute(f"select user_name, entr_time, photo, video, st_astext(point) point, st_astext(polygon), "
                       f"id, survey from {self.db}features where survey = {survey} and ans_check = 1 order by id")
        for row in cursor.fetchall():
            elem = {"user": f"{row[0]}", "time": f"{row[1]}", "photo": f"{row[2]}", "video": f"{row[3]} ",
                    "question": "<br>"}
            if row[3]:
                elem["video"] = f'<a href="{row[3]}">Click the link.</a>'
            if row[2]:
                elem["photo"] = f'<a href="{row[2]}"><img id="Pic" src="{row[2]}"></a>'
            cursor.execute(f"select id, question from {self.db}questions where survey = '{row[7]}' order by id")
            for line in cursor.fetchall():
                cursor.execute(f"select answer from {self.db}answers where q_id = {line[0]} and f_id = {row[6]} ")
                elem["question"] = elem["question"] + f"{line[1]}: {cursor.fetchall()[0][0]}<br>"
            if row[4]:
                source['point']["features"].append({"type": "Feature", "properties": elem,
                                                    "geometry": {"type": "Point", "coordinates": self.point(row[4])}})
            elif row[5]:
                source['polygon']["features"].append({"type": "Feature", "properties": elem,
                                                      "geometry": {"type": "MultiPolygon",
                                                                   "coordinates": [[self.polygon(row[5])]]}})
        return source

    def geom_extent(self, survey):
        geom_extent = {'point': None, 'polygon': None}

        cursor.execute(f'select st_extent(point) from {self.db}features where survey = {survey} and ans_check = 1')
        geom_extent['point'] = cursor.fetchall()[0][0]

        cursor.execute(f'select st_extent(polygon) from {self.db}features where survey = {survey} and ans_check = 1')
        geom_extent['polygon'] = cursor.fetchall()[0][0]

        return geom_extent

    def map_center(self, span):
        map_center = {'center_long': 0.0, 'center_lat': 0.0, 'point1_long': -180, 'point1_lat': -90, 'point2_long': 180,
                      'point2_lat': 90}

        if span:
            point1 = span[0].split(' ')
            point2 = span[1].split(' ')
            map_center['point1_long'], map_center['point1_lat'] = float(point1[0]), float(point1[1])
            map_center['point2_long'], map_center['point2_lat'] = float(point2[0]), float(point2[1])
            map_center['center_long'] = (map_center['point1_long'] + map_center['point2_long']) / 2
            map_center['center_lat'] = (map_center['point1_lat'] + map_center['point2_lat']) / 2

        return map_center

    def adjust(self, survey, point_extent, polygon_extent):
        adjust = {}

        if point_extent is not None and polygon_extent is not None:
            cursor.execute(f'select st_extent((select st_union((select st_setsrid(st_extent(point), 4326) '
                           f'from {self.db}features where survey = {survey} and ans_check = 1),'
                           f'(select st_setsrid(st_extent(polygon), 4326) '
                           f'from {self.db}features where survey = {survey} and ans_check = 1))))')
            adjust = self.map_center(cursor.fetchall()[0][0][4:-1].split(','))
        elif point_extent is not None and polygon_extent is None:
            cursor.execute(f'select st_extent(point) from {self.db}features where survey = {survey} and ans_check = 1')
            adjust = self.map_center(cursor.fetchall()[0][0][4:-1].split(','))
        elif point_extent is None and polygon_extent is not None:
            cursor.execute(f'select st_extent(polygon) from {self.db}features where survey = {survey} and '
                           f'ans_check = 1')
            adjust = self.map_center(cursor.fetchall()[0][0][4:-1].split(','))

        return adjust

    def distance(self, adjust):
        cursor.execute(
            f"select ST_Distance('SRID=4326;POINT({adjust['point1_long']} {adjust['point1_lat']})'::geography,"
            f"'SRID=4326;POINT({adjust['point2_long']} {adjust['point2_lat']})'::geography)")
        return int(cursor.fetchall()[0][0])

    def get_scale(self, distance):
        all_scales = self.scales
        scale = 1

        for k, v in all_scales.items():
            if distance <= k:
                scale = v
                break

        return scale

    def create(self, call):
        survey = f"'{self.get_survey(call)}'"

        pp_extent = self.geom_extent(survey)
        adjust = self.adjust(survey, pp_extent['point'], pp_extent['polygon'])
        distance = self.distance(adjust)
        pp_source = self.source(survey)

        modified = map_template.html_2 % (call.from_user.first_name, str(pp_source['point']), str(pp_source['polygon']),
                                          adjust['center_lat'], adjust['center_long'], self.get_scale(distance))

        output = io.BytesIO(str.encode(map_template.html_1 + modified + map_template.html_3, 'utf-8'))
        output.name = f'{call.from_user.first_name}.html'

        return output


class Delete(Survey):
    def __init__(self, db=''):
        super().__init__(db)
        self.db = db

    def del_question(self, message):
        cursor.execute(f"delete from {self.db}questions where survey = '{self.get_survey(message)}'")
        connection.commit()

    def check_ans(self, message):
        cursor.execute(f"select ans_check from {self.db}features where id = "
                       f"(select max(id) from {self.db}features where user_id = {message.from_user.id})")
        return cursor.fetchall()[0][0]

    def del_row(self, message):
        cursor.execute(f"delete from {self.db}answers where f_id = (select max(id) from {self.db}features where "
                       f"user_id = {message.from_user.id})")
        cursor.execute(f'delete from {self.db}features where id = (select max(id) from {self.db}features where '
                       f'user_id = {message.from_user.id})')
        connection.commit()

    def del_data(self, message):
        cursor.execute(f"select id from {self.db}features where survey = '{self.get_survey(message)}' and "
                       f"ans_check = 1")
        for row in cursor.fetchall():
            cursor.execute(f"delete from {self.db}answers where f_id = {row[0]}")
            connection.commit()

        cursor.execute(f"delete from {self.db}features where survey = '{self.get_survey(message)}' and ans_check = 1")
        connection.commit()

    def del_feature(self, message):
        cursor.execute(f"delete from {self.db}features where id = (select max(id) from {self.db}features where "
                       f"user_id = {message.from_user.id})")
        connection.commit()
