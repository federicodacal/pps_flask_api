from flask import Response, jsonify, request
from ..services.audio_service import AudioService

class AudioController:

    @staticmethod
    def get_audios():
        audios = AudioService.get_all_audios()
        return jsonify(audios), 200
    
    @staticmethod
    def get_audio(audio_id):
        audio = AudioService.get_audio_by_id(audio_id)
        if audio is None:
            return {"error": "Audio no encontrado"}, 404
        return jsonify(audio), 200
    
    @staticmethod 
    def get_audio_file(audio_file_name):
        audio_file = AudioService.get_audio_file_from_gridfs(audio_file_name)

        if not audio_file:
            return {"error": "Archivo no encontrado en MongoDB"}, 404

        return Response(audio_file.read(),
                    mimetype='audio/mpeg',  
                    headers={"Content-Disposition": f"attachment;filename={audio_file.filename}"})

    @staticmethod
    def create_audio():

        if 'file' not in request.files:
            print('No hay file')
            return {'error':'Archivo de audio no proporcionado'},400
        
        if request.form is None:
            print('No hay form')
            return {'error':'FormData no proporcionada'},400

        try:

            data = request.form
            file = request.files['file']

            print(f"Data id: {data["ID"]}, audio_name: {data["audio_name"]}")

            new_audio = AudioService.create_audio(data, file)
            print(jsonify(new_audio))
            return jsonify(new_audio), 201
        
        except ValueError as ve:
            print(str(ve))
            return {"error": str(ve)}, 400
        except RuntimeError as re:
            print(str(re))
            return {"error": str(re)}, 500
    
    @staticmethod
    def update_audio(audio_id):
        return 'Update audio'