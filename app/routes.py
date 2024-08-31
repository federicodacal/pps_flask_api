from flask import request, redirect, url_for, flash
from app import app, db 
from app.models import User

@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/users')
def get_users():
    return 'Users'

@app.route('/user', methods=['POST'])
def add_user():
    name = 'Pepe'
    new_user = User(name)
    db.session.add(new_user)
    db.session.commit
    flash('Agregado!')