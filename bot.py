import os
import telebot
import psycopg2
from engine.utils.answers import answers
from engine.utils.tables import Tables
from engine.process import State, Delete, Survey, CreateGJsonShp, CreateWebMap, Coord, Media, QuestionAnswer

token = os.environ['TEL_TOKEN']
bot = telebot.TeleBot(token)

Tables().create()

state, delete, survey = State(), Delete(), Survey()
coord, media, qa = Coord(), Media(), QuestionAnswer()
webmap, gjson_shp = CreateWebMap(), CreateGJsonShp()


@bot.message_handler(commands=['start'])
def command_handler(message):
    ans = answers['INTRO2']
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Create Survey', callback_data='create survey'))

    if state.show_state(message) in [state.states['SURVEY1'], state.states['SURVEY3'], state.states['RESULT'],
                                     state.states['CHECK2'], state.states['COLLECT']]:
        state.save_state(message, state.states['SURVEY1'])
    elif state.show_state(message) == state.states['INIT']:
        state.save_state(message, state.states['SURVEY1'])
        ans = answers['INTRO1'] % message.from_user.first_name
    elif state.show_state(message) in [state.states['QUESTION1'], state.states['QUESTION2']]:
        state.save_state(message, state.states['SURVEY1'])
        ans = answers['INTRO3']
        delete.del_question(message)
    elif state.show_state(message) in [state.states['POINT'], state.states['POLYGON'], state.states['TRANSIT'],
                                       state.states['MEDIA1'], state.states['MEDIA2']]:
        state.save_state(message, state.states['SURVEY1'])
        ans = answers['INTRO3']
        delete.del_feature(message)
    elif state.show_state(message) in [state.states['ANSWER'], state.states['CHECK1']]:
        state.save_state(message, state.states['SURVEY1'])
        delete.del_row(message)
        ans = answers['INTRO3']
    elif state.show_state(message) == state.states['SUBMIT']:
        state.save_state(message, state.states['SURVEY1'])
        if not delete.check_ans(message):
            delete.del_row(message)
            ans = answers['INTRO3']
    elif state.show_state(message) in [state.states['SURVEY2']]:
        state.save_state(message, state.states['SURVEY1'])
        ans = answers['INTRO3']

    bot.send_message(message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['SURVEY1'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'create survey':
        state.save_state(call, state.states['SURVEY2'])
        ans = answers['NAME']
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')


@bot.message_handler(func=lambda message: state.show_state(message) == state.states['SURVEY1'])
def message_handler(message):
    ans = answers['VIEW']
    markup = telebot.types.InlineKeyboardMarkup()

    if survey.survey_check(message):
        survey.save_survey(message)
        state.save_state(message, state.states['SURVEY3'])
        if survey.get_author(message) == message.from_user.id:
            markup.add(telebot.types.InlineKeyboardButton('View', callback_data='view'),
                       telebot.types.InlineKeyboardButton('Collect', callback_data='collect'),
                       telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
        else:
            ans = answers['COLLECT']
            markup.add(telebot.types.InlineKeyboardButton('Collect', callback_data='collect'),
                       telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
    else:
        ans = answers['NOT_EXIST']
        markup.add(telebot.types.InlineKeyboardButton('Create Survey', callback_data='create survey'))

    bot.send_message(message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.message_handler(func=lambda message: state.show_state(message) == state.states['SURVEY2'])
def message_handler(message):
    ans = answers['EXIST']

    if not survey.survey_check(message):
        if len(message.text) < 4:
            ans = answers['MIN_SYMBOL']
        else:
            ans = answers['LONG']
            if survey.save_survey(message):
                pass
            else:
                state.save_state(message, state.states['QUESTION1'])
                ans = survey.survey_initial(message)

    bot.send_message(message.chat.id, ans, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['SURVEY3'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'collect':
        state.save_state(call, state.states['COLLECT'])
        qa.init_row(call)
        ans = answers['GEOM']
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Point', callback_data='point'),
                   telebot.types.InlineKeyboardButton('Polygon', callback_data='polygon'))
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
    elif call.data == 'view' and survey.get_author(call) == call.from_user.id:
        if qa.ans_check(call):
            state.save_state(call, state.states['RESULT'])
            ans = answers['DOWNLOAD']
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Map', callback_data='map'),
                       telebot.types.InlineKeyboardButton('Shapefile', callback_data='shapefile'),
                       telebot.types.InlineKeyboardButton('GeoJSON', callback_data='geojson'))
            markup.add(telebot.types.InlineKeyboardButton('Delete', callback_data='delete'),
                       telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
        else:
            ans = answers['NO_DATA']
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Collect', callback_data='collect'),
                       telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
    elif call.data == 'back>>':
        state.save_state(call, state.states['SURVEY1'])
        ans = answers['INTRO2']
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Create Survey', callback_data='create survey'))
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.message_handler(func=lambda message: state.show_state(message) == state.states['QUESTION1'])
def message_handler(message):
    ans = qa.question_insert(message)
    markup = None

    if ans == answers['LONG']:
        pass
    else:
        state.save_state(message, state.states['QUESTION2'])
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Next', callback_data='next'),
                   telebot.types.InlineKeyboardButton('Done', callback_data='done'),
                   telebot.types.InlineKeyboardButton('Delete', callback_data='delete'))

    bot.send_message(message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['QUESTION2'])
def message_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'done':
        state.save_state(call, state.states['SURVEY1'])
        ans = answers['NAME_CREATE']
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Create Survey', callback_data='create survey'))
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
    elif call.data == 'next':
        survey.survey_next(call)
        state.save_state(call, state.states['QUESTION1'])
        ans = answers['NEXT_Q']
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')
    elif call.data == 'delete':
        qa.question_null(call)
        state.save_state(call, state.states['QUESTION1'])
        ans = answers['DELETED1']
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['COLLECT'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'point':
        state.save_state(call, state.states['POINT'])
        ans = answers['POINT']
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')
    elif call.data == 'polygon':
        state.save_state(call, state.states['POLYGON'])
        ans = answers['POLYGON']
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')


@bot.message_handler(func=lambda message: state.show_state(message) == state.states['POINT'])
def message_handler(message):
    ans = coord.point_manual(message)
    markup = None

    if ans[-1] == '?':
        state.save_state(message, state.states['TRANSIT'])
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Yes', callback_data='yes'),
                   telebot.types.InlineKeyboardButton('No', callback_data='no'))

    bot.send_message(message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['POLYGON'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'done' and coord.get_count(call) >= 4:
        state.save_state(call, state.states['TRANSIT'])
        ans = coord.polygon_create(call, coord.get_poly_points(call).split(','))
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Yes', callback_data='yes'),
                   telebot.types.InlineKeyboardButton('No', callback_data='no'))
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
    elif call.data == 'done' and coord.get_count(call) < 4:
        ans = answers['VERTICES'] % coord.get_count(call)
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')


@bot.message_handler(func=lambda message: state.show_state(message) == state.states['POLYGON'])
def message_handler(message):
    ans = coord.polygon_manual(message)

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Done', callback_data='done'))

    bot.send_message(message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.message_handler(content_types=['location'])
def location_handler(message):
    ans = answers['COORD_NS']
    markup = None

    if state.show_state(message) == state.states['POINT']:
        state.save_state(message, state.states['TRANSIT'])
        ans = coord.point_location(message)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Yes', callback_data='yes'),
                   telebot.types.InlineKeyboardButton('No', callback_data='no'))
    elif state.show_state(message) == state.states['POLYGON']:
        ans = coord.polygon_location(message)
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Done', callback_data='done'))

    bot.send_message(message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['TRANSIT'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'yes':
        state.save_state(call, state.states['MEDIA1'])
        ans = answers['ATTACH_MEDIA']
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')
    elif call.data == 'no':
        state.save_state(call, state.states['ANSWER'])
        ans = answers['ANSWER_Q1'] % qa.get_question(call)
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')


@bot.message_handler(func=lambda message: state.show_state(message) == state.states['MEDIA1'])
def message_handler(message):
    bot.send_message(message.chat.id, answers['INVALID'])


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    ans = answers['PHOTO_NS']
    markup = None

    try:
        if state.show_state(message) == state.states['MEDIA1']:
            path = media.media_path(token, bot.get_file(message.photo[-1].file_id), 'image/jpeg')
            state.save_state(message, state.states['MEDIA2'])
            ans = media.save_media(message, path, 'photo')
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Yes', callback_data='yes'),
                       telebot.types.InlineKeyboardButton('No', callback_data='no'))

    except psycopg2.ProgrammingError:
        pass

    bot.send_message(message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.message_handler(content_types=['video'])
def video_handler(message):
    ans = answers['VIDEO_NS']
    markup = None

    try:
        if state.show_state(message) == state.states['MEDIA1']:
            path = media.media_path(token, bot.get_file(message.video.file_id), 'video/mp4')
            state.save_state(message, state.states['MEDIA2'])
            ans = media.save_media(message, path, 'video')
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Yes', callback_data='yes'),
                       telebot.types.InlineKeyboardButton('No', callback_data='no'))
    except psycopg2.ProgrammingError:
        pass

    bot.send_message(message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['MEDIA2'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'yes':
        state.save_state(call, state.states['MEDIA1'])
        ans = answers['ATTACH_MEDIA']
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')
    elif call.data == 'no':
        state.save_state(call, state.states['ANSWER'])
        ans = answers['ANSWER_Q1'] % qa.get_question(call)
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML')


@bot.message_handler(func=lambda message: state.show_state(message) == state.states['ANSWER'])
def message_handler(message):
    ans = qa.answer_insert(message)
    markup = None

    if ans == answers['ALL_ANSWERED']:
        state.save_state(message, state.states['SUBMIT'])
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Submit', callback_data='submit'),
                   telebot.types.InlineKeyboardButton('Delete', callback_data='delete'))

    bot.send_message(message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['CHECK1'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'yes':
        state.save_state(call, state.states['SURVEY3'])
        delete.del_row(call)
        if survey.get_author(call) == call.from_user.id:
            ans = answers['DELETED2']
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('View', callback_data='view'),
                       telebot.types.InlineKeyboardButton('Collect', callback_data='collect'),
                       telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
        else:
            ans = answers['DELETED3']
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Collect', callback_data='collect'),
                       telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
    elif call.data == 'no':
        state.save_state(call, state.states['SUBMIT'])
        ans = answers['SUBMIT_DELETE']
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Submit', callback_data='submit'),
                   telebot.types.InlineKeyboardButton('Delete', callback_data='delete'))
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['CHECK2'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'yes':
        state.save_state(call, state.states['SURVEY3'])
        delete.del_data(call)
        ans = answers['DELETED2']
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('View', callback_data='view'),
                   telebot.types.InlineKeyboardButton('Collect', callback_data='collect'),
                   telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
    elif call.data == 'no':
        state.save_state(call, state.states['RESULT'])
        ans = answers['DOWNLOAD']
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Map', callback_data='map'),
                   telebot.types.InlineKeyboardButton('Shapefile', callback_data='shapefile'),
                   telebot.types.InlineKeyboardButton('GeoJSON', callback_data='geojson'))
        markup.add(telebot.types.InlineKeyboardButton('Delete', callback_data='delete'),
                   telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['SUBMIT'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if call.data == 'delete':
        state.save_state(call, state.states['CHECK1'])
        ans = answers['CONFIRM']
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Yes', callback_data='yes'),
                   telebot.types.InlineKeyboardButton('No', callback_data='no'))
        bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
    elif call.data == 'submit':
        qa.set_ans_check(call)
        state.save_state(call, state.states['RESULT'])
        if survey.get_author(call) == call.from_user.id:
            ans = answers['SUBMITTED1']
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Map', callback_data='map'),
                       telebot.types.InlineKeyboardButton('Shapefile', callback_data='shapefile'),
                       telebot.types.InlineKeyboardButton('GeoJSON', callback_data='geojson'))
            markup.add(telebot.types.InlineKeyboardButton('Delete', callback_data='delete'),
                       telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
        else:
            ans = answers['SUBMITTED2']
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: state.show_state(call) == state.states['RESULT'])
def callback_handler(call):
    bot.answer_callback_query(call.id)

    if survey.get_author(call) == call.from_user.id:
        if call.data == 'back>>':
            state.save_state(call, state.states['SURVEY3'])
            ans = answers['VIEW']
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('View', callback_data='view'),
                       telebot.types.InlineKeyboardButton('Collect', callback_data='collect'),
                       telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
        elif call.data == 'map':
            bot.send_document(call.message.chat.id, webmap.create(call))
        elif call.data == 'geojson':
            for geometry in gjson_shp.create(call, 'geojson'):
                bot.send_document(call.message.chat.id, geometry)
        elif call.data == 'shapefile':
            for file in gjson_shp.create(call, 'shapefile'):
                for geometry in file:
                    bot.send_document(call.message.chat.id, geometry)
        elif call.data == 'delete':
            state.save_state(call, state.states['CHECK2'])
            ans = answers['CONFIRM']
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Yes', callback_data='yes'),
                       telebot.types.InlineKeyboardButton('No', callback_data='no'))
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)
    else:
        if call.data == 'back>>':
            state.save_state(call, state.states['SURVEY3'])
            ans = answers['COLLECT']
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Collect', callback_data='collect'),
                       telebot.types.InlineKeyboardButton('Back>>', callback_data='back>>'))
            bot.send_message(call.message.chat.id, ans, parse_mode='HTML', reply_markup=markup)


if __name__ == "__main__":
    bot.polling()
