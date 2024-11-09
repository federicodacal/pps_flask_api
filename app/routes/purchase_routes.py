import datetime
from flask import Blueprint, request, jsonify
from ..databases.db import db  
from ..models.purchase import Purchase 
from ..models.purchase_detail import Purchase_detail 
from ..models.item import Item 

purchase_routes = Blueprint('purchase_routes', __name__)

# GET ALL
@purchase_routes.route('/purchases')
def get_purchases():
    purchases = Purchase.query.all()
    return jsonify([purchase.to_dict() for purchase in purchases]), 200

# GET BY ID
@purchase_routes.route('/purchases/<string:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id) 
    if purchase is None:
        return {"error": "Venta no encontrada"}, 404
    return jsonify(purchase.to_dict()), 200

# GET BY BUYER ID
@purchase_routes.route('/purchases/buyer/<string:buyer_id>', methods=['GET'])
def get_purchases_by_buyer(buyer_id):
    purchases = Purchase.query.filter_by(buyer_ID=buyer_id).all()
    if purchases:
        return jsonify([purchase.to_dict() for purchase in purchases]), 200
    else:
        return {"error": "No se encontraron ventas para este usuario"}, 404

# CREATE
@purchase_routes.route('/purchases', methods=['POST'])
def create_purchase():
    return 'Create Purchase'

# UPDATE
@purchase_routes.route('/purchases/<string:purchase_id>', methods=['PUT'])
def update_purchase(purchase_id):
    return 'Update Purchase'

# DELETE
@purchase_routes.route('/purchases/<string:purchase_id>', methods=['DELETE'])
def delete_purchase(purchase_id):
    return 'Delete Purchase'