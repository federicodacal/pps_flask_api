from flask import current_app
from pymongo import ReturnDocument

def get_next_sequence(sequence_name):
    try:
        mongo = current_app.config['MONGODB']
        
        # Actualizar el contador y obtener el valor actualizado
        counter = mongo.countermodels.update_one(
            {'_id': sequence_name}, 
            {'$inc': {'sequence_value': 1}}, 
            upsert=True
        )
        
        # Obtener el contador actualizado
        counter = mongo.countermodels.find_one({'_id': sequence_name})
        
        # Verificar si se obtuvo el valor
        if counter and 'sequence_value' in counter:
            return counter['sequence_value']
        else:
            print('Error: sequence_value no encontrado en counter.')
            return None
        
    except Exception as e:
        print(f'Error al obtener secuencia: {e}')
        return None