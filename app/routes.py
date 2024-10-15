from flask import jsonify
from app import app, db 
from app.models.user import User

@app.route('/')
def index():
    return 'Hello Flask Python'

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.ID, "name": user.username} for user in users]
    return jsonify(users_list)

@app.route('/user', methods=['GET', 'POST'])
def add_user():
    name = 'Pepe'
    new_user = User(username=name)
    db.session.add(new_user)
    db.session.commit()
    return 'Add a user by sending a POST request.'