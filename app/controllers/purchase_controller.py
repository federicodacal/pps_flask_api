from flask import jsonify, request
from ..services.purchase_service import PurchaseService

class PurchaseController:

    @staticmethod
    def get_purchases():
        try:
            purchases = PurchaseService.get_all_purchases()
            return jsonify(purchases), 200
        except ValueError as ve:
            return {"error": str(ve)}, 404
        except Exception as e:
            return {"error": str(e)}, 500
    
    @staticmethod
    def create_purchase():
        data = request.json or {}
        
        try:
            purchase_data = PurchaseService.create_purchase(data)
            return jsonify(purchase_data), 201
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            return {"error": str(re)}, 500
    
    @staticmethod
    def get_purchases_by_user(user_id):
        try:
            purchases = PurchaseService.get_purchases_by_user_id(user_id)
            return jsonify(purchases), 200
        except ValueError as ve:
            return {"error": str(ve)}, 404
        except Exception as e:
            return {"error": str(e)}, 500