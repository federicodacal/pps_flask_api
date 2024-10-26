from flask import Blueprint

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users')
def get_users():
    return "Lista de usuarios"