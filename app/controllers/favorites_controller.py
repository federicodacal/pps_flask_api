from flask import jsonify, request
from ..services.favorites_service import FavoriteService

class FavoriteController:

    @staticmethod
    def get_favorites(user_id):
        response, status_code = FavoriteService.get_favorites(user_id)
        return jsonify(response), status_code
    
    @staticmethod
    def add_favorite(audio_id):
        data = request.json or {}
        response, status_code = FavoriteService.add_favorite(audio_id, data)
        return jsonify(response), status_code
    
    @staticmethod
    def delete_favorite(audio_id):
        data = request.json or {}
        response, status_code = FavoriteService.delete_favorite(audio_id, data)
        return jsonify(response), status_code