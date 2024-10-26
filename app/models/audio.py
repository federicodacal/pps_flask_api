from sqlalchemy import func
from pps_flask_api.app import db

class Audio(db.Model):
    __tablename__= 'audios'

    ID = db.Column(db.String(50), primary_key=True)
    creator_ID = db.Column(db.String(50), db.ForeignKey('usuarios.id'), nullable=False)
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