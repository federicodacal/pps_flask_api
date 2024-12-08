import datetime
from flask import jsonify, request
from flask import current_app
from ..utils.collection_sequence import get_next_sequence

class GenreController:

    @staticmethod
    def get_genres():
        mongo = current_app.config['MONGODB']
        genres = mongo.generomodels.find()
        genre_list = []
        for genre in genres:
            genre['_id'] = str(genre['_id'])
            genre_list.append(genre)
        return jsonify(genre_list), 200

    @staticmethod
    def get_genre(genre_id):
        mongo = current_app.config['MONGODB']
        genre_id_int = int(genre_id)
        genre = mongo.generomodels.find_one({"id": genre_id_int})
        if genre:
            genre['_id'] = str(genre['_id'])
            return jsonify(genre), 200
        return jsonify({"error": "Genre not found"}), 404
    
    @staticmethod
    def create_genre():
        mongo = current_app.config['MONGODB']
        data = request.get_json()
        if 'nombre' not in data:
            return jsonify({"error": "nombre is required"}), 400
        
        next_id = get_next_sequence('genero_id')
        genre_id = mongo.generomodels.insert_one({
            "nombre": data['nombre'],
            "id": next_id,
            "fecha_creacion": datetime.datetime.now(),
            "fecha_modificacion": datetime.datetime.now()
        }).inserted_id
        return jsonify({"id": str(genre_id)}), 201
        
    @staticmethod
    def update_genre(genre_id):
        mongo = current_app.config['MONGODB']
        data = request.get_json()

        genre_id_int = int(genre_id)
        genre = mongo.generomodels.find_one({"id": genre_id_int})
        if not genre:
            return jsonify({"error": "Genre not found"}), 404
        
        mongo.generomodels.update_one(
            {"id": genre_id_int},
            {"$set": {
                "nombre": data.get('nombre', genre['nombre']), 
                "fecha_modificacion": datetime.datetime.now() }
            }  
        )
        return jsonify({"message": "Genre updated"}), 200
    
    @staticmethod
    def delete_genre(genre_id):
        mongo = current_app.config['MONGODB']

        genre_id_int = int(genre_id)
        genre = mongo.generomodels.find_one({"id": genre_id_int})
        if not genre:
            return jsonify({"error": "Genre not found"}), 404
        
        mongo.generomodels.delete_one({"id": genre_id_int})
        return jsonify({"message": "Genre deleted"}), 200
    