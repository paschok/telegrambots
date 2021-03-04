import telebot
from telebot import types

import config
import random

bot = telebot.TeleBot(config.TOKEN)

keyBoardAnswer_1 = '🎲 Give me random number'
keyBoardAnswer_2 = '😊 How u doin?'


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('media/welcome.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # normal keyboard at the bottom of the chat
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard=True == small keyboard
    item1 = types.KeyboardButton(keyBoardAnswer_1)
    item2 = types.KeyboardButton(keyBoardAnswer_2)

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Oh,  {0.first_name}, hi... geez \nI am - <b>{1.first_name}</b>, bot developed to annoy U."
                     "\nI will repeat after you or do little tasks.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def respond(message):
    if message.chat.type == 'private':
        if message.text == keyBoardAnswer_1:
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == keyBoardAnswer_2:

            # keyboard at the bottom of the message
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Not bad for today", callback_data='good')
            item2 = types.InlineKeyboardButton("It sucks", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Shitty as always. And you?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Happy to hear that 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Shit happens, brah 😢')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=keyBoardAnswer_2, reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Alert! Alert! Testing!!")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)