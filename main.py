import time

import telebot
import random


bot = telebot.TeleBot("7826590907:AAF3e4KsK8c3rUHHWSpjYvihuGdD8IhAzBs", parse_mode='HTML')

cities = set()
used_cities = set()
current_city = None
city = None


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    load_cities()
    bot.send_message(chat_id,f"""Привет <b>{message.chat.first_name}</b>, давай сыграем в города!
я знаю все города России(ну или почти все), а именно{len(cities)} ! А ты?""")


@bot.message_handler(commands=["rules", "r"])
def rules(message):
    chat_id = message.chat.id
    load_cities()
    bot.send_message(chat_id,"<b>Города</b> — это игра для нескольких (двух или более) человек, в которой каждый участник в свою очередь называет реально существующий в данный момент времени город любой существующей страны, название которого начинается на ту букву, которой оканчивается название предыдущего города, без каких-либо исключений")


@bot.message_handler(commands=["new", "n"])
def new_game(message):
    global city
    load_cities()
    chat_id = message.chat.id
    bot.send_message(chat_id, "Кто начинает? 0 - я, 1 - ты!")

    if random.randint(0,1)==0:
        time.sleep(2)
        bot.send_message(chat_id, "0")
        bot.send_message(chat_id, "Я начинаю...")
        city = random.choice(list(cities))
        used_cities.add(city)
        bot.send_message(chat_id, f"{city}. Тебе на {city[-1].upper()}")

    else:
        time.sleep(2)
        bot.send_message(chat_id, "1")
        bot.send_message(chat_id, "ты первый, начинай...")

@bot.message_handler(content_types=["text"])
def human_turn(message):
    global current_city
    chat_id = message.chat.id
    text = message.text.capitalize()
    #if current_city is None:
    if text in used_cities:
        bot.send_message(chat_id, "Такой город уже был")
    elif text in cities:
        bot.send_message(chat_id, f"Отличный выбор! Мне на {text[-1].upper()}")
        current_city = text
        used_cities.add(current_city)
    else:
        bot.send_message(chat_id, "Я не знаю такого города!")
    bot_turn()

@bot.message_handler(content_types=["text"])
def bot_turn():
    city_bot = random.choice(list(cities))
    while city_bot in used_cities:
        if city_bot not in used_cities:
            bot.send_message(city_bot, f"Тебе на {city_bot[-1]}")
            used_cities.add(city_bot)




def load_cities():
    with open("cities.txt", "r", encoding="utf-8") as f:
        for c in f.readlines():
            cities.add(c.strip())


print(used_cities)


bot.polling(non_stop=True)


