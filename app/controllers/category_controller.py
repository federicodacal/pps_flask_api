import datetime
from flask import jsonify, request
from flask import current_app
from ..utils.collection_sequence import get_next_sequence

class CategoryController:

    @staticmethod
    def get_categories():
        mongo = current_app.config['MONGODB']
        categories = mongo.categoriamodels.find()
        category_list = []
        for category in categories:
            category['_id'] = str(category['_id'])
            category_list.append(category)
        return jsonify(category_list), 200

    @staticmethod
    def get_category(category_id):
        mongo = current_app.config['MONGODB']
        category_id_int = int(category_id)
        category = mongo.categoriamodels.find_one({"id": category_id_int})
        if category:
            category['_id'] = str(category['_id'])
            return jsonify(category), 200
        return jsonify({"error": "Category not found"}), 404
    
    @staticmethod
    def create_category():
        mongo = current_app.config['MONGODB']
        data = request.get_json()
        if 'nombre' not in data:
            return jsonify({"error": "nombre is required"}), 400
        
        next_id = get_next_sequence('categoria_id')
        category_id = mongo.categoriamodels.insert_one({
            "nombre": data['nombre'],
            "id": next_id,
            "fecha_creacion": datetime.datetime.now(),
            "fecha_modificacion": datetime.datetime.now()
        }).inserted_id
        return jsonify({"id": str(category_id)}), 201
    
    @staticmethod
    def update_category(category_id):
        mongo = current_app.config['MONGODB']
        data = request.get_json()

        category_id_int = int(category_id)
        category = mongo.categoriamodels.find_one({"id": category_id_int})
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        mongo.categoriamodels.update_one(
            {"id": category_id_int},
            {"$set": {
                "nombre": data.get('nombre', category['nombre']), 
                "fecha_modificacion": datetime.datetime.now() }
            }  
        )
        return jsonify({"message": "Category updated"}), 200
    
    @staticmethod
    def delete_category(category_id):
        mongo = current_app.config['MONGODB']

        category_id_int = int(category_id)
        category = mongo.categoriamodels.find_one({"id": category_id_int})
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        mongo.categoriamodels.delete_one({"id": category_id_int})
        return jsonify({"message": "Category deleted"}), 200
