from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializar db y migrate
db = SQLAlchemy()
migrate = Migrate()