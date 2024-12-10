from flask import jsonify, request

from ..services.user_service import UserService

class UserController:

    @staticmethod
    def get_users():
        response, status_code = UserService.get_all_users()
        return jsonify(response), status_code
    
    @staticmethod
    def get_user(user_id):
        response, status_code = UserService.get_user_by_id(user_id)
        return jsonify(response), status_code
    
    @staticmethod
    def get_user_by_email(user_email):
        response, status_code = UserService.get_user_by_email(user_email)
        return jsonify(response), status_code

    @staticmethod
    def get_user_by_username(user_username):
        response, status_code = UserService.get_user_by_username(user_username)
        return jsonify(response), status_code
    
    @staticmethod
    def create_user():
        data = request.json or {}
        response, status_code = UserService.create_user(data)
        return jsonify(response), status_code

    @staticmethod
    def update_user(user_id):
        data = request.json or {}
        response, status_code = UserService.update_user(user_id, data)
        return jsonify(response), status_code
    
    @staticmethod
    def approve_user(user_id):
        response, status_code = UserService.update_user_state(user_id, 'active')
        return jsonify(response), status_code
    
    @staticmethod
    def deactivate_user(user_id):
        response, status_code = UserService.update_user_state(user_id, 'inactive')
        return jsonify(response), status_code
    
    @staticmethod
    def deactivate_creator(creator_id):
        response, status_code = UserService.update_creator_state(creator_id, 'inactive')
        return jsonify(response), status_code
    
    @staticmethod
    def activate_creator(creator_id):
        response, status_code = UserService.update_creator_state(creator_id, 'active')
        return jsonify(response), status_code
    
    @staticmethod
    def confirm_user_email(user_id):
        response, status_code = UserService.confirm_user_email(user_id)
        return jsonify(response), status_code
    
    @staticmethod
    def change_password(user_id):
        data = request.json or {}
        response, status_code = UserService.change_password(user_id, data)
        return jsonify(response), status_code
