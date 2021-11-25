import datetime
from engine.utils.utils import DotDict


class Data:
    num = 0

    @property
    def data_ques_ans(self):
        return {'question': [(f'question{self.num}_1',), (f'question{self.num}_2',)],
                'answer': [(f'answer{self.num}_1',), (f'answer{self.num}_2',),
                           (f'answer{self.num}_1',), (f'answer{self.num}_2',),
                           (f'answer{self.num + 1}_1',), (f'answer{self.num + 1}_2',),
                           (f'answer{self.num + 2}_1',), (f'answer{self.num + 2}_2',)],
                'count': 2}

    @property
    def data_question(self):
        return [(f'question{self.num}_1',), (f'question{self.num}_2',)]

    @property
    def data_double_answer(self):
        return [(f'answer{self.num}_1',), (f'answer{self.num}_2',),
                (f'answer{self.num}_1',), (f'answer{self.num}_2',),
                (f'answer{self.num + 1}_1',), (f'answer{self.num + 1}_2',),
                (f'answer{self.num + 2}_1',), (f'answer{self.num + 2}_2',),
                (f'answer{self.num}_1',), (f'answer{self.num}_2',),
                (f'answer{self.num}_1',), (f'answer{self.num}_2',),
                (f'answer{self.num + 1}_1',), (f'answer{self.num + 1}_2',),
                (f'answer{self.num + 2}_1',), (f'answer{self.num + 2}_2',)]

    @property
    def data_credentials(self):
        return 'postgres://bot:1234@localhost:5432/test_db'

    @property
    def data_states(self):
        return {'INIT': 1, 'SURVEY1': 2, 'SURVEY2': 3, 'SURVEY3': 4, 'COLLECT': 5, 'POINT': 6, 'POLYGON': 7,
                'TRANSIT': 8, 'MEDIA1': 9, 'MEDIA2': 10, 'QUESTION1': 11, 'QUESTION2': 12, 'ANSWER': 13, 'CHECK1': 14,
                'CHECK2': 15, 'SUBMIT': 16, 'RESULT': 17}

    @property
    def data_point(self):
        return 'POINT(45 45)'

    @property
    def data_polygon(self):
        return 'POLYGON((46 45,47 46,48 47,45 48,46 45))'

    @property
    def data_ans_check(self):
        return [1, 'null']

    @property
    def data_get_question(self):
        return 10

    @property
    def data_get_q_count(self):
        return [25, 29]

    @property
    def data_set_ans_check(self):
        return 11

    @property
    def data_answer_insert(self):
        return [[3, 2, 1], ['_1', '_2', '_3']]

    @property
    def data_get_pp(self):
        return '54.0 54.0, 45.0 46.0, 50.0 56.0'

    @property
    def data_append_pp(self):
        return [[True, '54.0 54.0', None], '48.0', '58.0']

    @property
    def data_get_count(self):
        return [True, '54.0 54.0, 45.0 46.0, 50.0 56.0', None]

    @property
    def data_point_polygon_manual(self):
        return ['12345 qwerty', '12345, qwerty', '-89, 179', '91, -181', '91, 179', '0, 181']

    @property
    def data_point_polygon_location(self):
        return [-89, 179]

    @property
    def data_polygon_create(self):
        return '54.35 54,45 46,50 56'

    @property
    def data_time(self):
        return datetime.datetime.now().strftime("%Y")

    @property
    def data_save_media(self):
        return '/test_path'

    @property
    def data_media_path(self):
        file_info = DotDict({'file_path': 1034})

        return ['1234', file_info, 'media']

    @property
    def data_map_center(self):
        return [['-45 -45', '70 45'], ['-45 -45', '45 45'], ['-40 -30', '70 30']]

    @property
    def data_adjust(self):
        return ['BOX(-45 -45,45 45)', 'BOX(-40 -30,70 30)']

    @property
    def data_get_scale(self):
        return [19, 599999, 13389850]

    @property
    def data_gjson_shp(self):
        return [[572000, 371], [372, 573000]]

    @property
    def data_count(self):
        return 2

    @property
    def data_distance(self):
        return 15038278

    @property
    def data_scale(self):
        return 1

    @property
    def data_double_point(self):
        return [[45.0, 45.0], [-45.0, -45.0]]

    @property
    def data_double_polygon(self):
        return [[[30.0, 30.0], [-30.0, -30.0], [10.0, 20.0], [30.0, 30.0]],
                [[40.0, 10.0], [-40.0, -10.0], [70.0, 20.0], [40.0, 10.0]]]

    @property
    def data_quad_point(self):
        return [[45.0, 45.0], [-45.0, -45.0], [45.0, 45.0], [-45.0, -45.0]]

    @property
    def data_quad_polygon(self):
        return [[[30.0, 30.0], [-30.0, -30.0], [10.0, 20.0], [30.0, 30.0]],
                [[40.0, 10.0], [-40.0, -10.0], [70.0, 20.0], [40.0, 10.0]],
                [[30.0, 30.0], [-30.0, -30.0], [10.0, 20.0], [30.0, 30.0]],
                [[40.0, 10.0], [-40.0, -10.0], [70.0, 20.0], [40.0, 10.0]]]

    @property
    def data_extent(self):
        return {'point': 'BOX(-45 -45,45 45)', 'polygon': 'BOX(-40 -30,70 30)'}

    @property
    def data_triple_map_center(self):
        return [{'center_long': 12.5, 'center_lat': 0.0, 'point1_long': -45.0, 'point1_lat': -45.0, 'point2_long': 70.0,
                 'point2_lat': 45.0},
                {'center_long': 0.0, 'center_lat': 0.0, 'point1_long': -45.0, 'point1_lat': -45.0, 'point2_long': 45.0,
                 'point2_lat': 45.0},
                {'center_long': 15.0, 'center_lat': 0.0, 'point1_long': -40.0, 'point1_lat': -30.0, 'point2_long': 70.0,
                 'point2_lat': 30.0}]

    @property
    def data_webmap(self):
        return  {'point': {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'},
                                   'type': 'name'},
                           'features': [{'geometry': {'coordinates': [45.0, 45.0],
                                                      'type': 'Point'},
                                         'properties': {'photo': '<a '
                                                                 'href="https://telegra.ph/test_path_photo35"><img '
                                                                 'id="Pic" '
                                                                 'src="https://telegra.ph/test_path_photo35"></a>',
                                                        'question': '<br>question35_1: '
                                                                    'answer35_1<br>question35_2: '
                                                                    'answer35_2<br>',
                                                        'time': '2021-11-20 22:45:00',
                                                        'user': 'Name35',
                                                        'video': '<a '
                                                                 'href="https://telegra.ph/test_path_video35">Click '
                                                                 'the link.</a>'},
                                         'type': 'Feature'},
                                        {'geometry': {'coordinates': [-45.0, -45.0],
                                                      'type': 'Point'},
                                         'properties': {'photo': 'None',
                                                        'question': '<br>question35_1: '
                                                                    'answer35_1<br>question35_2: '
                                                                    'answer35_2<br>',
                                                        'time': '2021-11-20 22:45:00',
                                                        'user': 'Name35',
                                                        'video': 'None '},
                                         'type': 'Feature'}],
                           'name': 'Places',
                           'type': 'FeatureCollection'},
                 'polygon': {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'},
                                     'type': 'name'},
                             'features': [{'geometry': {'coordinates': [[[[30.0, 30.0],
                                                                          [-30.0, -30.0],
                                                                          [10.0, 20.0],
                                                                          [30.0, 30.0]]]],
                                                        'type': 'MultiPolygon'},
                                           'properties': {'photo': '<a '
                                                                   'href="https://telegra.ph/test_path_photo36"><img '
                                                                   'id="Pic" '
                                                                   'src="https://telegra.ph/test_path_photo36"></a>',
                                                          'question': '<br>question35_1: '
                                                                      'answer36_1<br>question35_2: '
                                                                      'answer36_2<br>',
                                                          'time': '2021-11-20 22:45:00',
                                                          'user': 'Name36',
                                                          'video': '<a '
                                                                   'href="https://telegra.ph/test_path_video36">Click '
                                                                   'the link.</a>'},
                                           'type': 'Feature'},
                                          {'geometry': {'coordinates': [[[[40.0, 10.0],
                                                                          [-40.0, -10.0],
                                                                          [70.0, 20.0],
                                                                          [40.0, 10.0]]]],
                                                        'type': 'MultiPolygon'},
                                           'properties': {'photo': '<a '
                                                                   'href="https://telegra.ph/test_path_photo37"><img '
                                                                   'id="Pic" '
                                                                   'src="https://telegra.ph/test_path_photo37"></a>',
                                                          'question': '<br>question35_1: '
                                                                      'answer37_1<br>question35_2: '
                                                                      'answer37_2<br>',
                                                          'time': '2021-11-20 22:45:00',
                                                          'user': 'Name37',
                                                          'video': '<a '
                                                                   'href="https://telegra.ph/test_path_video37">Click '
                                                                   'the link.</a>'},
                                           'type': 'Feature'}],
                             'name': 'Places',
                             'type': 'FeatureCollection'}}

    @property
    def data_geom_gjson_point(self):
        return  {'check': 1,
                 'result': {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'},
                                    'type': 'name'},
                            'features': [{'geometry': {'coordinates': [45.0, 45.0],
                                                       'type': 'Point'},
                                          'properties': {'ans_1': 'answer47_1',
                                                         'ans_2': 'answer47_2',
                                                         'entr_time': '2021-11-20 22:45:00',
                                                         'id': 22,
                                                         'photo': 'https://telegra.ph/test_path_photo47',
                                                         'quest_1': 'question47_1',
                                                         'quest_2': 'question47_2',
                                                         'survey': 'survey47',
                                                         'user_name': 'Name47',
                                                         'video': 'https://telegra.ph/test_path_video47'},
                                          'type': 'Feature'},
                                         {'geometry': {'coordinates': [-45.0, -45.0],
                                                       'type': 'Point'},
                                          'properties': {'ans_1': 'answer47_1',
                                                         'ans_2': 'answer47_2',
                                                         'entr_time': '2021-11-20 22:45:00',
                                                         'id': 23,
                                                         'photo': 'None',
                                                         'quest_1': 'question47_1',
                                                         'quest_2': 'question47_2',
                                                         'survey': 'survey47',
                                                         'user_name': 'Name47',
                                                         'video': 'None'},
                                          'type': 'Feature'}],
                            'name': 'Places',
                            'type': 'FeatureCollection'}}

    @property
    def data_geom_gjson_polygon(self):
        return  {'check': 1,
                 'result': {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'},
                                    'type': 'name'},
                            'features': [{'geometry': {'coordinates': [[[[30.0, 30.0],
                                                                         [-30.0, -30.0],
                                                                         [10.0, 20.0],
                                                                         [30.0, 30.0]]]],
                                                       'type': 'MultiPolygon'},
                                          'properties': {'ans_1': 'answer48_1',
                                                         'ans_2': 'answer48_2',
                                                         'entr_time': '2021-11-20 22:45:00',
                                                         'id': 24,
                                                         'photo': 'https://telegra.ph/test_path_photo48',
                                                         'quest_1': 'question47_1',
                                                         'quest_2': 'question47_2',
                                                         'survey': 'survey47',
                                                         'user_name': 'Name48',
                                                         'video': 'https://telegra.ph/test_path_video48'},
                                          'type': 'Feature'},
                                         {'geometry': {'coordinates': [[[[40.0, 10.0],
                                                                         [-40.0, -10.0],
                                                                         [70.0, 20.0],
                                                                         [40.0, 10.0]]]],
                                                       'type': 'MultiPolygon'},
                                          'properties': {'ans_1': 'answer49_1',
                                                         'ans_2': 'answer49_2',
                                                         'entr_time': '2021-11-20 22:45:00',
                                                         'id': 25,
                                                         'photo': 'https://telegra.ph/test_path_photo49',
                                                         'quest_1': 'question47_1',
                                                         'quest_2': 'question47_2',
                                                         'survey': 'survey47',
                                                         'user_name': 'Name49',
                                                         'video': 'https://telegra.ph/test_path_video49'},
                                          'type': 'Feature'}],
                            'name': 'Places',
                            'type': 'FeatureCollection'}}

    @property
    def data_geom_shp_point(self):
        return  {'check': 1,
                 'dbf': b'\x03y\x0b\x16\x02\x00\x00\x00a\x01\xf5\x01\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'ID\x00\x00\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00USER_NAME\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00SURVEY\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                        b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00TIME'
                        b'\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PHOTO\x00\x00\x00'
                        b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00VIDEO\x00\x00\x00\x00\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00QUEST_1\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ANS_1\x00\x00\x00'
                        b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00QUEST_2\x00\x00\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00ANS_2\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                        b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r 37'
                        b'                                                Name53              '
                        b'                              survey53                              '
                        b'            20-Nov-2021 22:45:00                              https:'
                        b'//telegra.ph/test_path_photo53              https://telegra.ph/test_'
                        b'path_video53              question53_1                              '
                        b'        answer53_1                                        question53'
                        b'_2                                      answer53_2                  '
                        b'                       38                                           '
                        b'     Name53                                            survey53     '
                        b'                                     20-Nov-2021 22:45:00           '
                        b'                                                                    '
                        b'                                                   question53_1     '
                        b'                                 answer53_1                         '
                        b'               question53_2                                      ans'
                        b'wer53_2                                        ',
                 'shp': b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00N\xe8\x03\x00\x00'
                        b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00'
                        b'\x00\x80F\xc0\x00\x00\x00\x00\x00\x80F@\x00\x00\x00\x00\x00\x80F@'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01\x00\x00\x00\n\x01\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x80F@\x00\x00\x00\x00\x00\x80F@\x00\x00\x00\x02\x00\x00\x00\n'
                        b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00'
                        b'\x00\x80F\xc0',
                 'shx': b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00:\xe8\x03\x00\x00'
                        b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00'
                        b'\x00\x80F\xc0\x00\x00\x00\x00\x00\x80F@\x00\x00\x00\x00\x00\x80F@'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x002\x00\x00\x00\n\x00\x00\x00@\x00\x00\x00\n'}

    @property
    def data_geom_shp_polygon(self):
        return  {'check': 1,
                 'dbf': b'\x03y\x0b\x16\x02\x00\x00\x00a\x01\xf5\x01\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'ID\x00\x00\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00USER_NAME\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00SURVEY\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                        b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00TIME'
                        b'\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PHOTO\x00\x00\x00'
                        b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00VIDEO\x00\x00\x00\x00\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00QUEST_1\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ANS_1\x00\x00\x00'
                        b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00QUEST_2\x00\x00\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00ANS_2\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                        b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r 39'
                        b'                                                Name54              '
                        b'                              survey53                              '
                        b'            20-Nov-2021 22:45:00                              https:'
                        b'//telegra.ph/test_path_photo54              https://telegra.ph/test_'
                        b'path_video54              question53_1                              '
                        b'        answer54_1                                        question53'
                        b'_2                                      answer54_2                  '
                        b'                       40                                           '
                        b'     Name55                                            survey53     '
                        b'                                     20-Nov-2021 22:45:00           '
                        b'                   https://telegra.ph/test_path_photo55             '
                        b' https://telegra.ph/test_path_video55              question53_1     '
                        b'                                 answer55_1                         '
                        b'               question53_2                                      ans'
                        b'wer55_2                                        ',
                 'shp': b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xaa\xe8\x03\x00\x00'
                        b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00'
                        b'\x00\x00>\xc0\x00\x00\x00\x00\x00\x80Q@\x00\x00\x00\x00\x00\x00>@'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01\x00\x00\x008\x05\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00>\xc0\x00\x00\x00\x00\x00\x00>\xc0\x00\x00\x00\x00\x00\x00>@'
                        b'\x00\x00\x00\x00\x00\x00>@\x01\x00\x00\x00\x04\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00\x00\x00>@'
                        b'\x00\x00\x00\x00\x00\x00>\xc0\x00\x00\x00\x00\x00\x00>\xc0'
                        b'\x00\x00\x00\x00\x00\x00$@\x00\x00\x00\x00\x00\x004@\x00\x00\x00\x00'
                        b'\x00\x00>@\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x02\x00\x00\x008'
                        b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00'
                        b'\x00\x00$\xc0\x00\x00\x00\x00\x00\x80Q@\x00\x00\x00\x00\x00\x004@'
                        b'\x01\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00D@\x00\x00\x00\x00\x00\x00$@\x00\x00\x00\x00\x00\x00D\xc0'
                        b'\x00\x00\x00\x00\x00\x00$\xc0\x00\x00\x00\x00\x00\x80Q@'
                        b'\x00\x00\x00\x00\x00\x004@\x00\x00\x00\x00\x00\x00D@\x00\x00\x00\x00'
                        b'\x00\x00$@',
                 'shx': b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00:\xe8\x03\x00\x00'
                        b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00'
                        b'\x00\x00>\xc0\x00\x00\x00\x00\x00\x80Q@\x00\x00\x00\x00\x00\x00>@'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x002\x00\x00\x008\x00\x00\x00n\x00\x00\x008'}


class Result:
    num = 0

    @property
    def result_ques_ans(self):
        return {'question': [(f'question{self.num}_1',), (f'question{self.num}_2',)],
                'answer': [(f'answer{self.num}_1',), (f'answer{self.num}_2',),
                           (f'answer{self.num}_1',), (f'answer{self.num}_2',),
                           (f'answer{self.num + 1}_1',), (f'answer{self.num + 1}_2',),
                           (f'answer{self.num + 2}_1',), (f'answer{self.num + 2}_2',)],
                'count': 2}

    @property
    def result_credentials(self):
        return {'NAME': 'test_db', 'USER': 'bot', 'PASSWORD': '1234', 'HOST': 'localhost', 'PORT': '5432'}

    @property
    def result_states(self):
        return {'INIT': 1, 'SURVEY1': 2, 'SURVEY2': 3, 'SURVEY3': 4, 'COLLECT': 5, 'POINT': 6, 'POLYGON': 7,
                'TRANSIT': 8, 'MEDIA1': 9, 'MEDIA2': 10, 'QUESTION1': 11, 'QUESTION2': 12, 'ANSWER': 13, 'CHECK1': 14,
                'CHECK2': 15, 'SUBMIT': 16, 'RESULT': 17}

    @property
    def result_point(self):
        return [45.0, 45.0]

    @property
    def result_polygon(self):
        return [[46.0, 45.0], [47.0, 46.0], [48.0, 47.0], [45.0, 48.0], [46.0, 45.0]]

    @property
    def result_count(self):
        return 2

    @property
    def result_get_q_count(self):
        return 29

    @property
    def result_set_ans_check(self):
        return 1

    @property
    def result_ans_check(self):
        return [1, 'null']

    @property
    def result_answer_insert(self):
        return [2, 3]

    @property
    def result_get_pp(self):
        return '54.0 54.0, 45.0 46.0, 50.0 56.0'

    @property
    def result_append_pp(self):
        return ['54.0 54.0,58.0 48.0', '58.0 48.0']

    @property
    def result_get_count(self):
        return [3, 0]

    @property
    def result_point_manual(self):
        return ('POINT(179 -89)', datetime.datetime.now().strftime("%Y"))

    @property
    def result_polygon_create(self):
        return ("POLYGON((54.35 54,45 46,50 56,54.35 54))", datetime.datetime.now().strftime("%Y"))

    @property
    def result_save_media(self):
        return 'https://telegra.ph/test_path'

    @property
    def result_media_path(self):
        return 'https://telegra.ph/test_path'

    @property
    def result_extent(self):
        return {'point': 'BOX(-45 -45,45 45)', 'polygon': 'BOX(-40 -30,70 30)'}

    @property
    def result_triple_map_center(self):
        return [{'center_long': 12.5, 'center_lat': 0.0, 'point1_long': -45.0, 'point1_lat': -45.0, 'point2_long': 70.0,
                 'point2_lat': 45.0},
                {'center_long': 0.0, 'center_lat': 0.0, 'point1_long': -45.0, 'point1_lat': -45.0, 'point2_long': 45.0,
                 'point2_lat': 45.0},
                {'center_long': 15.0, 'center_lat': 0.0, 'point1_long': -40.0, 'point1_lat': -30.0, 'point2_long': 70.0,
                 'point2_lat': 30.0}]

    @property
    def result_distance(self):
        return [15038278, 13324945, 13389850]

    @property
    def result_get_scale(self):
        return [19, 6, 1]

    @property
    def result_gjson_shp(self):
        return [[572000, 371], [372, 573000]]

    @property
    def result_source_webmap(self):
        return  {'point': {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'},
                                   'type': 'name'},
                           'features': [{'geometry': {'coordinates': [45.0, 45.0],
                                                      'type': 'Point'},
                                         'properties': {'photo': '<a '
                                                                 'href="https://telegra.ph/test_path_photo26"><img '
                                                                 'id="Pic" '
                                                                 'src="https://telegra.ph/test_path_photo26"></a>',
                                                        'question': '<br>question26_1: '
                                                                    'answer26_1<br>question26_2: '
                                                                    'answer26_2<br>',
                                                        'time': '2021-11-20 22:45:00',
                                                        'user': 'Name26',
                                                        'video': '<a '
                                                                 'href="https://telegra.ph/test_path_video26">Click '
                                                                 'the link.</a>'},
                                         'type': 'Feature'},
                                        {'geometry': {'coordinates': [-45.0, -45.0],
                                                      'type': 'Point'},
                                         'properties': {'photo': 'None',
                                                        'question': '<br>question26_1: '
                                                                    'answer26_1<br>question26_2: '
                                                                    'answer26_2<br>',
                                                        'time': '2021-11-20 22:45:00',
                                                        'user': 'Name26',
                                                        'video': 'None '},
                                         'type': 'Feature'}],
                           'name': 'Places',
                           'type': 'FeatureCollection'},
                 'polygon': {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'},
                                     'type': 'name'},
                             'features': [{'geometry': {'coordinates': [[[[30.0, 30.0],
                                                                          [-30.0, -30.0],
                                                                          [10.0, 20.0],
                                                                          [30.0, 30.0]]]],
                                                        'type': 'MultiPolygon'},
                                           'properties': {'photo': '<a '
                                                                   'href="https://telegra.ph/test_path_photo27"><img '
                                                                   'id="Pic" '
                                                                   'src="https://telegra.ph/test_path_photo27"></a>',
                                                          'question': '<br>question26_1: '
                                                                      'answer27_1<br>question26_2: '
                                                                      'answer27_2<br>',
                                                          'time': '2021-11-20 22:45:00',
                                                          'user': 'Name27',
                                                          'video': '<a '
                                                                   'href="https://telegra.ph/test_path_video27">Click '
                                                                   'the link.</a>'},
                                           'type': 'Feature'},
                                          {'geometry': {'coordinates': [[[[40.0, 10.0],
                                                                          [-40.0, -10.0],
                                                                          [70.0, 20.0],
                                                                          [40.0, 10.0]]]],
                                                        'type': 'MultiPolygon'},
                                           'properties': {'photo': '<a '
                                                                   'href="https://telegra.ph/test_path_photo28"><img '
                                                                   'id="Pic" '
                                                                   'src="https://telegra.ph/test_path_photo28"></a>',
                                                          'question': '<br>question26_1: '
                                                                      'answer28_1<br>question26_2: '
                                                                      'answer28_2<br>',
                                                          'time': '2021-11-20 22:45:00',
                                                          'user': 'Name28',
                                                          'video': '<a '
                                                                   'href="https://telegra.ph/test_path_video28">Click '
                                                                   'the link.</a>'},
                                           'type': 'Feature'}],
                             'name': 'Places',
                             'type': 'FeatureCollection'}}

    @property
    def result_webmap(self):
        return  (b'<!doctype html>\n<html lang="en">\n<head>\n    <link rel="stylesheet" href='
                 b'"https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"\n          integrity="'
                 b'sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZ'
                 b'MZ19scR4PsZChSR7A=="\n          crossorigin=""/>\n    <style>\n        body'
                 b'{background-color: #3d85c6;}\n        #main {\n            height: 84vh;\n '
                 b'           width: 90vw;\n            margin: 0;\n            position: abs'
                 b'olute;\n            top: 50%;\n            left: 50%;\n            -ms-tran'
                 b'sform: translate(-50%, -50%);\n            transform: translate(-50%, -50'
                 b'%);\n        }\n        .mapid{\n            height: 79vh;\n            widt'
                 b'h: 90vw;\n        }\n        #Pic{\n            width: 100%;\n        }\n'
                 b'        #topbar{            \n            margin-left: auto;\n            '
                 b'margin-right: auto;\n            left: 0;\n            right: 0;\n         '
                 b'   text-align: center; \n            padding: 1px;\n            color: whi'
                 b'te;           \n        }\n    </style>\n    <script src="https://unpkg.com'
                 b'/leaflet@1.7.1/dist/leaflet.js"\n            integrity="sha512-XQoYMqMTK8'
                 b'LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA'
                 b'=="\n            crossorigin=""></script>\n    <title>Telegram bot</title>'
                 b'\n</head>\n<body>\n    <div id = main>\n    <div id="topbar"><b>Name35</b>, '
                 b'click an object for the popup</div>\n    <div id="mapid" class="mapid"></'
                 b'div>\n    </div>    \n<script>\n    "use strict"\n    var Source_point ='
                 b" {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'}, 'type': '"
                 b"name'}, 'features': [{'geometry': {'coordinates': [45.0, 45.0], 'type': 'Poi"
                 b'nt\'}, \'properties\': {\'photo\': \'<a href="https://telegra.ph/test_path'
                 b'_photo35"><img id="Pic" src="https://telegra.ph/test_path_photo35"></a>\''
                 b", 'question': '<br>question35_1: answer35_1<br>question35_2: answer35_2<br>'"
                 b", 'time': '2021-11-20 22:45:00', 'user': 'Name35', 'video': '<a href"
                 b'="https://telegra.ph/test_path_video35">Click the link.</a>\'}, \'type\': \''
                 b"Feature'}, {'geometry': {'coordinates': [-45.0, -45.0], 'type': 'Point'}, 'p"
                 b"roperties': {'photo': 'None', 'question': '<br>question35_1: answer35_1<br>q"
                 b"uestion35_2: answer35_2<br>', 'time': '2021-11-20 22:45:00', 'user': 'Name35"
                 b"', 'video': 'None '}, 'type': 'Feature'}], 'name': 'Places', 'type': 'Featur"
                 b"eCollection'};\n    var Source_polygon = {'crs': {'properties': {'name': "
                 b"'urn:ogc:def:crs:OGC:1.3:CRS84'}, 'type': 'name'}, 'features': [{'geometry':"
                 b" {'coordinates': [[[[30.0, 30.0], [-30.0, -30.0], [10.0, 20.0], [30.0, 30.0]"
                 b']]], \'type\': \'MultiPolygon\'}, \'properties\': {\'photo\': \'<a href="'
                 b'https://telegra.ph/test_path_photo36"><img id="Pic" src="https://telegra.ph/'
                 b'test_path_photo36"></a>\', \'question\': \'<br>question35_1: answer36_1<br>q'
                 b"uestion35_2: answer36_2<br>', 'time': '2021-11-20 22:45:00', 'user': 'Name36"
                 b'\', \'video\': \'<a href="https://telegra.ph/test_path_video36">Click the li'
                 b"nk.</a>'}, 'type': 'Feature'}, {'geometry': {'coordinates': [[[[40.0, 10.0],"
                 b" [-40.0, -10.0], [70.0, 20.0], [40.0, 10.0]]]], 'type': 'MultiPolygon'}, 'pr"
                 b'operties\': {\'photo\': \'<a href="https://telegra.ph/test_path_photo37"><im'
                 b'g id="Pic" src="https://telegra.ph/test_path_photo37"></a>\', \'question\':'
                 b" '<br>question35_1: answer37_1<br>question35_2: answer37_2<br>', 'time': '20"
                 b'21-11-20 22:45:00\', \'user\': \'Name37\', \'video\': \'<a href="https://tel'
                 b'egra.ph/test_path_video37">Click the link.</a>\'}, \'type\': \'Feature\'}'
                 b"], 'name': 'Places', 'type': 'FeatureCollection'};\n    var map = L.map('"
                 b"mapid', {\n        center: [0.000000,12.500000],\n        zoom: 1\n    });\n"
                 b"    var CartoDB_Positron = L.tileLayer('https://{s}.basemaps.cartocdn.com/li"
                 b'ght_all/{z}/{x}/{y}{r}.png\', {\n        attribution: \'&copy; <a href="htt'
                 b'ps://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; '
                 b'\' +\n            \'<a href="https://carto.com/attributions">CARTO</a>\''
                 b",\n        subdomains: 'abcd',\n        maxZoom: 19\n    }).addTo(map);\n   "
                 b" var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS"
                 b"/rest/services/World_Imagery/'+\n    'MapServer/tile/{z}/{y}/{x}', {\tattr"
                 b"ibution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX,'"
                 b"+\n    'GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User"
                 b" Community'\n    });\n    var Points = L.geoJSON(Source_point,{\n        po"
                 b'intToLayer: function (feature, latlng) {\n            return L.marker(lat'
                 b"lng, {icon: L.icon({\n                    iconUrl: 'https://telegra.ph/fi"
                 b"le/bc24c001d928ca59c469d.png',\n                    iconSize: [20, 20],\n "
                 b'                   iconAnchor: [10, 10],\n                    popupAnchor'
                 b': [0, -10]\n                })})\n        },\n        onEachFeature: functi'
                 b'on(feature, layer) {\n            layer.bindPopup(`\n            <p><b>Nam'
                 b'e:</b> ${feature.properties.user}\n            <br>\n            <b>Date/T'
                 b'ime (non-local):</b> ${feature.properties.time}\n            <br>\n       '
                 b'     <b>Question:</b> ${feature.properties.question}            \n       '
                 b'     <b>Latitude:</b> <i>${feature.geometry.coordinates[1].toFixed(4)}</'
                 b'i>,\n            <b>Longitude:</b> <i>${feature.geometry.coordinates[0].t'
                 b'oFixed(4)}</i>\n            <br>\n            <b>Video:</b> ${feature.prop'
                 b'erties.video}           \n            <br>\n            <b>Photo:</b> ${fe'
                 b'ature.properties.photo}\n            </p>`);\n        }\n    }).addTo(map);'
                 b'\n\n    var Polygons = L.geoJSON(Source_polygon,\n        {style: {},\n     '
                 b'   onEachFeature: function(feature, layer) {\n            layer.bindPopup'
                 b'(`\n            <p><b>Name:</b> ${feature.properties.user}\n            <b'
                 b'r>\n            <b>Date/Time (non-local):</b> ${feature.properties.time}\n'
                 b'            <br>\n            <b>Question:</b> ${feature.properties.quest'
                 b'ion}\n            <b>Video:</b> ${feature.properties.video}           \n  '
                 b'          <br>\n            <b>Photo:</b> ${feature.properties.photo}\n   '
                 b'         </p>`);\n        }    \n    }).addTo(map);\n\n    var baseMaps '
                 b'= {\n        "Map": CartoDB_Positron,\n        "Imagery": Esri_WorldImager'
                 b'y\n    };\n    var vectorL = {\n        "Points": Points,\n        "Polygons'
                 b'":Polygons\n    };\n    L.control.layers(baseMaps,vectorL).addTo(map);\n   '
                 b' var count = 0\n    var scbr = L.control.scale({imperial:false})\n    map.'
                 b'addEventListener("zoomend",function (){\n        if (map.getZoom() > 5 &&'
                 b' count === 0){\n            scbr.addTo(map);\n            count ++;\n      '
                 b'  }\n        else if (map.getZoom() <= 5) {\n            scbr.remove();\n  '
                 b'          count = 0;\n        }\n    })\n</script>\n</body>\n</html> ')

    @property
    def result_gjson_point(self):
        return  {'check': 1,
                 'result': {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'},
                                    'type': 'name'},
                            'features': [{'geometry': {'coordinates': [45.0, 45.0],
                                                       'type': 'Point'},
                                          'properties': {'ans_1': 'answer44_1',
                                                         'ans_2': 'answer44_2',
                                                         'entr_time': '2021-11-20 22:45:00',
                                                         'id': 22,
                                                         'photo': 'https://telegra.ph/test_path_photo44',
                                                         'quest_1': 'question44_1',
                                                         'quest_2': 'question44_2',
                                                         'survey': 'survey44',
                                                         'user_name': 'Name44',
                                                         'video': 'https://telegra.ph/test_path_video44'},
                                          'type': 'Feature'},
                                         {'geometry': {'coordinates': [-45.0, -45.0],
                                                       'type': 'Point'},
                                          'properties': {'ans_1': 'answer44_1',
                                                         'ans_2': 'answer44_2',
                                                         'entr_time': '2021-11-20 22:45:00',
                                                         'id': 23,
                                                         'photo': 'None',
                                                         'quest_1': 'question44_1',
                                                         'quest_2': 'question44_2',
                                                         'survey': 'survey44',
                                                         'user_name': 'Name44',
                                                         'video': 'None'},
                                          'type': 'Feature'}],
                            'name': 'Places',
                            'type': 'FeatureCollection'}}

    @property
    def result_gjson_polygon(self):
        return  {'check': 1,
                 'result': {'crs': {'properties': {'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'},
                                    'type': 'name'},
                            'features': [{'geometry': {'coordinates': [[[[30.0, 30.0],
                                                                         [-30.0, -30.0],
                                                                         [10.0, 20.0],
                                                                         [30.0, 30.0]]]],
                                                       'type': 'MultiPolygon'},
                                          'properties': {'ans_1': 'answer45_1',
                                                         'ans_2': 'answer45_2',
                                                         'entr_time': '2021-11-20 22:45:00',
                                                         'id': 24,
                                                         'photo': 'https://telegra.ph/test_path_photo45',
                                                         'quest_1': 'question44_1',
                                                         'quest_2': 'question44_2',
                                                         'survey': 'survey44',
                                                         'user_name': 'Name45',
                                                         'video': 'https://telegra.ph/test_path_video45'},
                                          'type': 'Feature'},
                                         {'geometry': {'coordinates': [[[[40.0, 10.0],
                                                                         [-40.0, -10.0],
                                                                         [70.0, 20.0],
                                                                         [40.0, 10.0]]]],
                                                       'type': 'MultiPolygon'},
                                          'properties': {'ans_1': 'answer46_1',
                                                         'ans_2': 'answer46_2',
                                                         'entr_time': '2021-11-20 22:45:00',
                                                         'id': 25,
                                                         'photo': 'https://telegra.ph/test_path_photo46',
                                                         'quest_1': 'question44_1',
                                                         'quest_2': 'question44_2',
                                                         'survey': 'survey44',
                                                         'user_name': 'Name46',
                                                         'video': 'https://telegra.ph/test_path_video46'},
                                          'type': 'Feature'}],
                            'name': 'Places',
                            'type': 'FeatureCollection'}}

    @property
    def result_geom_gjson_point(self):
        return  (b'{"crs": {"properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}, "type": "n'
                 b'ame"}, "features": [{"geometry": {"coordinates": [45.0, 45.0], "type": "Poin'
                 b't"}, "properties": {"ans_1": "answer47_1", "ans_2": "answer47_2", "entr_time'
                 b'": "2021-11-20 22:45:00", "id": 22, "photo": "https://telegra.ph/test_path_p'
                 b'hoto47", "quest_1": "question47_1", "quest_2": "question47_2", "survey": "su'
                 b'rvey47", "user_name": "Name47", "video": "https://telegra.ph/test_path_video'
                 b'47"}, "type": "Feature"}, {"geometry": {"coordinates": [-45.0, -45.0], "type'
                 b'": "Point"}, "properties": {"ans_1": "answer47_1", "ans_2": "answer47_2", "e'
                 b'ntr_time": "2021-11-20 22:45:00", "id": 23, "photo": "None", "quest_1": "que'
                 b'stion47_1", "quest_2": "question47_2", "survey": "survey47", "user_name": "N'
                 b'ame47", "video": "None"}, "type": "Feature"}], "name": "Places", "type": "Fe'
                 b'atureCollection"}')

    @property
    def result_geom_gjson_polygon(self):
        return  (b'{"crs": {"properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}, "type": "n'
                 b'ame"}, "features": [{"geometry": {"coordinates": [[[[30.0, 30.0], [-30.0, -3'
                 b'0.0], [10.0, 20.0], [30.0, 30.0]]]], "type": "MultiPolygon"}, "properties": '
                 b'{"ans_1": "answer48_1", "ans_2": "answer48_2", "entr_time": "2021-11-20 22:4'
                 b'5:00", "id": 24, "photo": "https://telegra.ph/test_path_photo48", "quest_1":'
                 b' "question47_1", "quest_2": "question47_2", "survey": "survey47", "user_name'
                 b'": "Name48", "video": "https://telegra.ph/test_path_video48"}, "type": "Feat'
                 b'ure"}, {"geometry": {"coordinates": [[[[40.0, 10.0], [-40.0, -10.0], [70.0, '
                 b'20.0], [40.0, 10.0]]]], "type": "MultiPolygon"}, "properties": {"ans_1": "an'
                 b'swer49_1", "ans_2": "answer49_2", "entr_time": "2021-11-20 22:45:00", "id": '
                 b'25, "photo": "https://telegra.ph/test_path_photo49", "quest_1": "question47_'
                 b'1", "quest_2": "question47_2", "survey": "survey47", "user_name": "Name49", '
                 b'"video": "https://telegra.ph/test_path_video49"}, "type": "Feature"}], "name'
                 b'": "Places", "type": "FeatureCollection"}')

    @property
    def result_shp_point(self):
        return  {'check': 1,
                 'dbf': b'\x00ID\x00\x00\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00USER_NAME\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00SURVEY\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                        b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00TIME'
                        b'\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PHOTO\x00\x00\x00'
                        b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00VIDEO\x00\x00\x00\x00\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00QUEST_1\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ANS_1\x00\x00\x00'
                        b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00QUEST_2\x00\x00\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00ANS_2\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                        b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r 37'
                        b'                                                Name50              '
                        b'                              survey50                              '
                        b'            20-Nov-2021 22:45:00                              https:'
                        b'//telegra.ph/test_path_photo50              https://telegra.ph/test_'
                        b'path_video50              question50_1                              '
                        b'        answer50_1                                        question50'
                        b'_2                                      answer50_2                  '
                        b'                       38                                           '
                        b'     Name50                                            survey50     '
                        b'                                     20-Nov-2021 22:45:00           '
                        b'                                                                    '
                        b'                                                   question50_1     '
                        b'                                 answer50_1                         '
                        b'               question50_2                                      ans'
                        b'wer50_2                                        ',
                 'shp': b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00N\xe8\x03\x00\x00'
                        b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00'
                        b'\x00\x80F\xc0\x00\x00\x00\x00\x00\x80F@\x00\x00\x00\x00\x00\x80F@'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01\x00\x00\x00\n\x01\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x80F@\x00\x00\x00\x00\x00\x80F@\x00\x00\x00\x02\x00\x00\x00\n'
                        b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00'
                        b'\x00\x80F\xc0',
                 'shx': b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00:\xe8\x03\x00\x00'
                        b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00'
                        b'\x00\x80F\xc0\x00\x00\x00\x00\x00\x80F@\x00\x00\x00\x00\x00\x80F@'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x002\x00\x00\x00\n\x00\x00\x00@\x00\x00\x00\n'}

    @property
    def result_shp_polygon(self):
        return  {'check': 1,
                 'dbf': b'\x00ID\x00\x00\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00USER_NAME\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00SURVEY\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                        b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00TIME'
                        b'\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PHOTO\x00\x00\x00'
                        b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00VIDEO\x00\x00\x00\x00\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00QUEST_1\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ANS_1\x00\x00\x00'
                        b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00QUEST_2\x00\x00\x00\x00C'
                        b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00ANS_2\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                        b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\r 39'
                        b'                                                Name51              '
                        b'                              survey50                              '
                        b'            20-Nov-2021 22:45:00                              https:'
                        b'//telegra.ph/test_path_photo51              https://telegra.ph/test_'
                        b'path_video51              question50_1                              '
                        b'        answer51_1                                        question50'
                        b'_2                                      answer51_2                  '
                        b'                       40                                           '
                        b'     Name52                                            survey50     '
                        b'                                     20-Nov-2021 22:45:00           '
                        b'                   https://telegra.ph/test_path_photo52             '
                        b' https://telegra.ph/test_path_video52              question50_1     '
                        b'                                 answer52_1                         '
                        b'               question50_2                                      ans'
                        b'wer52_2                                        ',
                 'shp': b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xaa\xe8\x03\x00\x00'
                        b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00'
                        b'\x00\x00>\xc0\x00\x00\x00\x00\x00\x80Q@\x00\x00\x00\x00\x00\x00>@'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x01\x00\x00\x008\x05\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00>\xc0\x00\x00\x00\x00\x00\x00>\xc0\x00\x00\x00\x00\x00\x00>@'
                        b'\x00\x00\x00\x00\x00\x00>@\x01\x00\x00\x00\x04\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00\x00\x00>@'
                        b'\x00\x00\x00\x00\x00\x00>\xc0\x00\x00\x00\x00\x00\x00>\xc0'
                        b'\x00\x00\x00\x00\x00\x00$@\x00\x00\x00\x00\x00\x004@\x00\x00\x00\x00'
                        b'\x00\x00>@\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x02\x00\x00\x008'
                        b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00'
                        b'\x00\x00$\xc0\x00\x00\x00\x00\x00\x80Q@\x00\x00\x00\x00\x00\x004@'
                        b'\x01\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00D@\x00\x00\x00\x00\x00\x00$@\x00\x00\x00\x00\x00\x00D\xc0'
                        b'\x00\x00\x00\x00\x00\x00$\xc0\x00\x00\x00\x00\x00\x80Q@'
                        b'\x00\x00\x00\x00\x00\x004@\x00\x00\x00\x00\x00\x00D@\x00\x00\x00\x00'
                        b'\x00\x00$@',
                 'shx': b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00:\xe8\x03\x00\x00'
                        b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00'
                        b'\x00\x00>\xc0\x00\x00\x00\x00\x00\x80Q@\x00\x00\x00\x00\x00\x00>@'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x002\x00\x00\x008\x00\x00\x00n\x00\x00\x008'}

    @property
    def result_geom_shp_point(self):
        return  [b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                 b'\x00\x00\x00\x00\x00\x00\x00N\xe8\x03\x00\x00\x01\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00'
                 b'\x00\x80F@\x00\x00\x00\x00\x00\x80F@\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\n'
                 b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80F@\x00\x00\x00\x00\x00\x80F@'
                 b'\x00\x00\x00\x02\x00\x00\x00\n\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80F\xc0'
                 b'\x00\x00\x00\x00\x00\x80F\xc0',
                 b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                 b'\x00\x00\x00\x00\x00\x00\x00:\xe8\x03\x00\x00\x01\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00\x00\x80F\xc0\x00\x00\x00\x00'
                 b'\x00\x80F@\x00\x00\x00\x00\x00\x80F@\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x002\x00\x00\x00\n\x00\x00\x00@'
                 b'\x00\x00\x00\n',
                 b'\x03y\x0b\x16\x02\x00\x00\x00a\x01\xf5\x01\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ID\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00USER_NAME\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00SURVEY\x00\x00\x00\x00\x00C'
                 b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00TIME\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                 b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PHOT'
                 b'O\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00VIDEO\x00\x00\x00\x00\x00\x00C'
                 b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00QUEST_1\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ANS_1\x00\x00\x00'
                 b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00QUEST_2\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ANS_2\x00\x00\x00'
                 b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\r 37                                                Name'
                 b'53                                            survey53                      '
                 b'                    20-Nov-2021 22:45:00                              https:'
                 b'//telegra.ph/test_path_photo53              https://telegra.ph/test_path_vid'
                 b'eo53              question53_1                                      answer53'
                 b'_1                                        question53_2                      '
                 b'                answer53_2                                         38       '
                 b'                                         Name53                             '
                 b'               survey53                                          20-Nov-2021'
                 b' 22:45:00                                                                   '
                 b'                                                               question53_1 '
                 b'                                     answer53_1                             '
                 b'           question53_2                                      answer53_2     '
                 b'                                   ',
                 b'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257'
                 b'223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]']

    @property
    def result_geom_shp_polygon(self):
        return  [b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                 b'\x00\x00\x00\x00\x00\x00\x00\xaa\xe8\x03\x00\x00\x05\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00\x00\x00>\xc0\x00\x00\x00\x00'
                 b'\x00\x80Q@\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x008'
                 b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00>\xc0\x00\x00\x00\x00\x00\x00>\xc0'
                 b'\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00\x00\x00>@\x01\x00\x00\x00'
                 b'\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00'
                 b'\x00\x00>@\x00\x00\x00\x00\x00\x00>\xc0\x00\x00\x00\x00\x00\x00>\xc0'
                 b'\x00\x00\x00\x00\x00\x00$@\x00\x00\x00\x00\x00\x004@\x00\x00\x00\x00'
                 b'\x00\x00>@\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x02\x00\x00\x008'
                 b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00\x00\x00$\xc0'
                 b'\x00\x00\x00\x00\x00\x80Q@\x00\x00\x00\x00\x00\x004@\x01\x00\x00\x00'
                 b'\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00D@\x00\x00\x00\x00'
                 b'\x00\x00$@\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00\x00\x00$\xc0'
                 b'\x00\x00\x00\x00\x00\x80Q@\x00\x00\x00\x00\x00\x004@\x00\x00\x00\x00'
                 b'\x00\x00D@\x00\x00\x00\x00\x00\x00$@',
                 b"\x00\x00'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                 b'\x00\x00\x00\x00\x00\x00\x00:\xe8\x03\x00\x00\x05\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00D\xc0\x00\x00\x00\x00\x00\x00>\xc0\x00\x00\x00\x00'
                 b'\x00\x80Q@\x00\x00\x00\x00\x00\x00>@\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x002\x00\x00\x008\x00\x00\x00n'
                 b'\x00\x00\x008',
                 b'\x03y\x0b\x16\x02\x00\x00\x00a\x01\xf5\x01\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ID\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00USER_NAME\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00SURVEY\x00\x00\x00\x00\x00C'
                 b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00TIME\x00\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x00'
                 b'2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PHOT'
                 b'O\x00\x00\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00VIDEO\x00\x00\x00\x00\x00\x00C'
                 b'\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00QUEST_1\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ANS_1\x00\x00\x00'
                 b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00QUEST_2\x00\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00'
                 b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00ANS_2\x00\x00\x00'
                 b'\x00\x00\x00C\x00\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                 b'\x00\x00\x00\x00\r 39                                                Name'
                 b'54                                            survey53                      '
                 b'                    20-Nov-2021 22:45:00                              https:'
                 b'//telegra.ph/test_path_photo54              https://telegra.ph/test_path_vid'
                 b'eo54              question53_1                                      answer54'
                 b'_1                                        question53_2                      '
                 b'                answer54_2                                         40       '
                 b'                                         Name55                             '
                 b'               survey53                                          20-Nov-2021'
                 b' 22:45:00                              https://telegra.ph/test_path_photo55 '
                 b'             https://telegra.ph/test_path_video55              question53_1 '
                 b'                                     answer55_1                             '
                 b'           question53_2                                      answer55_2     '
                 b'                                   ',
                 b'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257'
                 b'223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]']