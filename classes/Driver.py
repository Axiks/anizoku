import classes.Anime as Anime
import sqlite3
class Driver:
    def tt(self):
        print("work")
    def selectAllAnime(self):
        with sqlite3.connect('anizoku.db') as con:
            cur = con.cursor()
            cur.execute('SELECT rowid, name, description, imagesrc FROM likesAnime')
            allAnime = cur.fetchall()
            animes = [] 
            for animeDATA in allAnime:
                #print("Anime ID: " + str(animeDATA[0]))
                animes.append(Anime.Anime(animeDATA[0], animeDATA[2], animeDATA[3], animeDATA[4]))
            return animes

    def getUserAnime(self, userid):
        with sqlite3.connect('anizoku.db') as con:
            cur = con.cursor()
            vuserid = (userid,)
            cur.execute('SELECT rowid, * FROM likesAnime WHERE userid=?', vuserid)
            userAnime = cur.fetchall()
            animes = [] 
            for animeDATA in userAnime:
                #print("Anime ID: " + str(animeDATA[0]))
                animes.append(Anime.Anime(animeDATA[0], animeDATA[2], animeDATA[3], animeDATA[4]))
            return animes
    
    def getAvatar(self, animePositionId):
        with sqlite3.connect('anizoku.db') as con:
            cur = con.cursor()
            vanimePositionId = (animePositionId,)
            cur.execute('SELECT rowid, * FROM likesAnime WHERE rowid=?', vanimePositionId)
            animeAvatar = cur.fetchone()
            try:
                photo = open("image"+str(animeAvatar[0])+".jpg", 'rb')
                return photo
            except:
                photo = ""
                # print("Oops!  That Image dont open Driver")
                return ""

    def createAnime(self, userid, name, description, avatarsrc):
        with sqlite3.connect('anizoku.db') as con:
            cur = con.cursor()
            data = (userid, name, description, avatarsrc)
            cur.execute('INSERT INTO likesAnime (userid, name, description, imagesrc) VALUES (?,?,?,?)', data)
            animePositionId = cur.lastrowid
            return animePositionId


    def getAnime(self, animePositionId):
        with sqlite3.connect('anizoku.db') as con:
            cur = con.cursor()
            vanimePositionId = (animePositionId,)
            cur.execute('SELECT rowid, * FROM likesAnime WHERE rowid=?', vanimePositionId)
            animeData = cur.fetchone()

            anime = Anime.Anime(animeData[0], animeData[1], animeData[2], animeData[3])
            return anime
    
    def updateAnime(self, animePositionId, name, description, avatarsrc):
        with sqlite3.connect('anizoku.db') as con:
            cur = con.cursor()
            data = self.getAnime(animePositionId)
            if name != "":
                data.name = name
            if description != "":
                data.description = description
            if avatarsrc != "":
                data.avatarsrc = avatarsrc

            arrAnime = [data.name, data.description, data.avatarsrc, animePositionId]

            cur.execute("UPDATE likesAnime SET name = ?, description = ?, imagesrc = ? WHERE rowid = ?", arrAnime)

    # def __init__(self, animePositionId):
    #     self.getAnime(animePositionId)

    # def __init__(self, name, description, avatarsrc):
    #     self.name = name
    #     self.description = description
    #     self.avatarsrc = avatarsrc