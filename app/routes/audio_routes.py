import datetime
from flask import Blueprint, request, jsonify
from pps_flask_api.app.db import db  
from pps_flask_api.app.models.audio import Audio 

audio_routes = Blueprint('audio_routes', __name__)

# GET ALL
@audio_routes.route('/audios')
def get_audios():
    return 'Listado Audios'

# GET BY ID
@audio_routes.route('/audios/<string:audio_id>', methods=['GET'])
def get_audio(audio_id):
    return 'Audio ID:' + audio_id

# CREATE
@audio_routes.route('/audios', methods=['POST'])
def create_audio():
    return 'Create Audio'

# UPDATE
@audio_routes.route('/audios/<string:audio_id>', methods=['PUT'])
def update_audio(audio_id):
    return 'Update Audio'

# DELETE
@audio_routes.route('/audios/<string:audio_id>', methods=['DELETE'])
def delete_audio(audio_id):
    return 'Delete Audio'