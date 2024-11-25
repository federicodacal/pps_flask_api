import datetime
from sqlalchemy import text
from ..databases.db import db
from ..models.user import User
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
        return User.query.options(joinedload(User.user_detail)).filter_by(ID=user_id).first() # type: ignore
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(data):
        new_user = User(
            ID=data['ID'],
            user_detail_ID=data['user_detail_ID'],
            email=data['email'],
            pwd=data['pwd'],
            type=data['type'],
            state=data['state'],
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

        user.pwd = data.get('pwd', user.pwd)
        user.type = data.get('type', user.type)
        user.state = data.get('state', user.state)
        user.modified_at = datetime.datetime.now(datetime.timezone.utc)
        
        return user