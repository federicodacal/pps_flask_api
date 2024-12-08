import datetime

from ..services.user_service import UserService
from ..services.mail_service import MailService
from ..models.subscription_billing import Subscription_billing
from ..repositories.creator_repository import CreatorRepository
from ..databases.db import db
from ..repositories.subscription_repository import SubscriptionRepository


class SubscriptionService:

    @staticmethod
    def get_all_subscriptions():
        subscriptions = SubscriptionRepository.get_all_subscriptions()
        subscriptions_dict = [sub.to_dict() for sub in subscriptions]
        return subscriptions_dict, 200

    @staticmethod
    def get_subscription_by_id(subscription_id):
        sub = SubscriptionRepository.get_subscription_by_id(subscription_id)
        return sub, 200
    
    @staticmethod
    def create_subscription(data):
        try:
            if not data:
                return {"message": "Los datos proporcionados están vacíos"}, 400
            
            required_fields = ['renewal_time_in_days', 'revenue_percentage', 'monthly_price', 'type']
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return {"message": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}, 400
                        
            new_sub = SubscriptionRepository.create_subscription(data)

            db.session.commit()
            
            return { "new_sub": new_sub.to_dict() }, 200
        
        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
        
    @staticmethod
    def update_subscription(subscription_id, data):
        return 'Update subscription', 200
    
    @staticmethod
    def update_subscription_state(subscription_id, updated_state):
        return f'Update subscription state {updated_state}', 200
    
    @staticmethod 
    def evaluate_subscription_status_by_creator_id(creator_id):
        try: 
            creator = CreatorRepository.get_creator_by_id(creator_id)

            if not creator:
                return {"message": f"Creador con id {creator_id} no encontrado"}, 404
            
            account = creator.account
            if not account:
                return {"message": f"Cuenta de creador {creator_id} no encontrada"}, 404
            
            subscription_billing = Subscription_billing.query.filter_by(account_ID=account.ID).first()
            if not subscription_billing:
                return {"message": f"Cobro de subscrición para la cuenta con id {account.ID} no encontrada."}, 404

            today = datetime.datetime.now()
            next_payment_date = subscription_billing.next_payment_date

            if next_payment_date < today:
                days_overdue = (today - next_payment_date).days

                if(days_overdue > 30):
                    UserService.update_creator_state(creator.ID, 'debtor')
                elif(days_overdue > 60):
                    UserService.update_creator_state(creator.ID, 'inactive')

        except Exception as e:
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500    