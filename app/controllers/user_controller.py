from flask import jsonify, request
from ..services.user_service import UserService

class UserController:

    @staticmethod
    def get_users():
        users = UserService.get_all_users()
        return jsonify(users), 200
    
    @staticmethod
    def get_user(user_id):
        user = UserService.get_user_by_id(user_id)
        if user is None:
            return {"error": "Usuario no encontrado"}, 404
        return jsonify(user), 200
    
    @staticmethod
    def create_user():
        data = request.json or {}

        try:
            user_data = UserService.create_user(data)
            return jsonify(user_data), 201
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
        
    @staticmethod
    def update_user(user_id):
        data = request.json or {}
        
        try:
            updated_user = UserService.update_user(user_id, data)
            if not updated_user["user"]:
                return {"error": "Usuario no encontrado"}, 404
            return jsonify(updated_user), 200
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500

