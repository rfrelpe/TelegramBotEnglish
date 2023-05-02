# t.me/AnotherEnglishBotMIPT42_bot
# 6055064354:AAHs_0eXvki0pP2mHA5WWpGy7n4zlWvgjEA

# pip install googletrans-4.0.0rc1
from telebot import types  # для указание типов
import telebot
import pickle
from random_word import RandomWords
from googletrans import Translator
translator = Translator()


bot = telebot.TeleBot('6055064354:AAHs_0eXvki0pP2mHA5WWpGy7n4zlWvgjEA')

global_users_points_dict = {}
state = {}  # 0: menu; 1: ru -> en; 2: en -> ru
user_last_word_dict = {}

r = RandomWords()


def ru_to_en_train(message):
    global global_users_points_dict, r, user_last_word_dict

    res = 'banana'

    while translator.detect(res).lang != 'ru':
        res = translator.translate(
            r.get_random_word(), dest='ru', src='en').text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Закончить тренировку")
    btn2 = types.KeyboardButton("Дай мне другое слово")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text=f"Переведи следующее слово на английский: *{res}*",
                     reply_markup=markup,
                     parse_mode="Markdown")

    user_last_word_dict[message.from_user.username] = res


def en_to_ru_train(message):
    global global_users_points_dict, r, user_last_word_dict

    res = r.get_random_word()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Закончить тренировку")
    btn2 = types.KeyboardButton("Дай мне другое слово")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text=f"Переведи следующее слово на русский: *{res}*",
                     reply_markup=markup,
                     parse_mode="Markdown")

    user_last_word_dict[message.from_user.username] = res


def save_data():
    global global_users_points_dict
    with open('users_data.pickle', 'wb') as f:
        pickle.dump(global_users_points_dict, f)


def load_data():
    global global_users_points_dict
    try:
        with open('users_data.pickle', 'rb') as f:
            global_users_points_dict = pickle.load(f)
    except BaseException:
        global_users_points_dict = {}


def main_menu(message):

    state[message.from_user.username] = 0

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Русский -> English")
    btn2 = types.KeyboardButton("English -> Русский")
    btn3 = types.KeyboardButton("О боте...")
    btn4 = types.KeyboardButton("Моя статистика/Меню")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(
        message.chat.id,
        text=f"Привет, {message.from_user.username}! Давай изучать английский!",
        reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    global global_users_points_dict, state

    load_data()

    if message.from_user.username not in global_users_points_dict:
        global_users_points_dict[message.from_user.username] = 0

    main_menu(message)


@bot.message_handler(content_types=['text'])
def func(message):
    global global_users_points_dict, state, user_last_word_dict

    if (message.text == "Русский -> English"):
        markup_remove = types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            text="Давай переводить слова с русского на английский!",
            reply_markup=markup_remove)
        state[message.from_user.username] = 1
        ru_to_en_train(message)

    elif (message.text == "English -> Русский"):
        markup_remove = types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            text="Давай переводить слова с английского на русский!",
            reply_markup=markup_remove)
        state[message.from_user.username] = 2
        en_to_ru_train(message)

    elif (message.text == "О боте..."):
        bot.send_message(
            message.chat.id,
            text="Бот разработан _Лукьянчуком Вячеславом_ ([vk](https://vk.com/rfrelpes))",
            parse_mode="Markdown")
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню")
        main_menu(message)

    elif (message.text == "Моя статистика/Меню" or message.text == "Закончить тренировку"):
        bot.send_message(
            message.chat.id,
            text=f"Пользователь {message.from_user.username}! \nВсего баллов {global_users_points_dict[message.from_user.username]}.")
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню")
        main_menu(message)

        save_data()  # Save data only when the user sees :)

    elif state[message.from_user.username] == 1:  # ru -> en

        if message.text == "Дай мне другое слово":
            ru_to_en_train(message)
            return

        true_result = translator.translate(user_last_word_dict[message.from_user.username],
                                           dest='en',
                                           src='ru').text.lower()

        if message.text.lower() == true_result:
            global_users_points_dict[message.from_user.username] += 1

            bot.send_message(message.chat.id, text="Молодец, так держать!")

        else:
            bot.send_message(
                message.chat.id,
                text=f"Не совсем верно, попытайся ещё раз! Правильный ответ был {true_result}")

        ru_to_en_train(message)
    elif state[message.from_user.username] == 2:  # en -> ru

        if message.text == "Дай мне другое слово":
            en_to_ru_train(message)
            return

        true_result = translator.translate(user_last_word_dict[message.from_user.username],
                                           dest='ru',
                                           src='en').text.lower()

        if message.text.lower() == true_result:
            global_users_points_dict[message.from_user.username] += 1

            bot.send_message(message.chat.id, text="Молодец, так держать!")

        else:
            bot.send_message(
                message.chat.id,
                text=f"Не совсем верно, попытайся ещё раз! Правильный ответ был {true_result}")

        en_to_ru_train(message)


bot.polling(none_stop=True, interval=0)
