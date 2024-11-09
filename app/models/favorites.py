from ..databases.db import db

class Favorite(db.Model):
    __tablename__= 'favorites'
    
    ID = db.Column(db.String(50), primary_key=True)
    user_ID = db.Column(db.String(50), db.ForeignKey('users.ID'), nullable=False)
    audio_ID = db.Column(db.String(50), db.ForeignKey('audios.ID'), nullable=False)

    def __init__(self, ID, user_ID, audio_ID):
        self.ID = ID
        self.user_ID = user_ID
        self.audio_ID = audio_ID

    def to_dict(self):
        return {
            'ID': self.ID,
            'user_ID': self.user_ID,
            'audio_ID': self.audio_ID
        }