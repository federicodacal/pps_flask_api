from sqlalchemy import func
from pps_flask_api.app import db

class Item(db.Model):
    __tablename__= 'items'
    
    ID = db.Column(db.Integer, primary_key=True)
    audio_ID = db.Column(db.String(100), nullable=False)
    creator_ID = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)