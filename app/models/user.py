import datetime
import uuid

from sqlalchemy import func
from ..databases.db import db

class User(db.Model):
    __tablename__= 'users'

    ID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_detail_ID = db.Column(db.String(50), db.ForeignKey('users_details.ID'), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    # Relaciones
    purchased_audios = db.relationship('Purchase', back_populates='buyer', lazy=True)
    favorites = db.relationship('Favorite', back_populates='user')
    user_detail = db.relationship("User_detail", backref="user", lazy="joined")
    creator = db.relationship("Creator", back_populates="user", uselist=False)

    def __init__(self, user_detail_ID, email, pwd, type, ID = None, state = None, created_at=None, modified_at=None):
        self.ID = ID if ID is not None else str(uuid.uuid4())
        self.user_detail_ID = user_detail_ID
        self.email = email
        self.pwd = pwd
        self.type = type
        self.state = state if state is not None else "created"
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
            "state": self.state,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }
    