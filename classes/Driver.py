import classes.Anime as Anime
import sqlite3
class Driver:
    def selectAllAnime(self):
        with sqlite3.connect('anizoku.db') as con:
            cur = con.cursor()
            cur.execute('SELECT rowid, name, description, imagesrc, userid FROM likesAnime')
            allAnime = cur.fetchall()
            animes = [] 
            for animeDATA in allAnime:
                #print("Anime ID: " + str(animeDATA[0]))
                anime = Anime.Anime(animeDATA[0], animeDATA[1], animeDATA[2], animeDATA[3])
                anime.userid = animeDATA[4]
                #UpLoad Avatar
                avatar = self.getAvatar(animeDATA[0])                    
                anime.setAvatar(avatar)
                animes.append(anime)
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
                anime = Anime.Anime(animeDATA[0], animeDATA[2], animeDATA[3], animeDATA[4])
                anime.userid = animeDATA[1]
                #UpLoad Avatar
                avatar = self.getAvatar(animeDATA[0])                    
                anime.setAvatar(avatar)
                animes.append(anime)
            return animes

    def getAnime(self, animePositionId):
        with sqlite3.connect('anizoku.db') as con:
            cur = con.cursor()
            vanimePositionId = (animePositionId,)
            cur.execute('SELECT rowid, * FROM likesAnime WHERE rowid=?', vanimePositionId)
            animeData = cur.fetchone()
            anime = Anime.Anime(animeDATA[0], animeDATA[2], animeDATA[3], animeDATA[4])
            anime.userid = animeDATA[1]
            #UpLoad Avatar
            avatar = self.getAvatar(animeDATA[0])                    
            anime.setAvatar(avatar)
            animes.append(anime)
            return anime
    
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
                # print("Oops!  That Image dont open Driver")
                return False
    
    def uploadAvatar(self, animePositionId, downloaded_file, extension):
        #Upload to server store
        try:
            with open("image"+ str(animePositionId) + extension, 'wb') as new_file:
                new_file.write(downloaded_file)
                return True
        except:
            return False
                
    def createAnime(self, userid, anime):
        with sqlite3.connect('anizoku.db') as con:
            cur = con.cursor()
            data = (userid, anime.name, anime.description, anime.avatarsrc)
            cur.execute('INSERT INTO likesAnime (userid, name, description, imagesrc) VALUES (?,?,?,?)', data)
            animePositionId = cur.lastrowid
            #Laod avatar to server
            avatar = anime.getAvatar()
            if avatar != None:
                if self.uploadAvatar(animePositionId, avatar, anime.avatarextension):
                    return animePositionId
                else:
                    return 0
            else:
                return animePositionId
                
    def updateAnime(self, anime):
        with sqlite3.connect('anizoku.db') as con:
            if anime.animeid == 0:
                return False
            cur = con.cursor()
            arrAnime = [anime.name, anime.description, anime.avatarsrc, anime.animeid]
            animePositionId = cur.execute("UPDATE likesAnime SET name = ?, description = ?, imagesrc = ? WHERE rowid = ?", arrAnime)
            #Laod avatar to server
            print("Anime update function. Position: " + str(animePositionId) + " . animeid: " + str(anime.animeid))
            avatar = anime.getAvatar()
            if avatar != None:
                if self.uploadAvatar(anime.animeid, avatar, anime.avatarextension):
                    return animePositionId
                else:
                    return 0
            else:
                return animePositionId
            return True                