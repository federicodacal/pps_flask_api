from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, verify_jwt_in_request
from ..services.user_service import UserService
from ..utils.token_manager import revoke_token

class AuthService:

    @staticmethod
    def create_token(data):
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
    @jwt_required()
    def logout():
        verify_jwt_in_request()
        jti = get_jwt()["jti"]
        revoke_token(jti)
        return {"message": "Token cancelado con éxito"}, 200
    
    @staticmethod
    def register():
        return 'Register service'
    