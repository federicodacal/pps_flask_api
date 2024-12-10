import datetime

from flask import jsonify

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

        if not sub:
            return {"message": "Subscripcion no encontrada"}, 404
        
        sub_dict = sub.to_dict()
        return sub_dict, 200
    
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
        subscription = SubscriptionRepository.get_subscription_by_id(subscription_id)
        if not subscription:
            return {"error": "Suscripcion no encontrada"}, 404

        allowed_fields = ["renewal_time_in_days", "revenue_percentage", "monthly_price", "type"]
        for field in allowed_fields:
            if field in data:
                setattr(subscription, field, data[field])

        db.session.commit()

        return {"subscription": subscription.to_dict() if subscription else None}, 200
    
    @staticmethod
    def update_subscription_state(subscription_id, updated_state):
        subscription = SubscriptionRepository.get_subscription_by_id(subscription_id)
        if not subscription:
            return {"error": "Suscripcion no encontrada"}, 404
        
        updated_subscription = SubscriptionRepository.update_state_subscription(subscription_id, updated_state)

        db.session.commit()

        return {"sub": updated_subscription.to_dict() if updated_subscription else None }, 200
    
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

            print("Next payment:")
            print(next_payment_date)

            print("Today:")
            print(today)

            if next_payment_date < today:
                days_overdue = (today - next_payment_date).days

                print("Next payment:")
                print(next_payment_date)

                print("Days overdue:")
                print(days_overdue)

                if(days_overdue > 30 and days_overdue <= 59):
                    UserService.update_creator_state(creator.ID, 'debtor', days_overdue=days_overdue)
                elif(days_overdue > 60):
                    UserService.update_creator_state(creator.ID, 'inactive')

                return {
                    "creator_id": creator.ID,
                    "account_id": account.ID,
                    "subscription_billing_id": subscription_billing.ID,
                    "next_payment_date": next_payment_date,
                    "days_overdue": days_overdue,
                    "message": f"Creador tiene deuda pendiente: {days_overdue} días"
                }, 200
            else:
                return {
                    "creator_id": creator.ID,
                    "account_id": account.ID,
                    "subscription_billing_id": subscription_billing.ID,
                    "next_payment_date": next_payment_date,
                    "days_overdue": 0,
                    "message": "Creador no tiene deuda pendiente"
                }, 200

        except Exception as e:
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500    