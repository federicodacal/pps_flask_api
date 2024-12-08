from flask import Blueprint
from ..controllers.carrousel_controller import CarrouselController

carrousel_routes = Blueprint('carrousel_routes', __name__)

carrousel_routes.route('/carrousel', methods=['GET'])(CarrouselController.get_carrousel)
carrousel_routes.route('/carrousel/<string:carrousel_id>', methods=['GET'])(CarrouselController.get_carrousel_by_id)
carrousel_routes.route('/carrousel/img/<string:file_id>', methods=['GET'])(CarrouselController.get_carrousel_image)
carrousel_routes.route('/carrousel', methods=['POST'])(CarrouselController.create_carrousel)
carrousel_routes.route('/carrousel/<string:carrousel_id>', methods=['PUT'])(CarrouselController.update_carrousel)
carrousel_routes.route('/carrousel/<string:carrousel_id>', methods=['DELETE'])(CarrouselController.delete_carrousel)