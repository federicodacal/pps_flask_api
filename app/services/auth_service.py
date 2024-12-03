from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, verify_jwt_in_request
from ..services.user_service import UserService
from ..utils.token_manager import revoke_token
from werkzeug.security import check_password_hash

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

        if not check_password_hash(user["pwd"], password):
            return {"message": "No autorizado"}, 401

        expires_in = timedelta(minutes=30)

        user_data = user 
        user_data["user_detail"] = user.get("user_detail")  
        user_data["creator"] = user.get("creator") if user.get("creator") else None 

        payload = {
            "ID": user_data["ID"],
            "email": user_data["email"],
            "type": user_data["type"],
            "full_name": user_data["user_detail"]["full_name"],
            "username": user_data["user_detail"]["username"],
            "creator_ID": user_data["creator"]["ID"] if user_data["creator"] else None
        }

        print("Payload: ")
        print(payload)
        print("\n")

        token = create_access_token(identity=payload, expires_delta=expires_in)
        
        return {
            "message": "Token creado con éxito",
            "token": token,
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
    