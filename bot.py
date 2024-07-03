import os
import time
import telebot
from pytube import YouTube
from video_loader import Download  # Assuming this handles downloading

BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN or BOT_TOKEN == 'YOUR_TELEGRAM_BOT_API_TOKEN':
    raise ValueError("Please set your Telegram bot API token.")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help', 'settings'])
def send_welcome(message):
    sent_message = bot.reply_to(message, """\
Usage: 
/download [youtube_link]
/search [Your query, name of the video]
""")
    time.sleep(5)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")
    try:
        bot.delete_message(sent_message.chat.id, sent_message.message_id)
    except Exception as e:
        print(f"Error deleting bot message: {e}")


@bot.message_handler(commands=['download'])
def send_audio(message):
    if not message.text:
        bot.reply_to(message, "Please provide a valid YouTube video URL.")
        return

    try:
        # Extract the link from the message text
        command, link = message.text.split(maxsplit=1)
        mp3_path = Download(link)  # Assuming this function downloads and returns the path to the downloaded audio file

        if mp3_path:
            with open(mp3_path, 'rb') as audio_file:
                bot.send_audio(message.chat.id, audio=audio_file)
            os.remove(mp3_path)
        else:
            bot.reply_to(message, "An error occurred while downloading or converting the video.")

        bot.delete_message(message.chat.id, message.message_id)
    except ValueError:
        bot.reply_to(message, "Please provide a valid YouTube video URL.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")


@bot.message_handler(commands=['search'])
def search_video(message):
    if not message.text:
        bot.reply_to(message, "Please provide a query to search for YouTube videos.")
        return

    try:
        command, query = message.text.split(maxsplit=1)
        search_results = YouTube().search(query)

        if search_results:
            # Assuming you want to send the first result as a message
            video = search_results[0]
            response = f"Title: {video.title}\nLink: {video.watch_url}"
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "No results found for your query.")

        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")


@bot.message_handler(commands=['clear_chat'])
def clear_all_chat(message):
    # Placeholder implementation for clear_all_chat
    # Implement the logic to clear chat here if needed
    bot.reply_to(message, "Chat clearing functionality is not yet implemented.")


bot.infinity_polling()
