from flask import current_app, Response

from ..middlewares.api_exception import APIException
from ..repositories.audio_repository import AudioRepository
from ..repositories.item_repository import ItemRepository
from ..services.config_service import ConfigService
from ..utils.validators import validate_audio, validate_audio_file
from ..databases.db import db
from ..databases.mongodb import init_gridfs
from bson import ObjectId

class AudioService:

    @staticmethod
    def get_all_audios():
        audios = AudioRepository.get_all_audios_with_items()
        result = []

        for audio in audios:
            try:
                audio_data = audio.to_dict()
                audio_file = AudioService.get_audio_file_from_gridfs(audio.file_name)

                audio_data["item"] = audio.item.to_dict() if audio.item else None
                audio_data["file_url"] = f"{ConfigService.current_url}/audios/file/{audio.file_name}" if audio_file else None

                result.append(audio_data)
            except Exception as e:
                print(f"Error procesando audio {audio.ID}: {e}")
                continue

        return result, 200
    
    @staticmethod
    def get_audio_by_id(audio_id):
        audio = AudioRepository.get_audio_by_id_with_item(audio_id)

        if audio is None:
            return {"message": f"Audio con id {audio_id} no encontrado"}, 404
        
        audio_data = audio.to_dict()
        audio_file = AudioService.get_audio_file_from_gridfs(audio.file_name)

        audio_data["item"] = audio.item.to_dict() if audio.item else None
        audio_data["file_url"] = f"{ConfigService.current_url}/audios/file/{audio.file_name}" if audio_file else None

        return audio_data, 200
    
    @staticmethod
    def get_audios_by_creator(creator_id):
        audios = AudioRepository.get_audios_by_creator(creator_id)
        result = []

        for audio in audios:
            try:
                audio_data = audio.to_dict()
                audio_file = AudioService.get_audio_file_from_gridfs(audio.file_name)

                audio_data["item"] = audio.item.to_dict() if audio.item else None 
                audio_data["file_url"] = f"{ConfigService.current_url}/audios/file/{audio.file_name}" if audio_file else None

                result.append(audio_data)
            except Exception as e:
                print(f"Error procesando audio {audio.ID}: {e}")

        return result, 200

    @staticmethod 
    def create_audio(data, file):
        try:

            if not data:
                return {"message": "El FormData recibido está vacío"}, 400
            if not file: 
                return {"message": "El archivo de audio no fue proporcionado"}, 400
            
            validation, msg = validate_audio(data, file)
            if not validation:
                return {"message":msg}, 400
        
            grid_fs = current_app.config['GRID_FS']
            file_id = grid_fs.put(file, filename=file.filename)
            file_id_str = str(file_id)

            with db.session.begin():
                new_audio = AudioRepository.create_audio(data, file_id_str)
                new_item = ItemRepository.create_item(data, new_audio.ID)

            db.session.commit()

            return {
                "audio": new_audio.to_dict(),
                "item": new_item.to_dict()
            }, 201
        
        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
        
    @staticmethod 
    def update_audio(audio_id, data):
        try:

            if not data: 
                return {"message": "Los datos proporcionados están vacíos"}, 400

            audio = AudioRepository.get_audio_by_id_with_item(audio_id)

            if not audio:
                return {"message": f"El audio {audio_id} no fue encontrado"}, 404
            
            validation, msg = validate_audio(data, file=None, action="update")
            if not validation:
                return {"message":msg}, 400

            updated_audio = AudioRepository.update_audio(audio.ID, data)
            updated_item = ItemRepository.update_item(audio.item.ID, data)

            if updated_audio is None or updated_item is None:
                raise APIException(msg, status_code=400, error_type="Integrity Error")
            
            db.session.commit()
            
            return {
                "audio": updated_audio.to_dict() if updated_audio else None,
                "item": updated_item.to_dict() if updated_item else None,
            }, 200
        
        except APIException as aex:
            db.session.rollback()
            return {"message": str(aex), "error_type": aex.error_type}, aex.status_code
        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500
    
    @staticmethod 
    def delete_audio(audio_id):
        try:
            audio = AudioRepository.get_audio_by_id_with_item(audio_id)

            if not audio:
                return {"message": f"El audio {audio_id} no fue encontrado"}, 404

            ItemRepository.delete_item(audio.item.ID)
            AudioRepository.delete_audio(audio.ID)

            db.session.commit()

            grid_fs = current_app.config['GRID_FS']
            grid_fs.delete(ObjectId(audio.file_name))

            return {"message": f"Audio {audio_id}, ítem y archivo de mongodb eliminados correctamente."}, 200

        except Exception as e: 
            db.session.rollback()
            return {"message": f"Ocurrió un error elimiando el audio: {e}"}, 500
        
    @staticmethod 
    def update_state_audio(audio_id, updated_state):
        try: 
            audio = AudioRepository.get_audio_by_id_with_item(audio_id)
            if audio is None:
                return {"message": f"Audio con id {audio_id} no encontrado"}, 404
            
            updated_audio = AudioRepository.update_state_audio(audio_id, updated_state)
            updated_item = ItemRepository.update_state_item(audio.item.ID, updated_state)
            
            if updated_state == 'active':
                mail = 'audio active'
                #mail, status = MailService.send_approval_email(audio_data)
            elif updated_state == 'inactive':
                mail = 'audio inactive'
                #mail, status = MailService.send_rejection_email(audio_data)
                #AudioService.delete_audio(audio_id)

            db.session.commit()

            return {
                "message":f"El Audio: {audio_id} ahora es {updated_state}",
                "audio": updated_audio.to_dict() if updated_audio else None,
                "item": updated_item.to_dict() if updated_item else None,
                "mail": mail if mail else None
            }, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f'Ocurrió un error: {str(e)}', "error_type": "Unhandled Exception"}, 500

        
    @staticmethod
    def get_audio_file_from_gridfs(file_name):
        grid_fs = current_app.config['GRID_FS']
        return grid_fs.find_one({"_id": ObjectId(file_name)})

