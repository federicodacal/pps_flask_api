from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request
from ..utils.token_manager import revoke_token

class AuthService:

    @staticmethod
    def create_token():
        return 'Login service'
    
    @staticmethod
    def register():
        return 'Register service'
    
    @staticmethod
    @jwt_required()
    def logout():
        verify_jwt_in_request()
        jti = get_jwt()["jti"]
        revoke_token(jti)
        print("\nSe cancela el token\n")
        return {"message": "Token cancelado con éxito"}, 200
    