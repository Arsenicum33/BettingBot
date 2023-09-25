import datetime
import telebot
import random
from telebot import types

bot = telebot.TeleBot('6616430031:AAE49z6tahdbAeOLSsjDy_w-UU2B2xE8q-8')

bets = []

# Кнопки


def generate_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('create bet')
    item2 = types.KeyboardButton('get bets')
    markup.add(item1, item2)
    return markup


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome!",
                     reply_markup=generate_markup())


@bot.message_handler(func=lambda message: message.text == 'create bet')
def handle_create_bet(message):
    msg = bot.send_message(message.chat.id, 'Enter your bet in format "dd/mm/yyyy hh:MM temp":')
    bot.register_next_step_handler(msg, process_bet)


def process_bet(message):
    text = message.text
    bet_info = text.split(' ')
    date_time = bet_info[0]+' ' +bet_info[1]
    date = datetime.datetime.strptime(date_time, "%d/%m/%Y %H:%M")
    temp = bet_info[2]
    address = "mocked address " + str(random.randint(0,1000000))
    bets.append(address)
    bot.send_message(
        message.chat.id, f'Bet with date: "{date}" and temperature "{temp}" was created!', reply_markup=generate_markup())
    address = "some address"
    with open("addresses.txt", "a") as file:
        file.write(address+"\n")


@bot.message_handler(func=lambda message: message.text == 'get bets')
def handle_get_bets(message):
    if bets:
        bot.send_message(message.chat.id, '\n'.join(
            bets), reply_markup=generate_markup())
    else:
        bot.send_message(message.chat.id, 'No bets found',
                         reply_markup=generate_markup())


if __name__ == '__main__':
    print("Started")
    bot.polling(none_stop=True)
