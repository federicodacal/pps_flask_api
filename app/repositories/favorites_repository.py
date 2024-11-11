from pps_flask_api.app.models.audio import Audio
from ..databases.db import db
from ..models.favorites import Favorite

class FavoritesRepository:

    @staticmethod
    def get_favorites_by_user(user_id):
        return Favorite.query.filter_by(user_ID=user_id).join(Audio).all()
    
    @staticmethod
    def get_favorite(user_id, audio_id):
        return Favorite.query.filter_by(user_ID=user_id, ID=audio_id).first()
    
    @staticmethod 
    def add_favorite(user_id, audio_id):
        favorite = Favorite(user_ID=user_id, audio_ID=audio_id)
        db.session.add(favorite)
        db.session.commit()
        return favorite
    
    @staticmethod
    def delete_favorite(user_id, audio_id):
        favorite = Favorite.query.filter_by(user_ID=user_id, audio_ID=audio_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return True
        return False
