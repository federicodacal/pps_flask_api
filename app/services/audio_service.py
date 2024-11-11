from flask import current_app, Response
from ..repositories.audio_repository import AudioRepository
from ..repositories.item_repository import ItemRepository
from ..databases.db import db
from ..databases.mongodb import init_gridfs
from bson import ObjectId

class AudioService:

    @staticmethod
    def get_all_audios():
        audios = AudioRepository.get_all_audios_with_items()
        result = []

        for audio in audios:
            audio_data = audio.to_dict()
            audio_file = AudioService.get_audio_file_from_gridfs(audio.file_name)

            audio_data["item"] = audio.item.to_dict() if audio.item else None
            audio_data["file_url"] = f"http://localhost:5000/audios/file/{audio.file_name}" if audio_file else None

            result.append(audio_data)

        return result
    
    @staticmethod
    def get_audio_by_id(audio_id):
        audio = AudioRepository.get_audio_by_id_with_item(audio_id)

        if audio is None:
            return None
        
        audio_data = audio.to_dict()
        audio_file = AudioService.get_audio_file_from_gridfs(audio.file_name)

        audio_data["item"] = audio.item.to_dict() if audio.item else None
        audio_data["file_url"] = f"http://localhost:5000/audios/file/{audio.file_name}" if audio_file else None

        return audio_data
            
    
    @staticmethod 
    def create_audio(data, file):
        if not data or not file: 
            raise ValueError("Datos o archivos no fueron proporcionados")
        
        required_fields = ['ID', 'audio_name', 'state', 'category', 'genre', 'BPM', 'tone', 'length', 'size', 'description', 'state_item', 'price', 'item_ID']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {'error': f"Faltan los siguientes campos: {', '.join(missing_fields)}"}, 400
        
        try:
        
            grid_fs = current_app.config['GRID_FS']
            file_id = grid_fs.put(file, filename=file.filename)
            file_id_str = str(file_id)

            with db.session.begin():
                new_audio = AudioRepository.create_audio(data, file_id_str)
                new_item = ItemRepository.create_item(data, data["ID"])

            db.session.commit()

            return {
                "audio": new_audio.to_dict(),
                "item": new_item.to_dict()
            }
        
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Ocurrió un error al crear el audio: {str(e)}")
    
    @staticmethod
    def get_audio_file_from_gridfs(file_name):
        grid_fs = current_app.config['GRID_FS']
        return grid_fs.find_one({"_id": ObjectId(file_name)})


    '''
    def get_all_audios():
        audios = AudioRepository.get_all_audios_with_items()
        
        result = []
        for audio in audios:
            audio_data = audio.to_dict()  
        
            audio_data["item"] = audio.item.to_dict() if audio.item else None
            result.append(audio_data)

        return result
    '''