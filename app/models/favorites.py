from pps_flask_api.app import db

class Favorite(db.Model):
    __tablename__= 'favoritos'
    
    ID = db.Column(db.String(50), primary_key=True, autoincrement=True)
    user_ID = db.Column(db.String(50), nullable=False)
    audio_ID = db.Column(db.String(50), nullable=False)