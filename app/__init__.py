import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager


from .databases.mongodb import init_gridfs
from .databases.db import db, migrate 
from .routes.user_routes import user_routes
from .routes.audio_routes import audio_routes
from .routes.favorites_routes import favorites_routes
from .routes.purchase_routes import purchase_routes
from .routes.auth_routes import auth_routes
from .routes.subscriptions_routes import subscription_routes
from .routes.reports_routes import reports_routes
from .middlewares.api_exception import APIException, handle_api_exceptions, handle_general_exceptions
from dotenv import load_dotenv
from .utils.token_manager import is_token_revoked
import logging

# Crear una instancia de Flask
app = Flask(__name__)

# CORS
CORS(app)

# Configuración de la app
app.config.from_object('config.Config')

# Inicializar db y migrate con la app
db.init_app(app)
migrate.init_app(app, db)

# Inicializar GridFS
init_gridfs(app)

# Cargar dotenv
load_dotenv()

# Configurar JWT
app.secret_key = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)
revoked_tokens = set()

# Registrar bloqueo de tokens caducados
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return is_token_revoked(jwt_payload["jti"])

# Registrar middleware de manejo de excepciones
app.register_error_handler(APIException, handle_api_exceptions)
app.register_error_handler(Exception, handle_general_exceptions)

# Registrar las rutas
app.register_blueprint(user_routes)
app.register_blueprint(audio_routes)
app.register_blueprint(favorites_routes)
app.register_blueprint(purchase_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(subscription_routes)
app.register_blueprint(reports_routes)

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
from .models.subscription import Subscription
from .models.subscription_billing import Subscription_billing
 
# Configuración del logging
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info(f'Flask App startup!')
