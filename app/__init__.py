from flask import Flask
from flask_cors import CORS
from .mongodb import init_gridfs
from .db import db, migrate 
from .routes.user_routes import user_routes
from .routes.audio_routes import audio_routes
from .routes.purchase_routes import purchase_routes
import logging

# Crear una instancia de Flask
app = Flask(__name__)

# CORS
CORS(app)

# Configuración de la app
app.config.from_object('pps_flask_api.config.Config')

# Inicializar db y migrate con la app
db.init_app(app)
migrate.init_app(app, db)

# Inicializar GridFS
init_gridfs(app)
    
# Configuración de las rutas
app.register_blueprint(user_routes)
app.register_blueprint(audio_routes)
app.register_blueprint(purchase_routes)

# Importar modelos después de definir la app
from .models.user import User
from .models.user_detail import User_detail
from .models.purchase import Purchase
from .models.purchase_detail import Purchase_detail
from .models.item import Item
from .models.favorites import Favorite
from .models.creator import Creator
from .models.audio import Audio
from .models.account import Account
 
# Configuración del logging
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info(f'Flask App startup!')
