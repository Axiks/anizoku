import threading

import telebot
bot = telebot.TeleBot('1390196402:AAGrNlTMegTG86EwtwlckHiJnkzfsK6nMJw')

#Var
global btnaddanime
global addanimeid
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
    with sqlite3.connect('anizoku.db') as con:
        cur = con.cursor()
        vuserid = (userid,)
        cur.execute('SELECT rowid, * FROM likesAnime WHERE userid=?', vuserid)
        result = cur.fetchall()
        print(result)
        for anime in result:
            mess = "*" + anime[2]+ "*" + "\n\n" + anime[3]
            bot.send_message(chatid, mess, parse_mode= 'Markdown')
            try:
                photo = open("image"+str(anime[0])+".jpg", 'rb')
                bot.send_photo(chatid, photo)
            except:
                print("Oops!  That Image dont open")

def add_like_anime(userid, name, description):
    with sqlite3.connect('anizoku.db') as con:
        cur = con.cursor()
        data = (userid, name, description)
        cur.execute('INSERT INTO likesAnime (userid, name, description) VALUES (?,?,?)', data)

        global addanimeid
        addanimeid = cur.lastrowid

#Keyboard
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/MyAnime', '/AddAnime')

#Function
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт, ти написав мені /start. Дякую :3' , reply_markup=keyboard1)
    bot.send_message(message.chat.id, 'Даний бот допоможе тобі познайомитись з вподобаннями твоїх друзів в аніме). Також зможеш знайти знайомих з такими самими любими аніме як в тебе)')
# @bot.message_handler(commands=['Profile'])
# def profile_view(message):
#         bot.send_message(message.chat.id, 'Ооо. А це твій профіль. Мій список аніме:')
#         # message.from_user.id
# @bot.message_handler(commands=['Image'])
# def random_photo(message):
#     print(message)
#     photo = open('/home/neko/Pobrane/2a8de532-fcc6-4309-b4c5-2a58cef5b8c2.jpg', 'rb')
#     bot.send_photo(message.chat.id, photo)
#     bot.send_message(message.chat.id, 'Це фото.')
@bot.message_handler(commands=['AddAnime'])
def add_title(message):
    bot.send_message(message.chat.id, 'Ти написав мені Добавити Аніме. Введи імя тайтлу)')
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
    global btnaddanime
    print(btnaddanime)
    if btnaddanime:
        add_like_anime(message.from_user.id, message.text, "Descr")
        #bot.send_message(message.chat.id, 'Шукаю: ' + message.text)
        bot.send_message(message.chat.id, 'Anime add: ' + message.text + '. Pleace write description or upload Avatar')
        btnaddanime = False
    #bot.reply_to(message, message.text)
@bot.message_handler(content_types=['photo'])
def photoSave(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    global addanimeid
    with open("image"+ str(addanimeid) +".jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

bot.polling()