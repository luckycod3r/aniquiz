import telebot
from telebot import types
import pandas as pd
import datetime
bot = telebot.TeleBot("7372872405:AAHenpe8EY4qNTVp6CySVWaiX229Xti5ROE")

adm_list = ["699531292", "586275976", "705359495"]

@bot.message_handler(commands=["start"])
def start(message):
    inf_database = pd.read_csv("users1.csv")
    if str(message.chat.id) in adm_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton(text="Список участников")
        b2 = types.KeyboardButton(text="Очистить список")
        markup.add(b1, b2)
        bot.send_message(message.chat.id,
                         "Добро пожаловать в админ-панель", reply_markup=markup)
        bot.register_next_step_handler(message, adm)
    elif int(message.chat.id) not in list(inf_database["id"]):
        dt = datetime.datetime.now()
        bot.send_message(message.chat.id, f"Готово! Ваш номер участника: {len(inf_database) + 1}")
        inf_database.loc[len(inf_database)] = [str(message.chat.id), len(inf_database) + 1, f'{datetime.date.today().isoformat()} {dt.hour}:{dt.minute}']
        inf_database.to_csv("users1.csv", mode='w', index=False)
        bot.send_message(message.chat.id, f"Регистрация на другие квизы доступна в группе:\nhttps://vk.com/ani_quiz")
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрировались")

def adm(message):
    inf_database = pd.read_csv("users1.csv")
    if message.text == "Список участников":
        bot.send_message(message.chat.id, inf_database.to_string(index=False))
    elif message.text == "Очистить список":
        inf_database.drop(inf_database.index[0:], inplace=True)
        inf_database.to_csv("users1.csv", mode='w', index=False)
        bot.send_message(message.chat.id, "Список очищен")
bot.infinity_polling()