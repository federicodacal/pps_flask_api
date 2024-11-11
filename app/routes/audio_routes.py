import datetime
from flask import Blueprint, Response, request, jsonify, current_app
from ..controllers.audio_controller import AudioController 
from ..databases.db import db  
from ..models.audio import Audio 
from ..databases.mongodb import init_gridfs
from bson import ObjectId

audio_routes = Blueprint('audio_routes', __name__)

audio_routes.route('/audios', methods=["GET"])(AudioController.get_audios)
audio_routes.route('/audios/<string:audio_id>', methods=['GET'])(AudioController.get_audio)
audio_routes.route('/audios', methods=['POST'])(AudioController.create_audio)
audio_routes.route('/audios/<string:audio_id>', methods=['PUT'])(AudioController.update_audio)
audio_routes.route('/audios/file/<string:audio_file_name>', methods=['GET'])(AudioController.get_audio_file)

'''
# UPDATE
@audio_routes.route('/audios/<string:audio_id>', methods=['PUT'])
def update_audio(audio_id):

    data = request.json or {}

    if not data:
        return {"error": "Datos no proporcionados"}, 400

    audio = Audio.query.get(audio_id)
    if not audio:
        return {"error": "Audio no encontrado"}, 404

    audio.file_name = data.get('file_name', audio.file_name)
    audio.audio_name = data.get('audio_name', audio.audio_name)
    audio.state = data.get('state', audio.state)
    audio.category = data.get('category', audio.category)
    audio.genre = data.get('genre', audio.genre)
    audio.BPM = data.get('BPM', audio.BPM)
    audio.tone = data.get('tone', audio.tone)
    audio.length = data.get('length', audio.length)
    audio.size = data.get('size', audio.size)
    audio.score = data.get('score', audio.score)
    audio.description = data.get('description', audio.description)
    audio.modified_at = datetime.datetime.now(datetime.timezone.utc)

    db.session.commit()
    return jsonify(audio.to_dict()), 200

# DELETE
@audio_routes.route('/audios/<string:audio_id>', methods=['DELETE'])
def delete_audio(audio_id):

    audio = Audio.query.get(audio_id)

    if not audio:
        return {"error": "Audio no encontrado"}, 404

    db.session.delete(audio)
    db.session.commit()
    return {"message": "Audio eliminado exitosamente"}, 200

'''