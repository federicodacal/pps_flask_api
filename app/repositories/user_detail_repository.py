import datetime
from ..databases.db import db
from ..models.user_detail import User_detail

class UserDetailRepository:

    @staticmethod
    def create_user_detail(data):
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
        return new_user_detail
    
    @staticmethod
    def update_user_detail(user_detail_id, data):
        user_detail = User_detail.query.get(user_detail_id)

        if not user_detail:
            return None 
        
        user_detail.personal_ID = data.get('personal_ID', user_detail.personal_ID)
        user_detail.username = data.get('username', user_detail.username)
        user_detail.full_name = data.get('full_name', user_detail.full_name)
        user_detail.phone_number = data.get('phone_number', user_detail.phone_number)
        user_detail.modified_at = datetime.datetime.now(datetime.timezone.utc)

        return user_detail