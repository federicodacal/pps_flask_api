import datetime

from ..databases.db import db
from ..models.subscription import Subscription

class SubscriptionRepository:

    @staticmethod
    def get_all_subscriptions():
        return Subscription.query.all()
    
    @staticmethod
    def get_subscription_by_id(subscription_id):
        return Subscription.query.filter_by(ID=subscription_id).first() # type: ignore
    
    @staticmethod
    def create_subscription(data):
        new_subscription = Subscription(
            type=data['type'],
            renewal_time_in_days=data['renewal_time_in_days'],
            revenue_percentage=data['revenue_percentage'],
            monthly_price=data['monthly_price'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc),
        )
        db.session.add(new_subscription)
        return new_subscription
    
    @staticmethod
    def update_subscription(ID, data):
        subscription = Subscription.query.get(ID)

        if not subscription:
            return None

        subscription.type = data.get('type', subscription.type)
        subscription.renewal_time_in_days = data.get('renewal_time_in_days', subscription.renewal_time_in_days)
        subscription.revenue_percentage = data.get('revenue_percentage', subscription.revenue_percentage)
        subscription.monthly_price = data.get('monthly_price', subscription.monthly_price)
        subscription.modified_at = datetime.datetime.now(datetime.timezone.utc)
        
        return subscription
    
    @staticmethod
    def update_state_subscription(ID, state):
        subscription = Subscription.query.get(ID)

        if not subscription: 
            return None
        
        subscription.state = state
        subscription.modified_at = datetime.datetime.now(datetime.timezone.utc) 

        return subscription