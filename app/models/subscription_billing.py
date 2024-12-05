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