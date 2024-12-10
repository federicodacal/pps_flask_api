import datetime
from sqlalchemy import text

from ..models.user_detail import User_detail
from ..databases.db import db
from ..models.user import User
from ..models.creator import Creator
from sqlalchemy.orm import joinedload

class UserRepository:

    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_all_users_with_details_and_creators():
        return User.query.options(joinedload(User.user_detail),joinedload(User.creator)).all() # type: ignore

    @staticmethod
    def get_user_by_id_with_details(user_id):
        return User.query.options(joinedload(User.user_detail),joinedload(User.creator).joinedload(Creator.account)).filter_by(ID=user_id).first() # type: ignore
    
    @staticmethod
    def get_user_by_email_with_details(email):
        return User.query.options(joinedload(User.user_detail),joinedload(User.creator)).filter_by(email=email).first() #type: ignore
    
    @staticmethod
    def get_user_by_username_with_details(username):
        return User.query.join(User_detail, User.user_detail_ID == User_detail.ID).options(joinedload(User.user_detail)).filter(User_detail.username == username).first() #type: ignore

    @staticmethod
    def create_user(data):
        new_user = User(
            user_detail_ID=data['user_detail_ID'],
            email=data['email'],
            pwd=data['pwd'],
            type=data['type'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc),
        )
        db.session.add(new_user)
        return new_user
    
    @staticmethod
    def update_user(ID, data):
        user = User.query.get(ID)

        if not user:
            return None

        user.type = data.get('type', user.type)
        user.state = data.get('state', user.state)
        user.modified_at = datetime.datetime.now(datetime.timezone.utc)
        
        return user
    
    @staticmethod
    def update_state_user(ID, state):
        user = User.query.get(ID)

        if not user: 
            return None
        
        user.state = state
        user.modified_at = datetime.datetime.now(datetime.timezone.utc) 

        return user
    
    @staticmethod 
    def update_password(ID, pwd):
        user = User.query.get(ID)

        if not user:
            return None 
        
        user.pwd = pwd 
        user.modified_at = datetime.datetime.now(datetime.timezone.utc) 

        return user
