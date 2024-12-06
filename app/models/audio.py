import datetime
import uuid
from sqlalchemy import func
from ..databases.db import db

class Audio(db.Model):
    __tablename__= 'audios'

    ID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_ID = db.Column(db.String(50), db.ForeignKey('creators.ID'), nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    audio_name = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    BPM = db.Column(db.Integer, nullable=False)
    tone = db.Column(db.String(20), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)
    
    # Relaciones
    item = db.relationship('Item', back_populates='audio', uselist=False, lazy='joined')
    creator = db.relationship('Creator', back_populates='audios', uselist=False)
    favorites = db.relationship('Favorite', back_populates='audio')

    def __init__(self, creator_ID, file_name, audio_name, category, genre, BPM,
                 tone, length, size, description, state=None, score=None, created_at=None, modified_at=None, ID=None):
        self.ID = ID if ID is not None else str(uuid.uuid4())
        self.creator_ID = creator_ID
        self.file_name = file_name
        self.audio_name = audio_name
        self.state = state if state is not None else "created"
        self.category = category
        self.genre = genre
        self.BPM = BPM
        self.tone = tone
        self.length = length
        self.size = size
        self.score = score
        self.description = description
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
            "description": self.description,
            "score": self.score,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }