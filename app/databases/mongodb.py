from flask_pymongo import PyMongo
from gridfs import GridFS

def init_gridfs(app):

    global mongo

    # Inicializar PyMongo 
    mongo = PyMongo(app)

    # Inicializar GridFS solo si mongo.db no es None
    grid_fs = None
    if mongo.db is not None:
        grid_fs = GridFS(mongo.db)
        app.config['MONGODB'] = mongo.db
        app.config['GRID_FS'] = grid_fs
        return grid_fs
    else:
        raise ValueError("Error: mongo.db es None. No se pudo inicializar GridFS.")
