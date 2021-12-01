# The bot answers

INTRO1 = 'Hi, <b>%s</b>.\nIf you know the name of a Survey, please enter it below. If not, you can ' \
         '<b>"Create Survey"</b> and share it with your participants.\n\nTo reset the bot, click/type /start at ' \
         'any stage.'

INTRO2 = 'Returned to the first step.\nIf you know the name of a Survey, please enter it below. If not, ' \
         'you can <b>"Create Survey"</b> and share it with your participants.\n\nTo reset the bot, ' \
         'click/type /start at any stage.'

INTRO3 = 'Returned to the first step, the last entry was lost.\nIf you know the name of a Survey, ' \
         'please enter it below. If not, you can <b>"Create Survey"</b> and share it with your participants.\n\n' \
         'To reset the bot, click/type /start at any stage.'

NAME_CREATE = 'Enter your Survey name or <b>"Create Survey"</b>.'

NOT_EXIST = 'The entered Survey does not exist, try once again or <b>Create Survey</b>.'

EXIST = 'Survey already exists. Re-enter'

NAME = 'Enter Survey name'

MIN_SYMBOL = 'Minimum four symbols required. Re-enter'

VIEW = 'Click <b>"View"</b> to view the collected data, <b>"Collect"</b> to start collecting data or ' \
       '<b>"Back>>"</b> to return to the first step.'

NO_DATA = 'No data to view, click <b>"Collect"</b> to collect data, <b>"Back>>"</b> to return to the first step.'

DOWNLOAD = 'You can download data as a <b>"Map"</b>, <b>"Shapefile"</b> or <b>"GeoJSON"</b>. <b>"Delete"</b> ' \
           'to delete all your data, <b>"Back>>"</b> to return to the previous step.'

COLLECT = 'Click <b>"Collect"</b> to start collecting data or <b>"Back>>"</b> to return to the first step.'

POINT = 'Enter coordinates of your point using native Telegram <b>"Location"</b> function, ' \
        'choose the <b>"Send My Current Location"</b> option.\n\nYou also can enter coordinates manually, ' \
        'using the following template: <i>45.3456, 75.5634</i>, where the first digit is ' \
        'Latitude, the second one is Longitude.\n\nSpatial Reference: WGS84\nCoordinate System: Geographical'

POLYGON = 'Enter coordinates of vertices of your polygon using native ' \
          'Telegram <b>"Location"</b> function, choose the <b>"Send My Current Location"</b> option.' \
          '\n\nYou also can enter coordinates manually, using the following template: <i>45.3456, 75.5634</i>, ' \
          'where the first digit is Latitude, the second one is Longitude.\n\nWhen coordinates of all vertices have ' \
          'been entered, click <b>"Done"</b>.\n\nSpatial Reference: WGS84\nCoordinate System: Geographical'

GEOM = 'Choose geometry: <b>"Point"</b> or <b>"Polygon"</b>'

VERTICES = 'Number of entered vertices is %d. Minimum is 4. Continue to enter coordinates'

COORD_NS = 'Coordinates were not saved, use the Location function at the appropriate step'

PHOTO_NS = 'The photo was not saved, send it at an appropriate stage or multiple photos were submitted at once'

VIDEO_NS = 'The video was not saved, send it at an appropriate stage or multiple videos were submitted at once'

ATTACH_MEDIA = 'Attach a photo and/or video using native Telegram <b>Gallery</b> tool or using standard media ' \
               'attachment from a message. Only one photo and one video will be saved for each geometry'

INVALID = 'Invalid input, send a photo or video'

ANSWER_Q1 = "Answer the first Survey question:\n<i>%s</i>"

NEXT_Q = 'Enter the next question'

ALL_ANSWERED = 'You answered all the questions. Click <b>"Submit"</b> to submit, <b>"Delete"</b> to delete ' \
               'the last Survey entry'

SUBMIT_DELETE = 'Click <b>"Submit"</b> to submit, <b>"Delete"</b> to delete the last Survey entry'

SUBMITTED1 = 'Submitted. You can download data as a <b>"Map"</b>, <b>"Shapefile"</b> or <b>"GeoJSON"</b>. ' \
             '<b>"Delete"</b> to delete all your data, <b>"Back>>"</b> to continue.'

