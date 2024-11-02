import datetime
from flask import Blueprint, request, jsonify
from ..db import db  
from ..models.user_detail import User_detail 

user_routes = Blueprint('user_routes', __name__)

# GET ALL
@user_routes.route('/users')
def get_users():
    users = User_detail.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# GET BY ID
@user_routes.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = User_detail.query.get(user_id) 
    if user is None:
        return {"error": "Usuario no encontrado"}, 404
    return jsonify(user.to_dict()), 200

# CREATE
@user_routes.route('/users', methods=['POST'])
def create_user():

    data = request.json or {}

    if not data:
        return {"error": "Ocurrió un problema"}, 400

    new_user = User_detail(
        ID=data['ID'],
        personal_ID=data['personal_ID'],
        profile=data['profile'],
        username=data['username'],
        email=data['email'],
        full_name=data['full_name'],
        state=data['state'],
        phone_number=data['phone_number'],
        subscription_id=data['subscription_id'], # Puede ser opcional
        account_ID=data.get('account_ID'),  # Puede ser opcional
        credits=data.get('credits'),  # Puede ser opcional
        created_at=datetime.datetime.now(datetime.timezone.utc),
        modified_at=datetime.datetime.now(datetime.timezone.utc),
        points=data.get('points'),  # Puede ser opcional
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# UPDATE
@user_routes.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User_detail.query.get(user_id)
    if user is None:
        return {"error": "Usuario no encontrado"}, 404

    data = request.json or {}

    user.personal_ID = data.get('personal_ID', user.personal_ID)
    user.profile = data.get('profile', user.profile)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.full_name = data.get('full_name', user.full_name)
    user.state = data.get('state', user.state)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.account_ID = data.get('account_ID', user.account_ID)
    user.subscription_id = data.get('subscription_id', user.subscription_id)
    user.credits = data.get('credits', user.credits)
    user.points = data.get('points', user.points)
    user.modified_at = datetime.datetime.now(datetime.timezone.utc)  # Actualizar la fecha de modificación

    db.session.commit()
    return jsonify(user.to_dict()), 200

# DELETE
@user_routes.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User_detail.query.get(user_id)
    if user is None:
        return {"error": "Usuario no encontrado"}, 404

    db.session.delete(user)
    db.session.commit()
    return {"message": "Usuario eliminado"}, 204