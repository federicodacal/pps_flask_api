import datetime
from sqlalchemy import func
from ..db import db

class Audio(db.Model):
    __tablename__= 'audios'

    ID = db.Column(db.String(50), primary_key=True)
    creator_ID = db.Column(db.String(50), db.ForeignKey('creators.ID'), nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    audio_name = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    BPM = db.Column(db.Integer, nullable=False)
    tone = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, ID, creator_ID, file_name, audio_name, state, category, genre, BPM,
                 tone, length, size, description, score=None, created_at=None, modified_at=None):
        self.ID = ID
        self.creator_ID = creator_ID
        self.file_name = file_name
        self.audio_name = audio_name
        self.state = state
        self.category = category
        self.genre = genre
        self.BPM = BPM
        self.tone = tone
        self.length = length
        self.size = size
        self.description = description
        self.score = score
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at or datetime.datetime.now(datetime.timezone.utc)

    # Método para representar el objeto como un diccionario
    def to_dict(self):
        return {
            "ID": self.ID,
            "creator_ID": self.creator_ID,
            "file_name": self.file_name,
            "audio_name": self.audio_name,
            "state": self.state,
            "category": self.category,
            "genre": self.genre,
            "BPM": self.BPM,
            "tone": self.tone,
            "length": self.length,
            "size": self.size,
            "score": self.score,
            "description": self.description,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }