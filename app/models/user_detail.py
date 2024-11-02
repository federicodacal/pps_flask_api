import datetime

from ..db import db

class User_detail(db.Model):
    __tablename__= 'users_details'

    ID = db.Column(db.String(50), primary_key=True)
    personal_ID = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, ID, personal_ID, profile, username, email, full_name, state, phone_number, subscription_id=None, account_ID=None, credits=None, created_at=None, modified_at=None, points=None):
        self.ID = ID
        self.personal_ID = personal_ID
        self.profile = profile
        self.username = username
        self.email = email
        self.full_name = full_name
        self.state = state
        self.phone_number = phone_number
        self.subscription_id = subscription_id
        self.account_ID = account_ID
        self.credits = credits
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at or datetime.datetime.now(datetime.timezone.utc)
        self.points = points

    # Método para representar el objeto como un diccionario
    def to_dict(self):
        return {
            "ID": self.ID,
            "personal_ID": self.personal_ID,
            "profile": self.profile,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "state": self.state,
            "phone_number": self.phone_number,
            "account_ID": self.account_ID,
            "credits": self.credits,
            "subscription_id": self.subscription_id,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "points": self.points,
        }