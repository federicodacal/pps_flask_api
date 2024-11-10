import datetime
from ..databases.db import db
from ..models.account import Account

class AccountRepository:

    @staticmethod
    def get_account_by_creator_id(creator_id):
        return Account.query.filter_by(creator_ID=creator_id).first()

    @staticmethod
    def create_account(data):
        new_account = Account(
            ID=data['account_ID'],
            creator_ID=data['creator_ID'],
            personal_account_ID=data['personal_account_ID'],
            type=data['account_type'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc),
        )
        db.session.add(new_account)
        return new_account
    
    @staticmethod
    def update_account(creator_id, data):
        account = AccountRepository.get_account_by_creator_id(creator_id)

        if not account:
            return None 
        
        account.personal_account_ID = data.get('personal_account_ID', account.personal_account_ID)
        account.type = data.get('account_type', account.type)
        account.modified_at = datetime.datetime.now(datetime.timezone.utc)

        return account
    
