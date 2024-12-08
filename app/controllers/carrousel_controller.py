import datetime
from io import BytesIO
from bson import ObjectId
from flask import Response, jsonify, request, send_file
from flask import current_app
from gridfs import GridFS

from ..services.config_service import ConfigService
from ..utils.collection_sequence import get_next_sequence

class CarrouselController:

    @staticmethod
    def get_carrousel():
        mongo = current_app.config['MONGODB']
        carrousel = mongo.carrouselmodels.find()
        carrou_list = []
        for carrou in carrousel:
            for key, value in carrou.items():
                if isinstance(value, ObjectId):
                    carrou[key] = str(value)

            file_id = carrou.get("file_id")
            if file_id:
                carrou["imgUrl"] = f"{ConfigService.current_url}/carrousel/img/{file_id}"
            else:
                carrou["imgUrl"] = None

            carrou_list.append(carrou)
        return jsonify(carrou_list), 200

    @staticmethod
    def get_carrousel_by_id(carrousel_id):
        mongo = current_app.config['MONGODB']
    
        try:
            carrousel_id_int = int(carrousel_id)
        except ValueError:
            return jsonify({"error": "Invalid carrousel ID format"}), 400

        carrou = mongo.carrouselmodels.find_one({"id": carrousel_id_int})
        if not carrou:
            return jsonify({"error": "Carrousel not found"}), 404

        for key, value in carrou.items():
            if isinstance(value, ObjectId):
                carrou[key] = str(value)

        file_id = carrou.get("file_id")
        if file_id:
            carrou["imgUrl"] = f"{ConfigService.current_url}/carrousel/img/{file_id}"
        else:
            carrou["imgUrl"] = None

        return jsonify(carrou), 200
    
    @staticmethod
    def get_carrousel_image(file_id):
        mongo = current_app.config['MONGODB']
        grid_fs = GridFS(mongo, collection="images")
        file = grid_fs.find_one({"_id": ObjectId(file_id)})

        if not file:
            return {"message": "Imagen no encontrada"}, 404 

        file_data = file.read()
 
        return Response(file_data, mimetype=file.content_type)
    
    @staticmethod
    def create_carrousel():
        mongo = current_app.config['MONGODB']
        grid_fs = current_app.config['GRID_FS']

        data = request.form
        file = request.files.get('file')

        if not file or not file.filename or file.filename == '' or '.' not in file.filename:
            return {"message": "La imagen no fue proporcionada o es inválida"}, 400
        
        ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            return {"message": "El archivo no es un formato de imagen permitido"}, 400

        if not file.content_type.startswith('image/'):
            return {"message": "El archivo no es una imagen válida"}, 400

        try:
            file_id = grid_fs.put(file, filename=file.filename)

            next_id = get_next_sequence('carrousel_id')
            carrousel_id = mongo.carrouselmodels.insert_one({
                "titulo": data['titulo'],
                "descripcion": data['descripcion'],
                "id": next_id,
                "file_id": ObjectId(file_id),
                "fecha_creacion": datetime.datetime.now(),
                "fecha_modificacion": datetime.datetime.now()
            }).inserted_id

        except Exception as e:
            return {"message": f"Error al guardar el archivo: {str(e)}"}, 500

        return {"message": f"Imagen subida con éxito: {carrousel_id}", "file_id": str(file_id)}, 201
    
    @staticmethod
    def update_carrousel(carrousel_id):
        mongo = current_app.config['MONGODB']
        data = request.get_json()

        carrousel_id_int = int(carrousel_id)
        carrousel = mongo.carrouselmodels.find_one({"id": carrousel_id_int})
        if not carrousel:
            return jsonify({"error": "Carrousel not found"}), 404
        
        mongo.carrouselmodels.update_one(
            {"id": carrousel_id_int},
            {"$set": {
                "titulo": data.get('titulo', carrousel['titulo']), 
                "descripcion": data.get('descripcion', carrousel['descripcion']), 
                "fecha_modificacion": datetime.datetime.now() }
            }  
        )
        return jsonify({"message": "Category updated"}), 200
    
    @staticmethod
    def delete_carrousel(carrousel_id):
        mongo = current_app.config['MONGODB']

        carrousel_id_int = int(carrousel_id)
        carrousel = mongo.carrouselmodels.find_one({"id": carrousel_id_int})
        if not carrousel:
            return jsonify({"error": "Carrousel not found"}), 404
        
        mongo.carrouselmodels.delete_one({"id": carrousel_id_int})
        return jsonify({"message": "Carrousel deleted"}), 200
