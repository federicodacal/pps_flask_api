import datetime
from flask import Blueprint, request, jsonify
from ..db import db  
from ..models.audio import Audio 

audio_routes = Blueprint('audio_routes', __name__)

# GET ALL
@audio_routes.route('/audios')
def get_audios():
    audios = Audio.query.all()
    return jsonify([audio.to_dict() for audio in audios]), 200

# GET BY ID
@audio_routes.route('/audios/<string:audio_id>', methods=['GET'])
def get_audio(audio_id):
    audio = Audio.query.get(audio_id)
    if not audio:
        return {"error": "Audio no encontrado"}, 404
    return jsonify(audio.to_dict()), 200

# GET BY CREATOR ID
@audio_routes.route('/audios/creator/<string:creator_id>', methods=['GET'])
def get_audios_by_creator(creator_id):
    audios = Audio.query.filter_by(creator_ID=creator_id).all()
    if audios:
        return jsonify([audio.to_dict() for audio in audios]), 200
    else:
        return {"error": "No se encontraron audios para este creador"}, 404

# CREATE
@audio_routes.route('/audios', methods=['POST'])
def create_audio():

    data = request.json or {}

    if not data:
        return {"error": "Datos no proporcionados"}, 400

    new_audio = Audio(
        ID=data['ID'],
        creator_ID=data['creator_ID'],
        file_name=data['file_name'],
        audio_name=data['audio_name'],
        state=data['state'],
        category=data['category'],
        genre=data['genre'],
        BPM=data['BPM'],
        tone=data['tone'],
        length=data['length'],
        size=data['size'],
        score=data.get('score'),  # Opcional
        description=data['description'],
        created_at=datetime.datetime.now(datetime.timezone.utc),
        modified_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.session.add(new_audio)
    db.session.commit()
    return jsonify(new_audio.to_dict()), 201

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