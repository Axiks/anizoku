class Anime:
    userid = None
    animeid = 0
    name = ""
    description = ""
    avatarsrc = ""
    avatarobj = None
    avatarextension = None

    def __init__(self, animeid, name, description, avatarsrc):
        self.animeid = animeid
        self.name = name
        self.description = description
        self.avatarsrc = avatarsrc


    def setAvatar(self, downloaded_file):
        self.avatarobj = downloaded_file
    
    def getAvatar(self):
        return self.avatarobj