from flask import Blueprint
from ..controllers.genre_controller import GenreController

genre_routes = Blueprint('genre_routes', __name__)

genre_routes.route('/genres', methods=['GET'])(GenreController.get_genres)
genre_routes.route('/genres/<string:genre_id>', methods=['GET'])(GenreController.get_genre)
genre_routes.route('/genres', methods=['POST'])(GenreController.create_genre)
genre_routes.route('/genres/<string:genre_id>', methods=['PUT'])(GenreController.update_genre)
genre_routes.route('/genres/<string:genre_id>', methods=['DELETE'])(GenreController.delete_genre)