from flask import Blueprint
from ..controllers.subscription_controller import SubscriptionController

subscription_routes = Blueprint('subscription_routes', __name__)

subscription_routes.route('/subscriptions', methods=['GET'])(SubscriptionController.get_subscriptions)
subscription_routes.route('/subscriptions/<string:subscription_id>', methods=['GET'])(SubscriptionController.get_subscription)
subscription_routes.route('/subscriptions/creator/<string:creator_id>', methods=['GET'])(SubscriptionController.evaluate_subscription_status_by_creator)
subscription_routes.route('/subscriptions', methods=['POST'])(SubscriptionController.create_subscription)
subscription_routes.route('/subscriptions/<string:subscription_id>', methods=['PUT'])(SubscriptionController.update_subscription)
subscription_routes.route('/subscriptions/active/<string:subscription_id>', methods=['PUT'])(SubscriptionController.activate_subscription)
subscription_routes.route('/subscriptions/inactive/<string:subscription_id>', methods=['PUT'])(SubscriptionController.inactivate_subscription)