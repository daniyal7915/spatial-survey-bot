import re


def credentials(db_url):
    """Parse the database
       string"""
    transit1 = db_url.split('/')
    transit2 = transit1[2].split('@')
    name = transit1[-1]
    user, password = transit2[0].split(':')
    host, port = transit2[1].split(':')
    return {'NAME': name, 'USER': user, 'PASSWORD': password, 'HOST': host, 'PORT': port}


class DotDict(dict):
    """dot.notation access to
       dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class ProcessData:
    """The data containers and the substitute method."""

    def sub(self, text):
        """Substitute "'" with "`",
           otherwise the presence of "'" in a database
           query can cause an error"""
        pattern = re.compile(r"'")
        return pattern.sub('`', text)

    @property
    def states(self):
        """The States data
           container"""
        return {'INIT': 1, 'SURVEY1': 2, 'SURVEY2': 3, 'SURVEY3': 4, 'COLLECT': 5, 'POINT': 6, 'POLYGON': 7,
                'TRANSIT': 8, 'MEDIA1': 9, 'MEDIA2': 10, 'QUESTION1': 11, 'QUESTION2': 12, 'ANSWER': 13, 'CHECK1': 14,
                'CHECK2': 15, 'SUBMIT': 16, 'RESULT': 17}

    @property
    def scales(self):
        """the Scales data
            container"""
        return {20: 19, 30: 18, 50: 17, 100: 16, 300: 15, 500: 14, 1000: 13, 5000: 12, 10000: 11, 40000: 10, 80000: 9,
                150000: 8, 300000: 7, 600000: 6, 1200000: 5, 2500000: 4, 5000000: 3, 10000000: 2}

    @property
    def datum(self):
        """The Datum data
           container"""
        return 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],' \
               'PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
