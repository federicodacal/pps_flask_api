from ..utils.validators import validate_user, validate_creator
from ..middlewares.api_exception import APIException
from ..repositories.user_repository import UserRepository
from ..repositories.user_detail_repository import UserDetailRepository
from ..repositories.creator_repository import CreatorRepository
from ..repositories.account_repository import AccountRepository
from ..databases.db import db

class UserService:

    @staticmethod
    def get_all_users():
        users = UserRepository.get_all_users_with_details_and_creators()

        result = []
        for user in users:
            user_data = user.to_dict()  
        
            user_data["user_detail"] = user.user_detail.to_dict() if user.user_detail else None
            user_data["creator"] = user.creator.to_dict() if user.creator else None
            result.append(user_data)

        return result, 200

    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_user_by_id_with_details(user_id)
        if user is None:
            return {"message": f"Usuario con id {user_id} no encontrado"}, 404
        
        user_data = user.to_dict()
        user_data["user_detail"] = user.user_detail.to_dict() if user.user_detail else None
        user_data["creator"] = user.creator.to_dict() if user.creator else None

        return user_data, 200

    @staticmethod
    def create_user(data):
        try:
            if not data:
                return {"message": "Los datos proporcionados están vacíos"}, 400
            
            validation, msg = validate_user(data)
            if not validation:
                return {"message":msg}, 400
            
            with db.session.begin():

                new_user_detail = UserDetailRepository.create_user_detail(data)
                new_user = UserRepository.create_user(data)
                new_creator = None
                new_account = None

                if data.get('type') == 'creator':

                    validation, msg = validate_creator(data)
                    if not validation:
                        raise APIException(msg, status_code=400, error_type="Value Error")

                    new_creator = CreatorRepository.create_creator(data)
                    new_account = AccountRepository.create_account(data)

            db.session.commit()

            return {
                "user": new_user.to_dict(),
                "user_detail": new_user_detail.to_dict(),
                "creator": new_creator.to_dict() if new_creator else None,
                "account": new_account.to_dict() if new_account else None
            }, 200
        except APIException as aex:
            db.session.rollback()
            return {"message": str(aex), "error_type": aex.error_type}, aex.status_code
        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
        

    @staticmethod
    def update_user(user_id, data):
        try:
            if not data: 
                return {"message": "Los datos proporcionados están vacíos"}, 400

            user = UserRepository.get_user_by_id_with_details(user_id)
            if not user:
                return {"message": f"Usuario con id {user_id} no encontrado"}, 404
            
            validation, msg = validate_user(data, action="update")
            if not validation:
                return {"message":msg}, 400

            updated_user_detail = UserDetailRepository.update_user_detail(user.user_detail_ID, data)
            updated_user = UserRepository.update_user(user.ID, data)
            updated_creator = None
            updated_account = None

            if data.get('type') == 'creator':
                creator = CreatorRepository.get_creator_by_user_id(user.ID)

                validation, msg = validate_creator(data)
                if not validation:
                    return {"message":msg}, 400

                if creator:
                    updated_creator = CreatorRepository.update_creator(creator.ID, data)
                    updated_account = AccountRepository.update_account(creator.ID, data)

                else:
                    updated_creator = CreatorRepository.create_creator(data)
                    updated_account = AccountRepository.create_account(data)
            
            db.session.commit()
            
            return {
                "user": updated_user.to_dict() if updated_user else None,
                "user_detail": updated_user_detail.to_dict() if updated_user_detail else None,
                "creator": updated_creator.to_dict() if updated_creator else None,
                "account": updated_account.to_dict() if updated_account else None
            }, 200
        except APIException as aex:
            db.session.rollback()
            return {"message": str(aex), "error_type": aex.error_type}, aex.status_code
        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
