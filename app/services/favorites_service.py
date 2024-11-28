from ..repositories.audio_repository import AudioRepository
from ..databases.db import db
from ..services.config_service import ConfigService
from ..repositories.favorites_repository import FavoritesRepository

class FavoriteService:

    @staticmethod
    def get_favorites(user_id):
        favorites = FavoritesRepository.get_favorites_by_user_with_audios(user_id)
        
        result = []
        for favorite in favorites:
            favorite_data = favorite.to_dict()  
            
            favorite_data["audio"] = favorite.audio.to_dict() if favorite.audio else None
            favorite_data["audio"]["file_url"] = f"{ConfigService.current_url}/audios/file/{favorite.audio.file_name}" if favorite.audio.file_name else None

            result.append(favorite_data)

        return result, 200
    
    @staticmethod 
    def add_favorite(audio_id, data):
        try:

            fav_points = 1
            
            if not data:
                return {"message": "Los datos proporcionados están vacíos"}, 400
            
            if 'user_ID' not in data:
                return {"message": "No se recibió user_ID"}, 400
            
            user_id = data.get("user_ID")
            favorite = FavoritesRepository.get_favorite(user_id, audio_id)

            if favorite:
                return {"message":"El audio ya se encuentra en la lista de favoitos"}, 400
            
            new_favorite = FavoritesRepository.add_favorite(user_id, audio_id)
            updated_audio = AudioRepository.add_points_to_audio(audio_id, fav_points)

            db.session.commit()
            
            return {
                "new_favorite": new_favorite.to_dict(),
                "updated_audio": updated_audio.to_dict() if updated_audio else None
                }, 200
        
        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
    
    @staticmethod
    def delete_favorite(audio_id, data):
        if not data:
                return {"message": "Los datos proporcionados están vacíos"}, 400
            
        if 'user_ID' not in data:
            return {"message": "No se recibió user_ID"}, 400
        
        user_id = data.get("user_ID")
        if not FavoritesRepository.delete_favorite(user_id, audio_id):
            return {"message":"El favorito no se encontró"}, 404
        else:
            updated_audio = AudioRepository.add_points_to_audio(audio_id, -1)

        db.session.commit()
        
        return {
            "message": "Favorito eliminado con éxito",
            "updated_audio": updated_audio.to_dict() if updated_audio else None
            }, 200