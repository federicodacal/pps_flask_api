from ..databases.db import db
from ..repositories.subscription_repository import SubscriptionRepository


class SubscriptionService:

    @staticmethod
    def get_all_subscriptions():
        subs = SubscriptionRepository.get_all_subscriptions()
        return subs, 200

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