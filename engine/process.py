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


# The database connection
tables = Tables()
connection = tables.connection
cursor = tables.cursor


class State:
    """The bot states operations."""

    # Get states from a data container
    states = ProcessData().states

    def __init__(self, db=''):
        """The constructor for production or
           testing."""
        self.db = db

    def show_state(self, message):
        """Return the bot state for a message/call sender,
           if there is not any state insert the initial
           one into the table and return it."""
        cursor.execute(f'select exists(select 1 from {self.db}user_state where user_id = {message.from_user.id} '
                       f'limit 1)')
        if not cursor.fetchall()[0][0]:
            cursor.execute(f"insert into {self.db}user_state values({message.from_user.id},"
                           f"'{message.from_user.first_name}', {self.states['INIT']})")
            connection.commit()

        cursor.execute(f'select user_state from {self.db}user_state where user_id = {message.from_user.id}')
        return cursor.fetchall()[0][0]

    def save_state(self, message, current_state):
        """Save the bot state for a message/call
           sender """
        cursor.execute(f'update {self.db}user_state set user_state = {current_state} where '
                       f'user_id = {message.from_user.id}')
        connection.commit()


class Survey(ProcessData):
    """Survey operations."""

    def __init__(self, db=''):
        """The constructor for production or
           testing."""
        self.db = db

    def save_survey(self, message):
        """Control the message length. Save the survey name for
           a message/call sender."""
        if len(message.text) > 25:
            return True
        else:
            cursor.execute(f"update {self.db}user_state set survey = '{self.sub(message.text.lower())}' where "              
                           f"user_id = {message.from_user.id}")
            connection.commit()

    def get_survey(self, message):
        """Get the survey name for
           a message/call sender."""
        cursor.execute(f"select survey from {self.db}user_state where user_id = {message.from_user.id}")
        return cursor.fetchall()[0][0]

    def get_author(self, message):
        """Get the author of
           a survey."""
        cursor.execute(f"select author from {self.db}questions where survey = '{self.get_survey(message)}'")
        return cursor.fetchall()[0][0]

    def survey_initial(self, message):
        """Insert the survey name for a message/call sender.
           Return the proper answer."""
        cursor.execute(f"insert into {self.db}questions (id, survey, author) values (default, "
                       f"'{self.sub(message.text.lower())}', {message.from_user.id})")
        connection.commit()

        return answers['SURVEY_SAVED'] % self.sub(message.text)

    def survey_next(self, message):
        """Get the latest question for a survey,
           if None, insert the survey name for a message/call sender."""
        cursor.execute(f"select question from {self.db}questions where id = (select max(id) from {self.db}questions "
                       f"where survey = '{self.get_survey(message)}')")
        if cursor.fetchall()[0][0]:
            cursor.execute(f"insert into {self.db}questions (id, survey, author) values (default, "
                           f"'{self.get_survey(message)}', {message.from_user.id})")
            connection.commit()

    def survey_check(self, message):
        """Control the message length. Check if the new survey name
           already exists. Return boolean."""
        if len(message.text) > 25:
            return

        cursor.execute(f"select exists (SELECT 1 FROM {self.db}questions WHERE "
                       f"survey = '{self.sub(message.text.lower())}' LIMIT 1)")
        return cursor.fetchall()[0][0]


