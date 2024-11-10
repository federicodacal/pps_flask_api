import datetime
from ..databases.db import db
from ..models.creator import Creator
from sqlalchemy.orm import joinedload

class CreatorRepository:

    @staticmethod
    def get_creator_by_user_id(user_id):
        return Creator.query.filter_by(user_ID=user_id).first()
    
    @staticmethod 
    def get_creator_with_account(creator_id):
        return Creator.query.options(joinedload(Creator.account)).filter_by(ID=creator_id).first() # type: ignore

    @staticmethod
    def create_creator(data):
        new_creator = Creator(
            ID=data['creator_ID'],
            user_ID=data['ID'],
            subscription_ID=data['subscription_ID'],
            profile=data['profile'],
            points=data['points'],
            credits=data['credits'],
            state=data['state'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc),
        )
        db.session.add(new_creator)
        return new_creator
    
    @staticmethod
    def update_creator(creator_ID, data):
        creator = Creator.query.get(creator_ID)

        if not creator:
            return None 
        
        creator.subscription_ID = data.get('subscription_ID', creator.subscription_ID)
        creator.profile = data.get('profile', creator.profile)
        creator.points = data.get('points', creator.points)
        creator.credits = data.get('credits', creator.credits)
        creator.state = data.get('state', creator.state)
        creator.modified_at = datetime.datetime.now(datetime.timezone.utc)

        return creator
    
