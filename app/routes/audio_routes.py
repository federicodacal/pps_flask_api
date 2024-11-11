from flask import Blueprint
from ..controllers.audio_controller import AudioController 

audio_routes = Blueprint('audio_routes', __name__)

audio_routes.route('/audios', methods=["GET"])(AudioController.get_audios)
audio_routes.route('/audios/<string:audio_id>', methods=['GET'])(AudioController.get_audio)
audio_routes.route('/audios', methods=['POST'])(AudioController.create_audio)
audio_routes.route('/audios/<string:audio_id>', methods=['PUT'])(AudioController.update_audio)
audio_routes.route('/audios/<string:audio_id>', methods=['DELETE'])(AudioController.delete_audio)
audio_routes.route('/audios/creator/<string:creator_id>', methods=['GET'])(AudioController.get_audios_by_creator)
audio_routes.route('/audios/file/<string:audio_file_name>', methods=['GET'])(AudioController.get_audio_file)

'''
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