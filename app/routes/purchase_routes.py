from flask import Blueprint
from ..controllers.purchase_controller import PurchaseController

purchase_routes = Blueprint('purchase_routes', __name__)

purchase_routes.route('/purchases', methods=["GET"])(PurchaseController.get_purchases)
purchase_routes.route('/purchases', methods=["POST"])(PurchaseController.create_purchase)
purchase_routes.route('/purchases/<string:purchase_id>', methods=["GET"])(PurchaseController.get_purchase_by_id)
purchase_routes.route('/purchases/buyer/<string:user_id>', methods=["GET"])(PurchaseController.get_purchases_by_user)
