from flask import Blueprint
from ..controllers.user_controller import UserController

user_routes = Blueprint('user_routes', __name__)

user_routes.route('/users', methods=['GET'])(UserController.get_users)
user_routes.route('/users/<string:user_id>', methods=['GET'])(UserController.get_user)
user_routes.route('/users', methods=['POST'])(UserController.create_user)
user_routes.route('/users/<string:user_id>', methods=['PUT'])(UserController.update_user)
