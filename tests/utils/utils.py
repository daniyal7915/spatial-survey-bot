import io
from engine.utils.utils import DotDict
from tests.utils.data import Data


class Message(Data):
    num = 0
    text = 'survey'

    @property
    def message(self):
        if self.text == 'survey':
            return DotDict({'from_user': DotDict({'id': self.num, 'first_name': f'Name{self.num}'}),
                            'text': f'{self.text}{self.num}',
                            'location': DotDict({'latitude': self.data_point_polygon_location[0],
                                                 'longitude': self.data_point_polygon_location[1]}),
                            'survey': f'survey{self.num}'})
        else:
            return DotDict({'from_user': DotDict({'id': self.num, 'first_name': f'Name{self.num}'}),
                            'text': f'{self.text}',
                            'location': DotDict({'latitude': self.data_point_polygon_location[0],
                                                 'longitude': self.data_point_polygon_location[1]}),
                            'survey': f'survey{self.num}'})


class TestID:
    def transit_process(self, transit):
        test_id = [37, 38, 39, 40]

        for i in range(4):
            transit[i][0] = test_id[i]

        return transit

    def elem_process(self, elem, index):
        test_id = [22, 23, 24, 25]

        elem['id'] = test_id[index]

        return elem


class ShpProcess:
    def shp_value(self, shp):
        shp['shp'] = shp['shp'].getvalue()
        shp['shx'] = shp['shx'].getvalue()
        shp['dbf'] = shp['dbf'].getvalue()[31:]

        return shp

    def shp_bytes(self, shp):
        shp['shp'] = io.BytesIO(shp['shp'])
        shp['shx'] = io.BytesIO(shp['shx'])
        shp['dbf'] = io.BytesIO(shp['dbf'])

        return shp


class MockResponse:
    data = [{'src': 'https://telegra.ph/test_path'}]

    def __init__(self, status=None):
        self.status_code = status

    def json(self):
        if self.status_code == 200:
            return self.data





