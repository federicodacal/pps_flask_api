import datetime

from ..db import db

class User_detail(db.Model):
    __tablename__= 'users_details'

    ID = db.Column(db.String(50), primary_key=True)
    personal_ID = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, ID, personal_ID, username, full_name, phone_number, created_at=None, modified_at=None):
        self.ID = ID
        self.personal_ID = personal_ID
        self.username = username
        self.full_name = full_name
        self.phone_number = phone_number
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at or datetime.datetime.now(datetime.timezone.utc)

    # Método para representar el objeto como un diccionario
    def to_dict(self):
        return {
            "ID": self.ID,
            "personal_ID": self.personal_ID,
            "username": self.username,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }