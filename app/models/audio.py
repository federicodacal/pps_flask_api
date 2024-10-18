from pps_flask_api.app import db

class Audio(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    creator_ID = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    audio_name = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    BPM = db.Column(db.Integer(10), nullable=False)
    tone = db.Column(db.Integer(10), nullable=False)
    length = db.Column(db.Integer(10), nullable=False)
    size = db.Column(db.Integer(10), nullable=False)
    score = db.Column(db.Integer(40), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    modified_at = db.Column(db.String(50), nullable=False)