import datetime
from sqlalchemy import func
from ..databases.db import db

class Item(db.Model):
    __tablename__= 'items'
    
    ID = db.Column(db.String(50), primary_key=True)
    creator_ID = db.Column(db.String(50), db.ForeignKey('creators.ID'), nullable=False)
    audio_ID = db.Column(db.String(50), db.ForeignKey('audios.ID'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relaciones 
    purchase_detail = db.relationship('Purchase_detail', backref='item', lazy=True)

    def __init__(self, ID, creator_ID, audio_ID, price, state, created_at=None, modified_at=None):
        self.ID = ID
        self.creator_ID = creator_ID
        self.audio_ID = audio_ID
        self.price = price
        self.state = state
        self.created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at if modified_at else datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self):
        return {
            'ID': self.ID,
            'creator_ID': self.creator_ID,
            'audio_ID': self.audio_ID,
            'price': self.price,
            'state': self.state,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None,
        }