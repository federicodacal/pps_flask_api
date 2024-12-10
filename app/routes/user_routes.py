from flask import Blueprint
from ..controllers.user_controller import UserController

user_routes = Blueprint('user_routes', __name__)

user_routes.route('/users', methods=['GET'])(UserController.get_users)
user_routes.route('/users/<string:user_id>', methods=['GET'])(UserController.get_user)
user_routes.route('/users/email/<string:user_email>', methods=['GET'])(UserController.get_user_by_email)
user_routes.route('/users/username/<string:user_username>', methods=['GET'])(UserController.get_user_by_username)
user_routes.route('/users', methods=['POST'])(UserController.create_user)
user_routes.route('/users/<string:user_id>', methods=['PUT'])(UserController.update_user)
user_routes.route('/users/confirm-email/<string:user_id>', methods=['GET'])(UserController.confirm_user_email)
user_routes.route('/users/approval/<string:user_id>', methods=['POST'])(UserController.approve_user)
user_routes.route('/users/approval/<string:user_id>', methods=['DELETE'])(UserController.deactivate_user)
user_routes.route('/users/creator/<string:creator_id>', methods=['DELETE'])(UserController.deactivate_creator)
user_routes.route('/users/creator/<string:creator_id>', methods=['POST'])(UserController.activate_creator)
user_routes.route('/users/change-password/<string:user_id>', methods=['PUT'])(UserController.change_password)
