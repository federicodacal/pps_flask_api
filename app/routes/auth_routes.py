from flask import Blueprint
from ..controllers.auth_controller import AuthController

auth_routes = Blueprint('auth_routes', __name__)

auth_routes.route('/login', methods=['GET'])(AuthController.login)
auth_routes.route('/logout', methods=['GET'])(AuthController.logout)