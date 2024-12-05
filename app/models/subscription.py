import uuid
from ..databases.db import db

class Subscription(db.Model):
    __tablename__= 'subscriptions'

    ID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = db.Column(db.String(25), nullable=False) 
    renewal_time_in_days = db.Column(db.Integer, nullable=False) 
    revenue_percentage = db.Column(db.Float, nullable=False) 
    monthly_price = db.Column(db.Float, nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)
