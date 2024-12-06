import datetime
import uuid
from ..databases.db import db

class Subscription_billing(db.Model):
    __tablename__= 'subscriptions_billings'

    ID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_ID = db.Column(db.String(50), db.ForeignKey('accounts.ID'), nullable=False)
    subscription_ID = db.Column(db.String(50), db.ForeignKey('subscriptions.ID'), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    last_payment_date = db.Column(db.DateTime, nullable=True)
    next_payment_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, account_ID, subscription_ID, last_payment_date, next_payment_date, state=None, ID=None, created_at=None, modified_at=None):
        self.ID = ID if ID is not None else str(uuid.uuid4())
        self.account_ID = account_ID
        self.subscription_ID = subscription_ID
        self.last_payment_date = last_payment_date 
        self.next_payment_date = next_payment_date 
        self.state = state if state is not None else "created"
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at or datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self):
        return {
            'ID': self.ID,
            'account_ID': self.account_ID,
            'subscription_ID': self.subscription_ID,
            'state': self.state,
            'last_payment_date': self.last_payment_date,
            'next_payment_date': self.next_payment_date,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }