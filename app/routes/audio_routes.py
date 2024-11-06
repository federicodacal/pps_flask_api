import datetime
from flask import Blueprint, Response, request, jsonify, current_app
from ..db import db  
from ..models.audio import Audio 
from ..mongodb import init_gridfs
from bson import ObjectId

audio_routes = Blueprint('audio_routes', __name__)

# Función auxiliar para obtener el archivo desde GridFS
def get_audio_file_from_gridfs(file_name):
    grid_fs = current_app.config['GRID_FS']
    audio_file = grid_fs.find_one({"_id": ObjectId(file_name)})
    return audio_file

# GET ALL
@audio_routes.route('/audios')
def get_audios():
    audios = Audio.query.all()
    audios_list = []

    for audio in audios:
        audio_dict = audio.to_dict()  # Convertimos el objeto de audio a diccionario
        
        # Buscamos el archivo en MongoDB usando el 'file_name' que está almacenado en el modelo Audio
        audio_file = get_audio_file_from_gridfs(audio.file_name)
        
        if audio_file:
            # Si el archivo existe en MongoDB, podemos incluir la URL de descarga
            audio_dict["file_url"] = f"http://localhost:5000/audios/file/{audio.file_name}"
        else:
            audio_dict["file_url"] = None  # Si no existe el archivo, lo indicamos

        audios_list.append(audio_dict)

    return jsonify(audios_list), 200

# GET BY ID
@audio_routes.route('/audios/<string:audio_id>', methods=['GET'])
def get_audio(audio_id):
    audio = Audio.query.get(audio_id)
    
    if not audio:
        return {"error": "Audio no encontrado"}, 404

    # Obtenemos los detalles del audio, sin el archivo binario
    audio_dict = audio.to_dict()

    # Obtenemos el archivo correspondiente en MongoDB (GridFS)
    audio_file = get_audio_file_from_gridfs(audio.file_name)

    if not audio_file:
        return {"error": "Archivo no encontrado en MongoDB"}, 404

    # Incluir la URL del archivo en la respuesta
    audio_dict["file_url"] = f"http://localhost:5000/audios/file/{audio.file_name}"

    return jsonify(audio_dict), 200


# GET BY FILENAME (bin)
@audio_routes.route('/audios/file/<string:audio_file_name>', methods=['GET'])
def get_audio_file(audio_file_name):
    audio_file = get_audio_file_from_gridfs(audio_file_name)

    if not audio_file:
        return {"error": "Archivo no encontrado en MongoDB"}, 404

    # Establecer el tipo de contenido adecuado, por ejemplo 'audio/mpeg' o el tipo real del archivo
    return Response(audio_file.read(),
                    mimetype='audio/mpeg',  # Ajusta según el tipo real del archivo (puedes hacerlo dinámicamente)
                    headers={"Content-Disposition": f"attachment;filename={audio_file.filename}"})

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
    if 'file' not in request.files:
        return {'error':'Archivo de audio no proporcionado'},400
    
    file = request.files['file']
    
    # Cargar el archivo en GridFS
    grid_fs = current_app.config['GRID_FS']
    file_id = grid_fs.put(file, filename=file.filename)
    file_id_str = str(file_id)

    # Otros datos 
    data = request.form

    if not data:
        return {"error": "Faltaron datos"}, 400
    
    required_fields = ['ID', 'audio_name', 'state', 'category', 'genre', 'BPM', 'tone', 'length', 'size', 'description']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return {'error': f"Faltan los siguientes campos: {', '.join(missing_fields)}"}, 400

    new_audio = Audio(
        ID=data['ID'],
        creator_ID=data['creator_ID'],
        file_name=file_id_str,
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