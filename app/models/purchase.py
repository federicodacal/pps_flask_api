import datetime
from ..db import db

class Purchase(db.Model):
    __tablename__= 'purchases'

    ID = db.Column(db.String(50), primary_key=True)
    buyer_ID = db.Column(db.String(50), db.ForeignKey('users.ID'), nullable=False)
    flow_type = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    # Relaciones
    purchase_details = db.relationship('Purchase_detail', backref='purchase', lazy=True)

    def __init__(self, ID, buyer_ID, flow_type, currency, payment_method, state, created_at=None, modified_at=None):
        self.ID = ID
        self.buyer_ID = buyer_ID
        self.flow_type = flow_type
        self.currency = currency
        self.payment_method = payment_method
        self.state = state
        self.created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at if modified_at else datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self):
        return {
            'ID': self.ID,
            'buyer_ID': self.buyer_ID,
            'flow_type': self.flow_type,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'state': self.state,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None
        }
    
