from app import db 

class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    personal_ID = db.Column(db.Integer, nullable=False)
    profile = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    account_ID = db.Column(db.Integer, nullable=True)
    credits = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.String(50), nullable=False)
    modified_at = db.Column(db.String(50), nullable=False)
    # TODO
    # points = db.Column(db.Integer, nullable=True)
    # purchased_audios = db.Column(db.Integer, nullable=True)
    # favorites_audios = db.Column(db.String(50), nullable=False)
    # subscription_id = db.Column(db.Integer(20), nullable=False)
    # uploaded_audios = db.Column(db.Integer(20), nullable=False)