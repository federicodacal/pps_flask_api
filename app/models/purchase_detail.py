import datetime
from sqlalchemy import func
from pps_flask_api.app import db

class Purchase_detail(db.Model):
    __tablename__= 'detalles_ventas'

    ID = db.Column(db.String(50), primary_key=True)
    purchase_ID = db.Column(db.String(50), db.ForeignKey('ventas.ID'), nullable=True)
    item_ID = db.Column(db.String(50), db.ForeignKey('items.ID'), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    modified_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, ID, purchase_ID, item_ID, state, created_at=None, modified_at=None):
        self.ID = ID
        self.purchase_ID = purchase_ID
        self.item_ID = item_ID
        self.state = state
        self.created_at = created_at if created_at else datetime.datetime.now(datetime.timezone.utc)
        self.modified_at = modified_at if modified_at else datetime.datetime.now(datetime.timezone.utc)

    def to_dict(self):
        return {
            'ID': self.ID,
            'purchase_ID': self.purchase_ID,
            'item_ID': self.item_ID,
            'state': self.state,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'modified_at': self.modified_at.isoformat() if self.modified_at else None,
        }
    