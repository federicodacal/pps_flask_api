import datetime
from ..models.purchase import Purchase
from ..models.purchase_detail import Purchase_detail
from ..models.item import Item
from ..databases.db import db
from sqlalchemy.orm import joinedload

class PurchaseRepository:

    @staticmethod
    def get_all_purchases():
        return Purchase.query.options(joinedload(Purchase.purchase_details).joinedload(Purchase_detail.item)).all() # type: ignore 
    
    @staticmethod
    def get_purchases_with_details_and_audios_by_user_id(user_id):
        return Purchase.query.options(joinedload(Purchase.purchase_details).joinedload(Purchase_detail.item).joinedload(Item.audio)).filter_by(buyer_ID=user_id) # type: ignore
    
    @staticmethod
    def create_purchase(purchase_id, buyer_id, flow_type, payment_method):
        new_purchase = Purchase(
            ID=purchase_id, 
            buyer_ID=buyer_id,
            flow_type=flow_type,
            payment_method=payment_method,
            state="created",
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now()
        )
        db.session.add(new_purchase)
        return new_purchase