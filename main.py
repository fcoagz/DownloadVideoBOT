import telebot
from telebot.types import *
from pytube import YouTube
import os
from shutil import rmtree
import time

filePath = os.getcwd() + 'data/user/'
user = {} # dictionary

bot = telebot.TeleBot('TOKEN', parse_mode='HTML')

@bot.message_handler(commands=['start'])
def sendWelcome(message):
    bot.send_message(message.chat.id, '''Send me a YouTube video and I'll send it to you in seconds.''')

@bot.message_handler(content_types=['text'])
def receiveLink(message):
    user[message.chat.id] = {} # identifier
    user[message.chat.id]['url'] = message.text # save the message.text (url) in a keyword

    msg = bot.send_message(message.chat.id, '''😎 Downloading the video...''')

    try:
        yt = YouTube(user[message.chat.id]['url'])

        stream = yt.streams.filter(progressive=True, 
                                   file_extension='mp4').get_by_itag(18) # <18> 360p and <22> 720p
        stream.download(filePath+str(message.chat.id))

        content = filePath+str(message.chat.id)
        with os.scandir(content) as extractVideo:
            extractVideo = [file for file in extractVideo if file.is_file()]
        with open(extractVideo[0], 'rb') as video:
            bot.send_chat_action(message.chat.id, 'upload_video')
            bot.edit_message_text(text= '''<i>😎 Sending the video!</i>''',
                                  chat_id = message.chat.id,
                                  message_id= msg.message_id)
            bot.send_video(message.chat.id, video)
            bot.edit_message_text(text= '''<i>😎 Video sent!</i>''',
                                  chat_id = message.chat.id,
                                  message_id= msg.message_id)

            time.sleep(5)
            rmtree(content)
    except: 
        try: rmtree(content) 
        except: pass    
        bot.edit_message_text(text='''😓<i>Connection failed! Cannot download video.</i>''',
                                  chat_id= message.chat.id,
                                  message_id= msg.message_id)

if __name__ == '__main__':
    print('the bot is listening!')
    bot.infinity_polling()
