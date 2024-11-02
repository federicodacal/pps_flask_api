from ..db import db

class Favorite(db.Model):
    __tablename__= 'favorites'
    
    ID = db.Column(db.String(50), primary_key=True)
    user_ID = db.Column(db.String(50), db.ForeignKey('users.ID'), nullable=False)
    audio_ID = db.Column(db.String(50), db.ForeignKey('audios.ID'), nullable=False)