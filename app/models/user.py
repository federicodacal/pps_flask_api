from datetime import datetime

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
    modified_at = db.Column(db.DateTime, nullable=False)
    points = db.Column(db.Integer, nullable=True)
    # TODO
    # favorites_audios = db.Column(db.String(50), nullable=False)
    # subscription_id = db.Column(db.Integer(20), nullable=False)
    
    # Relaciones
    purchased_audios = db.relationship('Purchase', backref='buyer', lazy=True)
    uploaded_audios = db.relationship('Audio', backref='creator', lazy=True)