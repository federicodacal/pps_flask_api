from flask import request, redirect, url_for, flash, jsonify
from app import app, db 
from app.models import User

@app.route('/')
def index():
    return 'Hello Flask Python'

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name} for user in users]
    return jsonify(users_list)

@app.route('/user', methods=['GET', 'POST'])
def add_user():
    name = 'Pepe'
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    flash('Agregado!', 'success')
    return 'Add a user by sending a POST request.'