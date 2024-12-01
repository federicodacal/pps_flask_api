from flask import jsonify, request
from ..services.purchase_service import PurchaseService

class PurchaseController:

    @staticmethod
    def get_purchases():
        response, status_code = PurchaseService.get_all_purchases()
        return jsonify(response), status_code
    
    @staticmethod
    def get_purchase_by_id(purchase_id):
        response, status_code = PurchaseService.get_purchase_by_id(purchase_id)
        return jsonify(response), status_code
    
    @staticmethod
    def create_purchase():
        data = request.json or {}
        response, status_code = PurchaseService.create_purchase(data)
        return jsonify(response), status_code
    
    @staticmethod
    def get_purchases_by_user(user_id):
        response, status_code = PurchaseService.get_purchases_by_user_id(user_id)
        return jsonify(response), status_code