from flask import jsonify
from pps_flask_api.app import app, db
from pps_flask_api.app.models.user import User

@app.route('/')
def index():
    return 'Hello Flask Python'

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name} for user in users]
    return jsonify(users_list)

@app.route('/crear', methods=['GET', 'POST'])
def add_user():
    name = 'Nuevo'
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return 'Add a user by sending a POST request.'