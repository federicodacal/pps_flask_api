from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os

# Crear una instancia de Flask
app = Flask(__name__)

# Configuración de la app
app.config.from_object('pps_flask_api.config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importar rutas y modelos después de definir la app
from pps_flask_api.app import routes
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