SUBMITTED2 = 'Submitted. The data can be seen and downloaded by the Survey`s owner only. Create your own Survey to ' \
             'get the full functionality.\nClick <b>"Back>>"</b> to continue.'

DELETED1 = 'Deleted. Re-enter a question'

DELETED2 = 'Deleted. Click <b>"View"</b> to view the collected data, <b>"Collect"</b> to start collecting data or ' \
           '<b>"Back>>"</b> to return to the first step.'

DELETED3 = 'Deleted. Click <b>"Collect"</b> to start collecting data or <b>"Back>>"</b> to return to the fist step.'

CONFIRM = 'Are you sure?'

POINT_MEDIA = 'Coordinates: Latitude %.4f, Longitude %.4f were saved.\nDo you want to attach photo or video?'

INVALID_COORD = 'Invalid Latitude and Longitude, they must be between -90\u00b0 and 90\u00b0 and between -180\u00b0 ' \
                'and 180\u00b0, respectively'

INVALID_LAT = 'Invalid Latitude! It must be between -90\u00b0 and 90\u00b0'

INVALID_LONG = 'Invalid Longitude! It must be between -180\u00b0 and 180\u00b0'

FOLLOW_TEMPLATE = 'Invalid input! Follow the template: 45, 45 (where the first digit is Latitude, ' \
                  'the second one is Longitude.'

VERTEX_DONE = 'Enter coordinates of another vertex or click <b>"Done"</b>'

POLYGON_MEDIA = 'The polygon was saved.\nDo you want to attach photo or video?'

MEDIA_SAVED = 'Your %s was saved. Do you want to attach another %s or %s?'

MEDIA_NS = 'Your %s was not saved due to a mistake at the media hosting. Probably your file is too large.\n' \
           'Do you want to attach another %s or %s?'

SURVEY_SAVED = 'Survey <i>%s</i> was saved. Remember its name, it is required for the access to ' \
               'the Survey.\n\nEnter the first survey question.'

Q_SAVED = 'Your question "%s" was saved. Click <b>"Next"</b>, <b>"Done"</b> or <b>"Delete"</b>'

ANS_NEXT_Q = 'The next question:\n<i>%s</i>'

LONG = 'Your entry is too long.'

answers = {'INTRO1': INTRO1, 'INTRO2': INTRO2, 'INTRO3': INTRO3, 'POINT': POINT, 'POLYGON': POLYGON, 'NAME': NAME,
           'COLLECT': COLLECT, 'NOT_EXIST': NOT_EXIST, 'MIN_SYMBOL': MIN_SYMBOL, 'EXIST': EXIST, 'GEOM': GEOM,
           'DOWNLOAD': DOWNLOAD, 'NO_DATA': NO_DATA, 'NAME_CREATE': NAME_CREATE, 'NEXT_Q': NEXT_Q, 'DELETED1': DELETED1,
           'VERTICES': VERTICES, 'COORD_NS': COORD_NS, 'ATTACH_MEDIA': ATTACH_MEDIA, 'ANSWER_Q1': ANSWER_Q1,
           'INVALID': INVALID, 'PHOTO_NS': PHOTO_NS, 'VIDEO_NS': VIDEO_NS, 'ALL_ANSWERED': ALL_ANSWERED,
           'DELETED2': DELETED2, 'DELETED3': DELETED3, 'SUBMIT_DELETE': SUBMIT_DELETE, 'CONFIRM': CONFIRM,
           'SUBMITTED1': SUBMITTED1, 'SUBMITTED2': SUBMITTED2, 'VIEW': VIEW, 'POINT_MEDIA': POINT_MEDIA,
           'INVALID_COORD': INVALID_COORD, 'INVALID_LAT': INVALID_LAT, 'INVALID_LONG': INVALID_LONG,
           'FOLLOW_TEMPLATE': FOLLOW_TEMPLATE, 'VERTEX_DONE': VERTEX_DONE, 'POLYGON_MEDIA': POLYGON_MEDIA,
           'MEDIA_SAVED': MEDIA_SAVED, 'MEDIA_NS': MEDIA_NS, 'SURVEY_SAVED': SURVEY_SAVED, 'Q_SAVED': Q_SAVED,
           'ANS_NEXT_Q': ANS_NEXT_Q, 'LONG': LONG}
