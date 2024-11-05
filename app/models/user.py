import datetime

from sqlalchemy import func
from ..db import db

class User(db.Model):
    __tablename__= 'users'

    ID = db.Column(db.String(50), primary_key=True)
    user_detail_ID = db.Column(db.String(50), db.ForeignKey('users_details.ID'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    pwd = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    purchased_audios = db.relationship('Purchase', backref='buyer', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __init__(self, ID, user_detail_ID, email, pwd, type, state, created_at=None, modified_at=None):
        self.ID = ID
        self.user_detail_ID = user_detail_ID
        self.email = email
        self.pwd = pwd
        self.type = type
        self.state = state
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at or datetime.datetime.now(datetime.timezone.utc)

    # Método para representar el objeto como un diccionario
    def to_dict(self):
        return {
            "ID": self.ID,
            "user_detail_ID": self.user_detail_ID,
            "email": self.email,
            "pwd": self.pwd,
            "type": self.type,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }
    