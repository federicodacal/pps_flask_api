from ..db import db

class Favorite(db.Model):
    __tablename__= 'favoritos'
    
    ID = db.Column(db.String(50), primary_key=True)
    user_ID = db.Column(db.String(50), db.ForeignKey('usuarios.id'), nullable=False)
    audio_ID = db.Column(db.String(50), db.ForeignKey('audios.ID'), nullable=False)