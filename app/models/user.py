import datetime

from sqlalchemy import func
from pps_flask_api.app import db

class User(db.Model):
    __tablename__= 'usuarios'

    id = db.Column(db.String(50), primary_key=True)
    personal_ID = db.Column(db.Integer, nullable=False)
    profile = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    account_ID = db.Column(db.Integer, nullable=True)
    credits = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    subscription_id = db.Column(db.Integer, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)
    points = db.Column(db.Integer, nullable=True)
    
    # Relaciones
    purchased_audios = db.relationship('Purchase', backref='buyer', lazy=True)
    uploaded_audios = db.relationship('Audio', backref='creator', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    favorite_audios = db.relationship('Audio', secondary='favoritos', backref='favorited_by_users', lazy='dynamic')

    def __init__(self, id, personal_ID, profile, username, email, full_name, state, phone_number,
                 account_ID=None, credits=None, created_at=None, modified_at=None, points=None):
        self.id = id
        self.personal_ID = personal_ID
        self.profile = profile
        self.username = username
        self.email = email
        self.full_name = full_name
        self.state = state
        self.phone_number = phone_number
        self.account_ID = account_ID
        self.credits = credits
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at or datetime.datetime.now(datetime.timezone.utc)
        self.points = points

    # Método para representar el objeto como un diccionario
    def to_dict(self):
        return {
            "id": self.id,
            "personal_ID": self.personal_ID,
            "profile": self.profile,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "state": self.state,
            "phone_number": self.phone_number,
            "account_ID": self.account_ID,
            "credits": self.credits,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "points": self.points,
        }