class PointPolygon:
    """Parse point and polygon PostGIS (ST_AsText) string.
       Return the list of coordinates."""

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
    """Question and answers operations."""

    def __init__(self, db=''):
        """The constructor for production or
           testing."""
        super().__init__(db)
        self.db = db

    def ans_check(self, message):
        """Check if survey questions were answered.
           Return boolean"""
        cursor.execute(f"select exists(select 1 from {self.db}features where ans_check = 1 and "
                       f"survey = '{self.get_survey(message)}'limit 1)")
        return cursor.fetchall()[0][0]

    def init_row(self, message):
        """Insert the survey name and the first name
           for a message/call sender"""
        cursor.execute(f"insert into {self.db}features (id, user_id, user_name, survey) values (default, "
                       f"{message.from_user.id}, '{message.from_user.first_name}', '{self.get_survey(message)}')")
        connection.commit()

    def question_insert(self, message):
        """Control the message length. Get the latest question
           for a survey. If None, save the question into the
           latest row for the survey. Return the proper answer"""
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
        """Nullify the latest question for a survey"""
        cursor.execute(f"update {self.db}questions set question = null where id = (select max(id) from "
                       f"{self.db}questions where survey = '{self.get_survey(message)}')")
        connection.commit()

    def get_question(self, message):
        """Get question(s) for a survey from the questions table.
           Save the number of questions in the latest feature for a message/call sender
           in the features table. Return the first question."""
        cursor.execute(f"select id, question from {self.db}questions where survey = '{self.get_survey(message)}' "
                       f"order by id")
        result = cursor.fetchall()

        cursor.execute(f"update {self.db}features set q_count = {len(result)} where id = (select max(id) from "
                       f"{self.db}features where user_id = {message.from_user.id})")
        connection.commit()

        return result[0][1]

    def get_q_count(self, message):
        """Return the number of questions from the latest feature
           for a message/call sender."""
        cursor.execute(f"select q_count from {self.db}features where id = (select max(id) from {self.db}features where "
                       f"user_id = {message.from_user.id})")
        return cursor.fetchall()[0][0]

    def set_ans_check(self, message):
        """Save the answer check flag of the latest feature
           for a message/call sender."""
        cursor.execute(f"update {self.db}features set ans_check = 1 where id = (select max(id) from {self.db}features "
                       f"where user_id = {message.from_user.id})")
        connection.commit()

    def answer_insert(self, message, ans_num=''):
        """Control the message length. Call the get_q_count method, get the number of
           questions. Get questions for the survey from the questions table.
           Insert the foreign keys (feature id; question id, derived
           from the number of questions) and the answer for a message/call sender
           into the answers table. If the number of questions > 1, decrease it by 1
           in the features table. Return the proper answer"""
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
    """Coordinates operations."""

    def __init__(self, db=''):
        """The constructor for production or
            testing."""
        self.db = db

    def get_poly_points(self, message):
        """Return the list with coordinates of the polygon
           from the latest feature for a message/call sender"""
        cursor.execute(f"select poly_points from {self.db}features where id = (select max(id) from "
                       f"{self.db}features where user_id = {message.from_user.id})")
        return cursor.fetchall()[0][0]

    def append_poly_points(self, message, lat, long):
        """Append polygon longitude and latitude to the poly_points
           field of latest feature for a message/call sender"""
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
        """Return the number of polygon
           vertices"""
        if self.get_poly_points(message):
            return len(self.get_poly_points(message).split(','))
        else:
            return 0

    def point_manual(self, message):
        """Control the message length. In the case of the successful text
           input validation, save a point geometry and its creation time
           in the latest feature for a message/call sender.
           Return the proper answer"""
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
        """Save a point geometry derived from message.location
           and its creation time in the latest feature for
           a message/call sender. Return the proper answer"""
        lat = message.location.latitude
        long = message.location.longitude
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(f"update {self.db}features set point = ST_GeomFromText("
                       f"'POINT({long} {lat})',4326), entr_time = '{time}'"
                       f"where id = (select max(id) from {self.db}features where user_id = {message.from_user.id})")
        connection.commit()

        return answers['POINT_MEDIA'] % (lat, long)

    def polygon_manual(self, message):
        """Control the message length. In the case of the successful
           text input validation, call the append_poly_points method.
           Return the proper answer"""
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
        """Derive coordinates from message.location.
           Call the append_poly_points method. Return the proper answer"""
        lat = message.location.latitude
        long = message.location.longitude

        self.append_poly_points(message, lat, long)

        return answers['VERTEX_DONE']

    def polygon_create(self, message, poly_points):
        """Make sure that the poly_points list has
           matching the first and last elements. Save polygon and
           time in the latest feature for a message/call sender. Return
           the proper answer"""
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
    """Media operations"""

    def __init__(self, db=''):
        """The constructor for production or
           testing."""
        self.db = db

    def save_media(self, message, path, media):
        """Save generated media url in the appropriate field
           of the latest feature for a message/call sender.
           Return the appropriate answer."""
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
        """Get a saved media file from Telegram API. It contains a secret token,
           therefore can not be revealed. Save media to telegra.ph, get its url
           (it does not have any confidential information). Return the url."""
        try:
            with urllib.request.urlopen(f'https://api.telegram.org/file/bot{token}/{file_info.file_path}') as get:
                if get.getcode() == 200:
                    post = requests.post('https://telegra.ph/upload', files={'file': ('file', get, m_type)})
                    if post.status_code == 200:
                        return post.json()[0]['src']
        except:
            pass


class Shp(PointPolygon, TestID):
    """Shapefile operations."""

    def __init__(self, db=''):
        """The constructor for production or
           testing."""
        self.db = db

    # Get datum from a data container
    datum = ProcessData().datum

    def shp(self, geom_type, survey, question, answer, count):
        """Create a dictionary, were keys are names of the mandatory files of
           the shapefile format, values are empty binary objects. Using the Shapefile library
           write into the dictionary all data collected by all users under a survey.
           Return the dictionary either for point(s) or polygon(s)."""
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

            # Assigning the pre-set IDs in the test mode
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
        """Call the shp method, transfer, inter alia, a geometry type into it, get
           a dictionary with data. If it contains geometry, produce mandatory for
           the shapefile format files as file-like objects, produce a projection description.
           Assign the proper names and extensions. Return a list of created objects."""
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
    """GeoJSON operations."""

    def __init__(self, db=''):
        """The constructor for production or
           testing."""
        self.db = db

    def gjson(self, geom_type, survey, question, answer, count):
        """From all data collected by all users under a survey
           create a GeoJson using the template. Return it either
           for point(s) or polygon(s)."""
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

            # Assigning the pre-set IDs in the test mode
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
        """Call the gjson method, transfer, inter alia, a geometry type into it, get
           a GeoJson. If it contains geometry, produce a file-like object,
           assign the proper name and extension, return it."""
        result = self.gjson(geom_type, survey, data['question'], data['answer'], data['count'])

        if result['check'] == 1:
            output = io.BytesIO(json.dumps(result['result']).encode('utf-8'))
            output.name = f'{call.from_user.first_name}_{geom_type}.geojson'
            return output


class CreateGJsonShp(Survey, GeoJson, Shp):
    """Shapefile and/or GeoJSON creation"""

    def __init__(self, db=''):
        """The constructor for production or
           testing."""
        super().__init__(db)
        self.db = db

    def ques_ans(self, survey):
        """Return the dictionary of questions and
           all answers for a survey, collected by all users."""
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
        """Return a list of shapefile(s) or GeoJSON(s) for point(s)
           and/or polygon(s) as file-like objects."""
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
    """Web Map creation"""

    def __init__(self, db=''):
        """The constructor for production or
           testing."""
        super().__init__(db)
        self.db = db

    def source(self, survey):
        """Return a dictionary containing Web Map specific GeoJSONs
           for both point(s) anb polygon(s) with all data collected by
           all users under a survey."""
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
        """Return a dictionary with the spatial extent for
           all point(s) and/or polygon(s), collected by all users under a survey."""
        geom_extent = {'point': None, 'polygon': None}

        cursor.execute(f'select st_extent(point) from {self.db}features where survey = {survey} and ans_check = 1')
        geom_extent['point'] = cursor.fetchall()[0][0]

        cursor.execute(f'select st_extent(polygon) from {self.db}features where survey = {survey} and ans_check = 1')
        geom_extent['polygon'] = cursor.fetchall()[0][0]

        return geom_extent

    def map_center(self, span):
        """Return a dictionary with the center and two marginal points
           of an area, derived from the entered data."""
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
        """Return the spatially adjusted area, encompassing all collected
           by all users geometries under a survey"""
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
        """Return the distance between the
           two farthest points of an adjusted area"""
        cursor.execute(
            f"select ST_Distance('SRID=4326;POINT({adjust['point1_long']} {adjust['point1_lat']})'::geography,"
            f"'SRID=4326;POINT({adjust['point2_long']} {adjust['point2_lat']})'::geography)")
        return int(cursor.fetchall()[0][0])

    def get_scale(self, distance):
        """Return the scale derived
           from a distance"""
        all_scales = self.scales
        scale = 1

        for k, v in all_scales.items():
            if distance <= k:
                scale = v
                break

        return scale

    def create(self, call):
        """Call the listed below methods for a survey.
           Insert the results into the HTML/CSS/JavaScript template, containing
           the Leaflet map. Produce a file-like object, assign the proper name and extension,
           return it."""
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
    """Delete operations"""

    def __init__(self, db=''):
        """The constructor for production or
           testing."""
        super().__init__(db)
        self.db = db

    def del_question(self, message):
        """Delete questions for
           a survey"""
        cursor.execute(f"delete from {self.db}questions where survey = '{self.get_survey(message)}'")
        connection.commit()

    def check_ans(self, message):
        """Check if the latest feature for a
           message/call sender has the answered questions."""
        cursor.execute(f"select ans_check from {self.db}features where id = "
                       f"(select max(id) from {self.db}features where user_id = {message.from_user.id})")
        return cursor.fetchall()[0][0]

    def del_row(self, message):
        """Delete the latest feature and the associated answers
           for a message/call sender from the features and answers tables."""
        cursor.execute(f"delete from {self.db}answers where f_id = (select max(id) from {self.db}features where "
                       f"user_id = {message.from_user.id})")
        cursor.execute(f'delete from {self.db}features where id = (select max(id) from {self.db}features where '
                       f'user_id = {message.from_user.id})')
        connection.commit()

    def del_data(self, message):
        """Delete all features and the associated answers
           for a survey from features and answers tables."""
        cursor.execute(f"select id from {self.db}features where survey = '{self.get_survey(message)}' and "
                       f"ans_check = 1")
        for row in cursor.fetchall():
            cursor.execute(f"delete from {self.db}answers where f_id = {row[0]}")
            connection.commit()

        cursor.execute(f"delete from {self.db}features where survey = '{self.get_survey(message)}' and ans_check = 1")
        connection.commit()

    def del_feature(self, message):
        """Delete the latest feature for
           a message/call sender."""
        cursor.execute(f"delete from {self.db}features where id = (select max(id) from {self.db}features where "
                       f"user_id = {message.from_user.id})")
        connection.commit()
