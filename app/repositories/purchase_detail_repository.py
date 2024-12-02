import datetime

from ..models.item import Item
from ..models.purchase import Purchase
from ..databases.db import db
from ..models.purchase_detail import Purchase_detail
from sqlalchemy.orm import joinedload

class PurchaseDetailRepository:
    
    @staticmethod
    def create_purchase_detail(purchase_id, item_id):
        new_detail = Purchase_detail(
            purchase_ID=purchase_id,
            item_ID=item_id,
            state="created",
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now()
        )
        db.session.add(new_detail)
        return new_detail
    
    @staticmethod
    def has_bought_audio(buyer_id, audio_id):
        return db.session.query(Purchase_detail).join(Purchase).join(Item).filter(Purchase.buyer_ID == buyer_id, Item.audio_ID == audio_id).first() is not None #type: ignore