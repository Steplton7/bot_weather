import os
import time
import config
import telebot
import pogodamail
from pogodamail import URL
from telebot import types
from base import PostresDB

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['test'])
def find_file_ids(message):
    #if message.from_user.id == 5458172332:
    for file in os.listdir('C:\\python_equals\\telegram_bot\\static\\'):
        if file.split('.')[-1] == 'png':
            f = open('C:\\python_equals\\telegram_bot\\static\\'+file, 'rb')
            msg = bot.send_photo(message.chat.id, f)
                # А теперь отправим вслед за файлом его file_id
            bot.send_message(message.chat.id, msg.photo, reply_to_message_id=msg.message_id)
        time.sleep(3)


@bot.message_handler(commands=['test_photo'])
def find_file_ids(message):
    db_worker = PostresDB(**config.db)
    png = db_worker.get_png('ясно')
    bot.send_photo(message.chat.id, png[1])


@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.last_name != None:
        mess = f'Привет {message.from_user.first_name} {message.from_user.last_name} \n Данный бот сделан для того что был готов к любой погоде'
    else:
        mess = f'Привет {message.from_user.first_name} \n Данный бот сделан для того что был готов к любой погоде'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начнем!")
    btn2 = types.KeyboardButton("Не интересно(")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)





@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    db_worker = PostresDB(**config.db)
    if message.text == 'Начнем!':
        if db_worker.get_user(message.from_user.id) == 0:
            db_worker.set_user(message.chat.id, message.from_user.id, message.from_user.first_name, message.from_user.last_name, 0)
        text = 'Отлично, в каком городе ты живешь? \nПостарайся написать название города правильно, а то я могу не найти его'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('/menu')
        btn2 = types.KeyboardButton('/exit')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif message.text == 'Не интересно(':
        text = "Я пока больше ничего не умею"
        bot.send_message(message.chat.id, text)
    else:
        if db_worker.get_user(message.from_user.id) == 0:
            text = 'Странно не вижу тебя среди своих пользователей \nВернись в главное меню и попробуй сначала'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('/start')
            btn2 = types.KeyboardButton('/exit')
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, text, reply_markup=markup)
        else:
            city = message.text.title()
            temp = pogodamail.parsing(URL, city)
            png = db_worker.get_png(temp[1])
            temp = '{0} {1}'.format(temp[0], temp[1])
            #print(png)
            if len(png) != 0:
                bot.send_photo(message.chat.id, png[0][1], caption=temp)
            else:
                bot.send_message(message.chat.id, temp)



if __name__ == '__main__':
    bot.infinity_polling()
