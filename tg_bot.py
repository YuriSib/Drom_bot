import telebot
import os
import time

from main import scrapping_drom, compare

bot = telebot.TeleBot('6034305301:AAFCiWFQoMQIIee5x2kT62zQJsSXFtyRKSk')


# @bot.message_handler(commands=['start'])
# def test(message_):
#     chat_id = message_.chat.id
#     bot.reply_to(message_, f"Your chat ID is: {chat_id}")

def message(car):
    bot.send_message(674796107, car)


if __name__ == "__main__":
    url = 'https://auto.drom.ru/region54/all/?minprice=500000&minyear=2014&inomarka=1&keywords=срочно'
    while True:
        suitable_options, list_id = scrapping_drom(url)
        new_car = compare(suitable_options, list_id)
        if new_car:
            message(new_car)
        time.sleep(300)

