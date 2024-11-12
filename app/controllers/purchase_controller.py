from flask import jsonify, request
from ..services.purchase_service import PurchaseService

class PurchaseController:

    @staticmethod
    def get_purchases():
        purchases = PurchaseService.get_all_purchases()
        return jsonify(purchases), 200
    
    @staticmethod
    def create_purchase():
        purchase = PurchaseService.create_purchase()
        return jsonify(purchase), 200
    
    @staticmethod
    def get_purchases_by_user(user_id):
        purchases = PurchaseService.get_purchases_by_user_id(user_id)
        return jsonify(purchases), 200