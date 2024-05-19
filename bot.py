import os
import telebot
from telebot import types
from video_loader import Download

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help', 'settings'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['start', 'help', 'settings'])
def send_audio(message):

    bot.send_audio(audio=open('tests/test.mp3', 'rb'))

@bot.message_handler(commands=['clear_chat'])
def clear_all_chat():
    pass

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
