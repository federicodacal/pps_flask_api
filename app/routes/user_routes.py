import datetime
from flask import Blueprint, request, jsonify
from ..db import db  
from ..models.user_detail import User_detail 
from ..models.user import User 
from ..models.creator import Creator 

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

    try:
        # Insertar en users_details
        new_user_detail = User_detail(
            ID=data['user_detail_ID'],
            personal_ID=data['personal_ID'],
            username=data['username'],
            full_name=data['full_name'],
            phone_number=data['phone_number'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc),
        )
        db.session.add(new_user_detail)
        db.session.commit()

        # Insertar en users
        new_user = User(
            ID=data['user_ID'],
            user_detail_ID=data['user_detail_ID'],  # Relacionado con user_detail
            email=data['email'],
            pwd=data['pwd'],
            type=data['type'],
            state=data['state'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc),
        )
        db.session.add(new_user)
        db.session.commit()

        if data['type'] == 'creador':
            # Insertar en creator
            new_creator = Creator(
                ID=data['creator_ID'],
                user_ID=data['user_ID'],  # Relacionado con user
                subscription_ID=data['subscription_ID'],
                profile=data['profile'],
                points=data['points'],
                credits=data['credits'],
                account_ID=['account_ID'],
                state=data['state'],
                created_at=datetime.datetime.now(datetime.timezone.utc),
                modified_at=datetime.datetime.now(datetime.timezone.utc),
            )
            db.session.add(new_creator)
            db.session.commit()

        return jsonify({
            "user_detail": new_user_detail.to_dict(),
            "user": new_user.to_dict(),
            "creator": new_creator.to_dict(),
        }), 201

    except Exception as e:
        db.session.rollback()
        return {"error": f"Ocurrió un error al crear el usuario: {str(e)}"}, 500

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