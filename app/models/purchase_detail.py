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