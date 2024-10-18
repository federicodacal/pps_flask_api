from flask import Flask
from pps_flask_api.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import logging

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from pps_flask_api.app import routes
from pps_flask_api.app.models import *

# Setup console loggin
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App startup')
