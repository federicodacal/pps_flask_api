from datetime import timedelta
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from ..services.user_service import UserService
from ..services.auth_service import AuthService

class AuthController:

    @staticmethod
    def login():
        response = AuthService.login()
        return jsonify(response), 200
    
    @staticmethod
    def create_token():
        #response = AuthService.create_token()

        data = request.json or {}

        if not data:
            return {"message": "No se recibieron los datos"}, 400
        
        if not data.get("email") or data["email"] == '':
            return {"message": "No se ingresó el email"}, 400
        
        if not data.get("pwd") or data["pwd"] == '':
            return {"message": "No se ingresó la clave"}, 400
        
        email = data["email"]
        password = data["pwd"]

        user = UserService.get_user_by_email(email)
        
        if user is None:
            return {"message": f"Usuario con email {email} no encontrado"}, 404

        if not password == user["pwd"]:
            return {"message": "No autorizado"}, 401
        else:
            expires_in = timedelta(minutes=30)
            token = create_access_token(identity=email, expires_delta=expires_in)
            return {
                "message": "Token creado con éxito",
                "token": token,
                "user": user,
                "status_code": 200
            }, 200
    
    @staticmethod
    def logout():
        response = AuthService.logout()
        return jsonify(response), 200
    
    @staticmethod
    def register():
        response = AuthService.register()
        return jsonify(response), 200