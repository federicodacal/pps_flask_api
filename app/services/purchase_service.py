from ..databases.db import db

class PurchaseService:

    @staticmethod
    def get_all_purchases():
        return 'Get: purchases'
    
    @staticmethod
    def create_purchase():
        return 'Post: purchase'
    
    @staticmethod
    def get_purchases_by_user_id(user_id):
        return 'Get: purchases by user'