from flask import jsonify, request
from ..services.favorites_service import FavoriteService

class FavoriteController:

    @staticmethod
    def get_favorites(user_id):
        users = FavoriteService.get_favorites(user_id)
        return jsonify(users), 200
    
    @staticmethod
    def add_favorite(audio_id):
        data = request.get_json()
        user_id = data.get("user_id")
        try:
            FavoriteService.add_favorite(user_id, audio_id)
            return jsonify({"message": "Audio añadido a favoritos"}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    
    @staticmethod
    def delete_favorite(audio_id):
        data = request.get_json()
        user_id = data.get("user_id")
        try:
            FavoriteService.delete_favorite(user_id, audio_id)
            return jsonify({"message": "Audio eliminado de favoritos"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404