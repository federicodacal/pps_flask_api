import datetime
from werkzeug.security import generate_password_hash

from ..repositories.subscription_repository import SubscriptionRepository
from ..repositories.subscription_billing_repository import SubscriptionBillingRepository
from ..repositories.audio_repository import AudioRepository
from ..repositories.item_repository import ItemRepository
from ..services.audio_service import AudioService
from ..models.audio import Audio
from ..services.mail_service import MailService
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
        if user.creator and user.creator.account:
            user_data["creator"]["account"] = user.creator.account.to_dict()
        else:
            user_data["account"] = None

        return user_data, 200
    
    @staticmethod
    def get_user_by_email(email):
        user = UserRepository.get_user_by_email_with_details(email)

        if user is None:
            return {"message": f"Usuario con email {email} no encontrado"}, 404    
            
        user_data = user.to_dict()
        user_data["user_detail"] = user.user_detail.to_dict() if user.user_detail else None
        user_data["creator"] = user.creator.to_dict() if user.creator else None

        return user_data, 200
    
    @staticmethod
    def get_user_by_username(username):
        user = UserRepository.get_user_by_username_with_details(username)

        if user is None:
            return {"message": f"Usuario con username {username} no encontrado"}, 404    
            
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
                data["user_detail_ID"] = new_user_detail.ID

                pwd = data.get("pwd")
                hashed_password = generate_password_hash(pwd)
                data["pwd"] = hashed_password

                new_user = UserRepository.create_user(data)
                data["ID"] = new_user.ID

                new_creator = None
                new_account = None
                new_subscription_billing = None

                if data.get('type') == 'creator':

                    validation, msg = validate_creator(data)
                    if not validation:
                        raise APIException(msg, status_code=400, error_type="Value Error")

                    new_creator = CreatorRepository.create_creator(data)
                    data["creator_ID"] = new_creator.ID

                    new_account = AccountRepository.create_account(data)

                    subscription = SubscriptionRepository.get_subscription_by_id(data["subscription_ID"])

                    if not subscription:
                        raise APIException('No se encontró la subscripción', status_code=400, error_type="Integrity Error")   
                    
                    data["last_payment_date"] = None
                    data["next_payment_date"] = datetime.datetime.now() + datetime.timedelta(days=subscription.renewal_time_in_days) 
                    data["account_ID"] = new_account.ID

                    new_subscription_billing = SubscriptionBillingRepository.create_subscription_billing(data)

            db.session.commit()

            confirmation_email, status_code = MailService.send_confirmation_email(new_user.email, new_user_detail.full_name, new_user.ID)

            return {
                "user": new_user.to_dict(),
                "user_detail": new_user_detail.to_dict(),
                "creator": new_creator.to_dict() if new_creator else None,
                "account": new_account.to_dict() if new_account else None,
                "confirmation_email": confirmation_email if confirmation_email else None,
                "new_subscription_billing": new_subscription_billing.to_dict() if new_subscription_billing else None
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
        
    @staticmethod
    def update_user_state(user_id, updated_state):
        try: 
            user = UserRepository.get_user_by_id_with_details(user_id)
            if user is None:
                return {"message": f"Usuario con id {user_id} no encontrado"}, 404
            
            updated_user = UserRepository.update_state_user(user_id, updated_state)

            updated_creator = None
            if(user.type == 'creator'):
                creator = CreatorRepository.get_creator_by_user_id(user_id)
                if creator is not None:
                    updated_creator = CreatorRepository.update_state_creator(creator.ID, updated_state)

            user_data = user.to_dict()
            user_data["user_detail"] = user.user_detail.to_dict() if user.user_detail else None
            
            if updated_state == 'active':
                mail, status = MailService.send_approval_email(user_data)
            elif updated_state == 'inactive':
                mail, status = MailService.send_rejection_email(user_data)

            db.session.commit()

            return {
                "message":f"El usuario: {user_id} ahora es {updated_state}",
                "user": updated_user.to_dict() if updated_user else None,
                "creator": updated_creator.to_dict() if updated_creator else None,
                "mail": mail if mail else None
            }, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
        
    @staticmethod
    def update_creator_state(creator_id, updated_state):
        try:
            creator = CreatorRepository.get_creator_with_audios(creator_id)
            if creator is None:
                return {"message": f"Creator con id {creator} no encontrado"}, 404
            
            updated_creator = CreatorRepository.update_state_creator(creator_id, updated_state)

            updated_audios = []
            for audio in creator.audios:
                AudioRepository.update_state_audio(audio.ID,updated_state)
                ItemRepository.update_state_item(audio.item.ID, updated_state)               
                audio_data = audio.to_dict()
            
                audio_data["item"] = audio.item.to_dict() if audio.item else None
                updated_audios.append(audio_data)

            db.session.commit()

            if updated_state == 'inactive':
                user = UserRepository.get_user_by_id_with_details(creator.user_ID)

                if user is not None:
                    user_data = user.to_dict()
                    user_data["user_detail"] = user.user_detail.to_dict() if user.user_detail else None

                    deactivation_email, status = MailService.send_deactivation_email(user_data)

            return {
                "message":f"El creador {creator_id} y sus audios ahora están '{updated_state}'",
                "updated_creator": updated_creator.to_dict() if updated_creator else None,
                "audios": updated_audios if updated_audios else None,
            }, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
    
    @staticmethod
    def confirm_user_email(user_id):
        try: 
            user = UserRepository.get_user_by_id_with_details(user_id)
            if user is None:
                return {"message": f"Usuario con id {user_id} no encontrado"}, 404

            if user.state != 'created':
                return {"message": f"El estado del usuario debe ser 'created'"}, 400
            
            updated_user = UserRepository.update_state_user(user_id, 'verified')

            db.session.commit()

            return {
                "message":"Email ha sido verificado con éxito.",
                "user": updated_user.to_dict() if updated_user else None,
            }, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
