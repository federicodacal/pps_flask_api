from ..repositories.favorites_repository import FavoritesRepository

class FavoriteService:

    @staticmethod
    def get_favorites(user_id):
        favorites = FavoritesRepository.get_favorites_by_user(user_id)
        
        result = []
        for favorite in favorites:
            favorite_data = favorite.to_dict()  
            
            favorite_data["audio"] = favorite.audio.to_dict() if favorite.audio else None
            result.append(favorite_data)

        return result
    
    @staticmethod 
    def add_favorite(user_id, audio_id):
        favorite = FavoritesRepository.get_favorite(user_id, audio_id)
        if favorite:
            raise ValueError("El audio ya se está en la lista de favoitos")
        
        return FavoritesRepository.add_favorite(user_id, audio_id)
    
    @staticmethod
    def delete_favorite(user_id, audio_id):
        if not FavoritesRepository.delete_favorite(user_id, audio_id):
            raise ValueError("El favorite no se encontró")