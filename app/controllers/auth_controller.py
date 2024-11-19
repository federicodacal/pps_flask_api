from flask import jsonify, request
from ..services.auth_service import AuthService

class AuthController:

    @staticmethod
    def login():
        response = AuthService.login()
        return jsonify(response), 200
    
    @staticmethod
    def logout():
        response = AuthService.logout()
        return jsonify(response), 200
    
    @staticmethod
    def register():
        response = AuthService.register()
        return jsonify(response), 200