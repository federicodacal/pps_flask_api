import datetime
from ..databases.db import db
from ..models.item import Item

class ItemRepository:

    @staticmethod
    def get_all_items():
        return Item.query.all()
    
    @staticmethod
    def get_item_by_id(item_id):
        return Item.query.get(item_id)
    
    @staticmethod
    def create_item(data, audio_id):
        new_audio = Item(
            ID=data['item_ID'],
            creator_ID=data['creator_ID'],
            audio_ID=audio_id,
            price=data['price'],
            state=data['state_item'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(new_audio)
        return new_audio