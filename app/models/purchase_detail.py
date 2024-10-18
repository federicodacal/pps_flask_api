from pps_flask_api.app import db

class Purchase_detail(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    purchase_ID = db.Column(db.String(100), nullable=True)
    item_ID = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.String(50), nullable=False)
    modified_at = db.Column(db.String(50), nullable=False)