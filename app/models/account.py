import datetime

from sqlalchemy import func
from ..databases.db import db

class Account(db.Model):
    __tablename__= 'accounts'

    ID = db.Column(db.String(50), primary_key=True)
    creator_ID = db.Column(db.String(50), db.ForeignKey('creators.ID'), nullable=False)
    personal_account_ID = db.Column(db.String(50))
    type = db.Column(db.String(25), nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    # Relaciones
    creator = db.relationship('Creator', back_populates='account', uselist=False)

    def __init__(self, ID, creator_ID, personal_account_ID, type, created_at=None, modified_at=None):
        self.ID = ID
        self.creator_ID = creator_ID
        self.personal_account_ID = personal_account_ID
        self.type = type
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at or datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self):
        return {
            'ID': self.ID,
            'creator_ID': self.creator_ID,
            'personal_account_ID': self.personal_account_ID,
            'type': self.type,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }