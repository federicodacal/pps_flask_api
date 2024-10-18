from pps_flask_api.app import db

class Item(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    audio_ID = db.Column(db.String(100), primary_key=True)
    creator_ID = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    modified_at = db.Column(db.String(50), nullable=False)