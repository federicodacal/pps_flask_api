from flask import Response, jsonify, request
from ..services.audio_service import AudioService

class AudioController:

    @staticmethod
    def get_audios():
        response, status_code = AudioService.get_all_audios()
        return jsonify(response), status_code
    
    @staticmethod
    def get_audio(audio_id):
        response, status_code = AudioService.get_audio_by_id(audio_id)
        return jsonify(response), status_code
    
    @staticmethod 
    def get_audio_file(audio_file_name):
        audio_file = AudioService.get_audio_file_from_gridfs(audio_file_name)

        if not audio_file:
            return {"error": "Archivo no encontrado en MongoDB"}, 404

        return Response(audio_file.read(),
                    mimetype='audio/mpeg',  
                    headers={"Content-Disposition": f"attachment;filename={audio_file.filename}"})
    
    @staticmethod
    def get_audios_by_creator(creator_id):
        response, status_code = AudioService.get_audios_by_creator(creator_id)
        return jsonify(response), status_code
    
    @staticmethod
    def create_audio():
        data = request.form or {}
        file = request.files['file'] or {}

        response, status_code = AudioService.create_audio(data, file)
        return jsonify(response), status_code
        
    @staticmethod
    def update_audio(audio_id):
        data = request.json or {}
        response, status_code = AudioService.update_audio(audio_id, data)
        return jsonify(response), status_code
    
    @staticmethod
    def delete_audio(audio_id):
        response, status_code = AudioService.delete_audio(audio_id)
        return jsonify(response), status_code