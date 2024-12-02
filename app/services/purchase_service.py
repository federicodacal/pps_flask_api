from ..repositories.user_repository import UserRepository
from ..repositories.creator_repository import CreatorRepository
from ..services.mail_service import MailService
from ..repositories.audio_repository import AudioRepository
from ..services.audio_service import AudioService
from ..services.config_service import ConfigService
from ..databases.db import db
from ..repositories.purchase_repository import PurchaseRepository
from ..repositories.purchase_detail_repository import PurchaseDetailRepository
from ..repositories.item_repository import ItemRepository
from ..utils.validators import validate_purchase
from ..middlewares.api_exception import APIException

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
        
        return result, 200
    
    @staticmethod 
    def get_purchase_by_id(purchase_id):
        purchase = PurchaseRepository.get_purchase_by_id_with_details_and_audios(purchase_id)
    
        if not purchase:
            return {"message": f"Venta con id {purchase_id} no encontrada"}, 404
        
        purchase_data = purchase.to_dict()
        total = 0

        purchase_data["purchase_details"] = []

        # Recorrer los detalles de la compra
        for detail in purchase.purchase_details:
            detail_data = detail.to_dict()
            item_data = detail.item.to_dict()

            # Si el ítem tiene un audio
            if detail.item.audio:
                audio_data = detail.item.audio.to_dict()
                audio_file = AudioService.get_audio_file_from_gridfs(detail.item.audio.file_name)
                audio_data["file_url"] = (
                    f"{ConfigService.current_url}/audios/file/{detail.item.audio.file_name}"
                    if audio_file
                    else None
                )
                item_data["audio"] = audio_data
                item_data["audio"]["audio_name"] = detail.item.audio.audio_name

                # Agregar la información del creador del audio
                if detail.item.audio.creator and detail.item.audio.creator.user and detail.item.audio.creator.user.user_detail:
                    audio_data["creator"] = {
                        "username": detail.item.audio.creator.user.user_detail.username
                    }
                else:
                    audio_data["creator"] = None
            else:
                item_data["audio"] = None

            # Acumulando el total
            total += detail.item.price
            
            # Asociamos el item a los detalles
            detail_data["item"] = item_data
            purchase_data["purchase_details"].append(detail_data)

        purchase_data["total"] = total

        return purchase_data, 200
    
    @staticmethod
    def create_purchase(data):
        try: 
            if not data:
                return {"message": "Los datos proporcionados están vacíos"}, 400
            
            validation, msg = validate_purchase(data)
            if not validation:
                return {"message":msg}, 400
            
            buyer_id = data.get("buyer_ID")
            flow_type = data.get("flow_type")
            payment_method = data.get("payment_method")
            items = data.get("items", [])          

            with db.session.begin():

                purchase = PurchaseRepository.create_purchase(buyer_id, flow_type, payment_method)

                buyer = UserRepository.get_user_by_id_with_details(buyer_id)
                buyer_email = buyer.to_dict()["email"] if buyer else None

                purchase_details = []

                creators_data = {}

                for item_data in items:
                    audio_id = item_data.get("audio_ID")
                    creator_id = item_data.get("creator_ID")
                    item_id = item_data.get("item_ID")
                    price = item_data.get("price")

                    #if not audio_id or not creator_id or not item_id or not price:
                    #    raise ValueError("Cada ítem incluir item_ID, audio_ID, creator_ID y price")

                    if PurchaseDetailRepository.has_bought_audio(buyer_id, audio_id):
                        raise APIException(f"El comprador ya adquirió el audio con ID {audio_id}", status_code=400, error_type="Duplicate Purchase")
                    
                    audio = AudioRepository.get_audio_by_id_with_item(audio_id)
                    if not audio:
                        raise APIException(f"El audio con ID {audio_id} no existe", status_code=404, error_type="Value Error")
                
                    if audio.creator_ID != creator_id:
                        raise APIException(f"El audio con ID {audio_id} no pertenece al creador con ID {creator_id}", status_code=400, error_type="Integrity Error")
                    
                    if audio.item.ID != item_id:
                        raise APIException(f"El audio con ID {audio_id} no corresponde al item con ID {item_id}", status_code=400, error_type="Integrity Error")
                    
                    purchase_details.append({
                        "audio_name": audio.audio_name,
                        "price": price
                    })

                    if creator_id not in creators_data:
                        creator = CreatorRepository.get_creator_by_id(creator_id)
                        if not creator:
                            raise APIException(f"El creador con ID {creator_id} no existe", status_code=404, error_type="Value Error")
                        
                        if creator.user.ID == buyer_id:
                            raise APIException(f"No se permite que un creador compre sus propios audios", status_code=404, error_type="Value Error")
                        
                        creators_data[creator_id] = {
                            "email": creator.user.email if creator.user else None,
                            "audios": []
                        }

                        creators_data[creator_id]["audios"].append({
                            "name": audio.audio_name,
                            "price": price
                        })

                    PurchaseDetailRepository.create_purchase_detail(purchase.ID, item_id)
                    CreatorRepository.add_credits_to_creator(creator_id, price)

                    match audio.category:
                        case 'sample':
                            sample_points = 25
                            AudioRepository.add_points_to_audio(audio.ID, sample_points)
                            CreatorRepository.add_points_to_creator(creator_id, sample_points)
                        case 'acapella':
                            acapella_points = 30
                            AudioRepository.add_points_to_audio(audio.ID, acapella_points)
                            CreatorRepository.add_points_to_creator(creator_id, acapella_points)
                        case 'effect':
                            effect_points = 10
                            AudioRepository.add_points_to_audio(audio.ID, effect_points)
                            CreatorRepository.add_points_to_creator(creator_id, effect_points)
                        case _:
                            AudioRepository.add_points_to_audio(audio.ID, 5)
                            CreatorRepository.add_points_to_creator(creator_id, 5)   

                MailService.send_purchase_email_to_buyer(buyer_email, purchase_details)

                for creator_id, creator_info in creators_data.items():
                    MailService.send_purchase_email_to_creators(creator_info)

            return {"purchase_id": purchase.ID}, 200
        
        except APIException as aex:
            db.session.rollback()
            return {"message": str(aex), "error_type": aex.error_type}, aex.status_code
        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
    
    @staticmethod
    def get_purchases_by_user_id(user_id):
        purchases = PurchaseRepository.get_purchases_with_details_and_audios_by_user_id(user_id)

        if not purchases:
            return {"message": f"No se encontraron compras para el usuario: {user_id}"}, 404
        
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
                    item_data["audio"]["audio_name"] = detail.item.audio.audio_name

                    if(detail.item.audio.creator and detail.item.audio.creator.user and detail.item.audio.creator.user.user_detail):
                        audio_data["creator"] = { "username": detail.item.audio.creator.user.user_detail.username }
                    else:
                        audio_data["creator"] = None

                else:
                    item_data["audio"] = None

                total += detail.item.price
                
                detail_data["item"] = item_data
                purchase_data["purchase_details"].append(detail_data)

            purchase_data["total"] = total

            result.append(purchase_data)
        
        return result, 200