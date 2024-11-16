from ..repositories.audio_repository import AudioRepository
from ..services.audio_service import AudioService
from ..services.config_service import ConfigService
from ..databases.db import db
from ..repositories.purchase_repository import PurchaseRepository
from ..repositories.purchase_detail_repository import PurchaseDetailRepository
from ..repositories.item_repository import ItemRepository

class PurchaseService:

    @staticmethod
    def get_all_purchases():
        purchases = PurchaseRepository.get_all_purchases()
    
        result = []
        for purchase in purchases:
            purchase_data = purchase.to_dict() 
            total = sum(detail.item.price for detail in purchase.purchase_details)  
            purchase_data["total"] = total

            for detail in purchase.purchase_details:
                detail_data = detail.to_dict()
                detail_data["item"] = detail.item.to_dict() 
                purchase_data["purchase_details"] = purchase_data.get("purchase_details", []) + [detail_data]
            
            result.append(purchase_data)
        
        return result
    
    @staticmethod
    def create_purchase(data):
        if not data:
            raise ValueError("Los datos proporcionados están vacíos")
        
        purchase_id = data.get("purchase_ID")
        buyer_id = data.get("buyer_ID")
        flow_type = data.get("flow_type")
        payment_method = data.get("payment_method")
        items = data.get("items", [])

        if not buyer_id or not flow_type or not payment_method or not items:
            raise ValueError("Faltan datos")
        
        try: 
            with db.session.begin():

                purchase = PurchaseRepository.create_purchase(purchase_id, buyer_id, flow_type, payment_method)

                for item_data in items:
                    audio_id = item_data.get("audio_ID")
                    creator_id = item_data.get("creator_ID")
                    item_id = item_data.get("item_ID")
                    price = item_data.get("price")

                    if not audio_id or not creator_id or not item_id or not price:
                        raise ValueError("Cada ítem incluir audio_ID, creator_ID y price")
                    
                    audio = AudioRepository.get_audio_by_id_with_item(audio_id)
                    if not audio:
                        raise ValueError(f"El audio con ID {audio_id} no existe")
                
                    if audio.creator_ID != creator_id:
                        raise ValueError(f"El audio con ID {audio_id} no pertenece al creador con ID {creator_id}")
                    
                    if audio_id != item_data["audio_ID"]:
                        raise ValueError(f"El audio con ID {audio_id} no corresponde al item con ID {item_id}")

                    PurchaseDetailRepository.create_purchase_detail(purchase.ID, item_id)

            db.session.commit()

            return {"purchase_id": purchase.ID}
        
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Ocurrió un error al crear la compra: {str(e)}: {e.args}")
    
    @staticmethod
    def get_purchases_by_user_id(user_id):
        purchases = PurchaseRepository.get_purchases_with_details_and_audios_by_user_id(user_id)

        if not purchases:
            raise ValueError(f"No se encontraron compras para el usuario: {user_id}")
        
        result = []
        for purchase in purchases: 
            purchase_data = purchase.to_dict()

            total = 0

            purchase_data["purchase_details"] = []
            for detail in purchase.purchase_details:
                detail_data = detail.to_dict()
                item_data = detail.item.to_dict()
                
                if detail.item.audio:
                    audio_data = detail.item.audio.to_dict()
                    audio_file = AudioService.get_audio_file_from_gridfs(detail.item.audio.file_name)
                    audio_data["file_url"] = (
                        f"{ConfigService.current_url}/audios/file/{detail.item.audio.file_name}"
                        if audio_file
                        else None
                    )
                    item_data["audio"] = audio_data
                else:
                    item_data["audio"] = None

                total += detail.item.price
                
                detail_data["item"] = item_data
                purchase_data["purchase_details"].append(detail_data)

            purchase_data["total"] = total

            result.append(purchase_data)
        
        return result