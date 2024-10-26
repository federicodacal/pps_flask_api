from sqlalchemy import func
from pps_flask_api.app import db

class Purchase(db.Model):
    __tablename__= 'ventas'

    ID = db.Column(db.String(50), primary_key=True)
    buyer_ID = db.Column(db.String(50), db.ForeignKey('usuarios.id'), nullable=False)
    flow_type = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime, nullable=False)

    # Relaciones
    purchase_details = db.relationship('Purchase_detail', backref='purchase', lazy=True)
