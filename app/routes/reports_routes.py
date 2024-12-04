from flask import Blueprint
from ..controllers.reports_controller import ReportsController

reports_routes = Blueprint('reports_routes', __name__)

reports_routes.route('/reports/purchases', methods=['GET'])(ReportsController.get_report_purchases)
reports_routes.route('/reports/users', methods=['GET'])(ReportsController.get_report_users)
reports_routes.route('/reports/audios', methods=['GET'])(ReportsController.get_report_audios)
reports_routes.route('/reports/creators', methods=['GET'])(ReportsController.get_report_creators)