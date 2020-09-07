import os.path
from classes import Driver
from classes import Anime
#from classes import driver
#import classes.driver as driver

import threading

import telebot
bot = telebot.TeleBot('1390196402:AAGrNlTMegTG86EwtwlckHiJnkzfsK6nMJw')

#Var
global btnaddanime
global addanimename
global addanimedescription
global addanimeavatar
global addanimeid
global animePreSave
global userId
global chatId
global messageBuffer
messageBuffer = ""
chatId = 0
userId = 0
animePreSave = Anime.Anime
addanimename = False
addanimedescription = False
addanimeavatar = False
btnaddanime = False
addanimeid = 0
#db
import sqlite3
    # cur.execute("""CREATE TABLE likesAnime (
    #     userid TEXT,
    #     name TEXT,
    #     description TEXT
    #     imagesrc TEXT
    # )""")

def select_like_anime(userid, chatid):
    d = Driver.Driver()
    userAnime = d.getUserAnime(userid)
    for anime in userAnime:
        mess = "*" + anime.name+ "*" + "\n\n" + anime.description
        bot.send_message(chatid, mess, parse_mode= 'Markdown')
        photo = anime.getAvatar()
        try:
            bot.send_photo(chatid, photo)
        except:
            print("Oops!  That Image dont open")
            
def add_like_anime(userid, name, description):
    d = Driver.Driver()
    a = Anime.Anime("", name, description, "")
    a.userId = userid
    #lastrowid = d.createAnime(userid, name, description, "")
    lastrowid = d.createAnime(userid, a)
    global addanimeid
    addanimeid = lastrowid


def add_anime():
    global btnaddanime
    global animePreSave
    global addanimename
    global addanimedescription
    global chatId
    global userId
    global messageBuffer
    global addanimeavatar
    
    #Добавлення аніме в ОЗУ
    if btnaddanime:
        if addanimename == False:
            #Добавлення назви
            animePreSave.name = messageBuffer
            addanimename = True
            bot.send_message(chatId, "Введи опис до аніме: '" + animePreSave.name + "'")
            addanimeavatar = True
            return 0
        if addanimename == True and addanimedescription == False:
            #Добавлення опису
            animePreSave.description = messageBuffer
            addanimedescription = True
        
        if addanimename == True and addanimedescription == True:
            add_like_anime(userId, animePreSave.name, animePreSave.description)
            #bot.send_message(message.chat.id, 'Шукаю: ' + message.text)
            #bot.send_message(message.chat.id, 'Аніме добавлено в нашу базу даних. Някую)')
            btnaddanime = False
            addanimename = False
            addanimedescription = False
        

#Keyboard
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/MyAnime', '/AddAnime', '/AllAnime')

#Function
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт, ти написав мені /start. Дякую :3' , reply_markup=keyboard1)
    bot.send_message(message.chat.id, 'Даний бот допоможе тобі познайомитись з вподобаннями твоїх друзів в аніме). Також зможеш знайти знайомих з такими самими любими аніме як в тебе)')

@bot.message_handler(commands=['AllAnime'])
def all_anime(message):
     d = Driver.Driver()
     allAnime = d.selectAllAnime()
     for anime in allAnime:
        mess = "*" + anime.name+ "*" + "\n\n" + anime.description
        bot.send_message(message.from_user.id, mess, parse_mode= 'Markdown')
        try:
            photo = anime.getAvatar()
            bot.send_photo(message.from_user.id, photo)
        except:
            print("Oops!  That Image dont open")
    
@bot.message_handler(commands=['AddAnime'])
def add_title(message):
    bot.send_message(message.chat.id, 'НЯ :3 Як називається аніме?')
    global btnaddanime
    btnaddanime = True
    #title = message.text
    #bot.send_message(message.chat.id, title, reply_markup=keyboard1)
    #select_like_anime()
@bot.message_handler(commands=['MyAnime'])
def my_title(message):
    t = threading.Thread(target=select_like_anime, name='ThreadDB', args=(message.from_user.id, message.chat.id, ))
    t.start()
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global chatId
    global userId
    global messageBuffer
    userId = message.from_user.id
    chatId = message.chat.id
    messageBuffer = message.text
    print(btnaddanime)
    add_anime()
@bot.message_handler(content_types=['photo'])
def photoSave(message):
    global addanimeavatar
    global animePreSave
    global btnaddanime
    if addanimeavatar:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        # unpacking the tuple
        extension = os.path.splitext(file_info.file_path)[1]
        if False:
        #if btnaddanime == True:
            animePreSave.setAvatar(downloaded_file)
        else:
            global addanimeid
            d = Driver.Driver()
            d.uploadAvatar(addanimeid, downloaded_file, extension)
            addanimeavatar = False

bot.polling()