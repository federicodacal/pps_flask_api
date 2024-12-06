import datetime

from ..databases.db import db
from ..models.subscription_billing import Subscription_billing

class SubscriptionBillingRepository:

    @staticmethod
    def get_all_subscriptions_billings():
        return Subscription_billing.query.all()
    
    @staticmethod
    def get_subscription_billing_by_id(subscription_billing_id):
        return Subscription_billing.query.filter_by(ID=subscription_billing_id).first() # type: ignore
    
    @staticmethod
    def create_subscription_billing(data):
        new_subscription = Subscription_billing(
            account_ID=data['account_ID'],
            subscription_ID=data['subscription_ID'],
            last_payment_date=data['last_payment_date'],
            next_payment_date=data['next_payment_date'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc),
        )
        db.session.add(new_subscription)
        return new_subscription
    
    @staticmethod
    def update_subscription_billing(ID, data):
        subscription = Subscription_billing.query.get(ID)

        if not subscription:
            return None

        subscription.account_ID = data.get('account_ID', subscription.account_ID)
        subscription.subscription_ID = data.get('subscription_ID', subscription.subscription_ID)
        subscription.state = data.get('state', subscription.state)
        subscription.last_payment_date = data.get('last_payment_date', subscription.last_payment_date)
        subscription.next_payment_date = data.get('next_payment_date', subscription.next_payment_date)
        subscription.modified_at = datetime.datetime.now(datetime.timezone.utc)
        
        return subscription