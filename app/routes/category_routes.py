from flask import Blueprint
from ..controllers.category_controller import CategoryController

category_routes = Blueprint('category_routes', __name__)

category_routes.route('/categories', methods=['GET'])(CategoryController.get_categories)
category_routes.route('/categories/<string:category_id>', methods=['GET'])(CategoryController.get_category)
category_routes.route('/categories', methods=['POST'])(CategoryController.create_category)
category_routes.route('/categories/<string:category_id>', methods=['PUT'])(CategoryController.update_category)
category_routes.route('/categories/<string:category_id>', methods=['DELETE'])(CategoryController.delete_category)