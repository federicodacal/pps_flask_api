from app import db

class Favorite(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.Integer, primary_key=True)
    audio_ID = db.Column(db.String(100), nullable=False)