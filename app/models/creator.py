import datetime
import uuid

from sqlalchemy import func
from ..databases.db import db

class Creator(db.Model):
    __tablename__= 'creators'

    ID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_ID = db.Column(db.String(50), db.ForeignKey('users.ID'), nullable=False)
    subscription_ID = db.Column(db.String(50), nullable=False)
    profile = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    # Relaciones
    account = db.relationship('Account', back_populates='creator', uselist=False)
    audios = db.relationship('Audio', back_populates='creator', lazy=True)
    user = db.relationship('User', back_populates='creator', lazy='joined')

    def __init__(self, user_ID, profile, subscription_ID, ID=None, state = None, points=None, credits=None, created_at=None, modified_at=None):
        self.ID = ID if ID is not None else str(uuid.uuid4())
        self.user_ID = user_ID
        self.profile = profile
        self.state = state if state is not None else "created"
        self.points = points if points is not None else 0
        self.credits = credits if credits is not None else 0
        self.subscription_ID = subscription_ID
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at or datetime.datetime.now(datetime.timezone.utc)

    # Método para representar el objeto como un diccionario
    def to_dict(self):
        return {
            "ID": self.ID,
            "user_ID": self.user_ID,
            "profile": self.profile,
            "points": self.points,
            "credits": self.credits,
            "state": self.state,
            "subscription_ID": self.subscription_ID,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }