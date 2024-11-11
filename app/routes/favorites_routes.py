from flask import Blueprint
from ..controllers.favorites_controller import FavoriteController 

favorites_routes = Blueprint('favorites_routes', __name__)

favorites_routes.route('/favorites/<string:user_id>', methods=["GET"])(FavoriteController.get_favorites)
favorites_routes.route('/favorites/<string:audio_id>', methods=['POST'])(FavoriteController.add_favorite)
favorites_routes.route('/favorites/<string:audio_id>', methods=['DELETE'])(FavoriteController.delete_favorite)