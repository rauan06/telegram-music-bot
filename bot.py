import os
import telebot
from telebot import types
from video_loader import Download

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help', 'settings'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['download'])
def send_audio(message):
    if not message.text:
        bot.reply_to(message, "Please provide a valid YouTube video URL.")
        return
    
    try:
        # Extract the link from the message text
        command, link = message.text.split(maxsplit=1)
        mp3_path = Download(link)
        
        if mp3_path:
            with open(mp3_path, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio=audio_file)
            os.remove(mp3_path)
        else:
            bot.reply_to(message, "An error occurred while downloading or converting the video.")
    except ValueError:
        bot.reply_to(message, "Please provide a valid YouTube video URL.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")


@bot.message_handler(commands=['clear_chat'])
def clear_all_chat():
    pass


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
