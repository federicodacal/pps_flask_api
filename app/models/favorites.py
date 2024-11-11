import uuid
from ..databases.db import db

class Favorite(db.Model):
    __tablename__= 'favorites'
    
    ID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_ID = db.Column(db.String(50), db.ForeignKey('users.ID'), nullable=False)
    audio_ID = db.Column(db.String(50), db.ForeignKey('audios.ID'), nullable=False)

    # Relaciones
    user = db.relationship("User", back_populates="favorites")
    audio = db.relationship("Audio", back_populates="favorites")

    def __init__(self, user_ID, audio_ID, ID=None):
        self.ID = ID if ID is not None else str(uuid.uuid4())
        self.user_ID = user_ID
        self.audio_ID = audio_ID

    def to_dict(self):
        return {
            'ID': self.ID,
            'user_ID': self.user_ID,
            'audio_ID': self.audio_ID
        }