import datetime
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