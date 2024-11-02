import datetime

from sqlalchemy import func
from ..db import db

class Creator(db.Model):
    __tablename__= 'creators'

    ID = db.Column(db.String(50), primary_key=True)
    user_detail_ID = db.Column(db.String(50), db.ForeignKey('users_details.ID'), nullable=False)
    profile = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    account_ID = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    # Relaciones
    uploaded_audios = db.relationship('Audio', backref='creator', lazy=True)