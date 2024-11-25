from flask import jsonify, request
from ..services.auth_service import AuthService

class AuthController:

    @staticmethod
    def login():
        data = request.json or {}
        response, status_code = AuthService.create_token(data)
        return jsonify(response), status_code
    
    @staticmethod
    def logout():
        response, status_code = AuthService.logout()
        return jsonify(response), status_code
    
    @staticmethod
    def register():
        response = AuthService.register()
        return jsonify(response), 200