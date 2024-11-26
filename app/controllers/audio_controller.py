import re
from flask import Response, jsonify, request, send_file, stream_with_context
from ..services.audio_service import AudioService
from flask_jwt_extended import jwt_required

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
        '''
        audio_file = AudioService.get_audio_file_from_gridfs(audio_file_name)

        if not audio_file:
            return {"error": "Archivo no encontrado en MongoDB"}, 404
        
        file_size = audio_file.length
        start = 0
        end = file_size - 1

        range_header = request.headers.get('Range', None)
        if range_header:
            
            if range_match:
                start = int(range_match.group(1))
                if range_match.group(2):
                    end = int(range_match.group(2))

        chunk_size = (end - start) + 1
        audio_file.seek(start)

    
        def generate():
            remaining = chunk_size
            while remaining > 0:
                chunk = audio_file.read(min(8192, remaining))  
                if not chunk:
                    break
                remaining -= len(chunk)
                yield chunk

        return Response(
            generate(),
            status=206,  # Transmisión parcial
            mimetype='audio/mpeg',
            headers={
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(chunk_size),
                "Content-Disposition": f"inline; filename={audio_file.filename}",
                "Transfer-Encoding": "chunked",
            },
        )
        '''
        audio_file = AudioService.get_audio_file_from_gridfs(audio_file_name)

        if not audio_file:
            return {"message": "Archivo de audio no encontrado"}, 404

        return send_file(
            audio_file, 
            mimetype='audio/mpeg',  
            as_attachment=True, 
            download_name=audio_file.filename
        ), 200
        
        
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