from flask import Flask
from pps_flask_api.app.db import db, migrate 
from pps_flask_api.app.routes.user_routes import user_routes
from pps_flask_api.app.routes.audio_routes import audio_routes
from pps_flask_api.app.routes.purchase_routes import purchase_routes
import logging
import os

# Crear una instancia de Flask
app = Flask(__name__)

# Configuración de la app
app.config.from_object('pps_flask_api.config.Config')

# Inicializar db y migrate con la app
db.init_app(app)
migrate.init_app(app, db)

# Configuración de las rutas
app.register_blueprint(user_routes)
app.register_blueprint(audio_routes)
app.register_blueprint(purchase_routes)

# Importar modelos después de definir la app
from pps_flask_api.app.models.user import User
from pps_flask_api.app.models.audio import Audio
from pps_flask_api.app.models.favorites import Favorite
from pps_flask_api.app.models.purchase_detail import Purchase_detail
from pps_flask_api.app.models.item import Item
from pps_flask_api.app.models.purchase import Purchase
 
# Configuración del logging
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App startup')
