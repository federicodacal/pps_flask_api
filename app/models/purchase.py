import datetime
import uuid
from ..databases.db import db

class Purchase(db.Model):
    __tablename__= 'purchases'

    ID = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_ID = db.Column(db.String(50), db.ForeignKey('users.ID'), nullable=False)
    flow_type = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    # Relaciones
    purchase_details = db.relationship('Purchase_detail', backref='purchase', lazy=True)

    def __init__(self, buyer_ID, flow_type, payment_method, state, created_at=None, modified_at=None, ID=None):
        self.ID = ID if ID is not None else str(uuid.uuid4())
        self.buyer_ID = buyer_ID
        self.flow_type = flow_type
        self.payment_method = payment_method
        self.state = state
        self.created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at if modified_at else datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self):
        return {
            'ID': self.ID,
            'buyer_ID': self.buyer_ID,
            'flow_type': self.flow_type,
            'payment_method': self.payment_method,
            'state': self.state,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None
        }
    
