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
    