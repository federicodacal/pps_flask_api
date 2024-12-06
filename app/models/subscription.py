import datetime
import uuid
from ..databases.db import db

class Subscription(db.Model):
    __tablename__= 'subscriptions'

    ID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = db.Column(db.String(25), nullable=False) 
    state = db.Column(db.String(25), nullable=False) 
    renewal_time_in_days = db.Column(db.Integer, nullable=False) 
    revenue_percentage = db.Column(db.Float, nullable=False) 
    monthly_price = db.Column(db.Float, nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, renewal_time_in_days, revenue_percentage, monthly_price, type, state=None, ID=None, created_at=None, modified_at=None):
        self.ID = ID if ID is not None else str(uuid.uuid4())
        self.renewal_time_in_days = renewal_time_in_days
        self.revenue_percentage = revenue_percentage
        self.monthly_price = monthly_price
        self.state = state if state is not None else "active"
        self.type = type
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at or datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self):
        return {
            'ID': self.ID,
            'renewal_time_in_days': self.renewal_time_in_days,
            'revenue_percentage': self.revenue_percentage,
            'monthly_price': self.monthly_price,
            'type': self.type,
            'state': self.state,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }