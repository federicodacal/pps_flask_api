from pps_flask_api.app import db

class Purchase(db.Model):
    __tablename__= 'ventas'
    ID = db.Column(db.Integer, primary_key=True)
    buyer_ID = db.Column(db.String(50), nullable=False)
    flow_type = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    modified_at = db.Column(db.String(50), nullable=False)