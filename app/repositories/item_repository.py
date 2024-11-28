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
            creator_ID=data['creator_ID'],
            audio_ID=audio_id,
            price=data['price'],
            created_at=datetime.datetime.now(datetime.timezone.utc),
            modified_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.session.add(new_audio)
        return new_audio
    
    @staticmethod
    def update_item(ID, data):
        item = Item.query.get(ID)

        if not item:
            return None
        
        item.price = data.get('price', item.price)
        item.state = data.get('state_item', item.state)
        item.modified_at = datetime.datetime.now(datetime.timezone.utc)
        
        return item
    
    @staticmethod
    def delete_item(item_id):
        item = Item.query.get(item_id)
        if item:
            db.session.delete(item)

    @staticmethod
    def update_state_item(ID, state):
        item = Item.query.get(ID)

        if not item: 
            return None
        
        item.state = state
        item.modified_at = datetime.datetime.now(datetime.timezone.utc) 

        return item