import datetime

from sqlalchemy import func
from ..db import db

class Billing_account(db.Model):
    __tablename__= 'billing_accounts'

    ID = db.Column(db.String(50), primary_key=True)
    user_detail_ID = db.Column(db.String(50), db.ForeignKey('users_details.ID'), nullable=False)
    type = db.Column(db.String(25), nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)