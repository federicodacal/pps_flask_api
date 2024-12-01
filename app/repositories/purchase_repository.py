import datetime
from ..models.purchase import Purchase
from ..models.audio import Audio
from ..models.creator import Creator
from ..models.user import User
from ..models.purchase_detail import Purchase_detail
from ..models.item import Item
from ..databases.db import db
from sqlalchemy.orm import joinedload

class PurchaseRepository:

    @staticmethod
    def get_all_purchases():
        return Purchase.query.options(joinedload(Purchase.purchase_details).joinedload(Purchase_detail.item)).all() # type: ignore 
    
    @staticmethod
    def get_purchase_by_id_with_details_and_audios(purchase_id):
        return Purchase.query.options(joinedload(Purchase.purchase_details).joinedload(Purchase_detail.item).joinedload(Item.audio).joinedload(Audio.creator).joinedload(Creator.user).joinedload(User.user_detail)).filter_by(ID=purchase_id).first() #type: ignore
    
    @staticmethod
    def get_purchases_with_details_and_audios_by_user_id(user_id):
        return Purchase.query.options(joinedload(Purchase.purchase_details).joinedload(Purchase_detail.item).joinedload(Item.audio).joinedload(Audio.creator).joinedload(Creator.user).joinedload(User.user_detail)).filter_by(buyer_ID=user_id).all() # type: ignore
    
    @staticmethod
    def create_purchase(buyer_id, flow_type, payment_method):
        new_purchase = Purchase(
            buyer_ID=buyer_id,
            flow_type=flow_type,
            payment_method=payment_method,
            state="created",
            created_at=datetime.datetime.now(),
            modified_at=datetime.datetime.now()
        )
        db.session.add(new_purchase)
        return new_purchase