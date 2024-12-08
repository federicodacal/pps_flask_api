from flask import jsonify, request
from ..services.subscription_service import SubscriptionService

class SubscriptionController:

    @staticmethod
    def get_subscriptions():
        response, status_code = SubscriptionService.get_all_subscriptions()
        return jsonify(response), status_code
    
    @staticmethod
    def get_subscription(subscription_id):
        response, status_code = SubscriptionService.get_subscription_by_id(subscription_id)
        return jsonify(response), status_code
    
    @staticmethod
    def create_subscription():
        data = request.json or {}
        response, status_code = SubscriptionService.create_subscription(data)
        return jsonify(response), status_code

    @staticmethod
    def update_subscription(subscription_id):
        data = request.json or {}
        response, status_code = SubscriptionService.update_subscription(subscription_id, data)
        return jsonify(response), status_code
    
    @staticmethod
    def activate_subscription(subscription_id):
        response, status_code = SubscriptionService.update_subscription_state(subscription_id, 'active')
        return jsonify(response), status_code
    
    @staticmethod
    def inactivate_subscription(subscription_id):
        response, status_code = SubscriptionService.update_subscription_state(subscription_id, 'inactive')
        return jsonify(response), status_code
    
    @staticmethod
    def evaluate_subscription_status_by_creator(creator_id):
        response, status_code = SubscriptionService.evaluate_subscription_status_by_creator_id(creator_id)
        return jsonify(response), status_code