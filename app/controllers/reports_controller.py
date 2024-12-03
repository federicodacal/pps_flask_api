from flask import jsonify, request

from ..services.reports_service import ReportsService

class ReportsController:

    @staticmethod
    def get_report_purchases():
        response, status_code = ReportsService.get_report_purchases()
        return jsonify(response), status_code
    
    @staticmethod
    def get_report_users():
        response, status_code = ReportsService.get_report_users()
        return jsonify(response), status_code
    
    @staticmethod
    def get_report_audios():
        response, status_code = ReportsService.get_report_audios()
        return jsonify(response), status_code
    
    @staticmethod
    def get_report_creators():
        response, status_code = ReportsService.get_report_creators()
        return jsonify(response), status_code