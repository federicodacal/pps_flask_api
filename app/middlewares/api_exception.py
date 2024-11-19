import traceback
import logging
from flask import jsonify

logger = logging.getLogger("api_errors")
logging.basicConfig(level=logging.ERROR)

class APIException(Exception):
    def __init__(self, message, status_code=400, error_type="Application Error"):
        super().__init__(message)
        self.message = message 
        self.status_code = status_code
        self.error_type = error_type

def handle_api_exceptions(error):
    error_trace = traceback.format_exc()
    logger.error(f"Error: {error.message}\nTraceback: {error_trace}")
    response = {
        "error": error.message,
        "type": error.error_type,
        #"traceback": error_trace
    }
    return jsonify(response), error.status_code

def handle_general_exceptions(error):
    error_trace = traceback.format_exc()
    logger.error(f"Unhandled Exception: {str(error)}\nTraceback: {error_trace}")
    response = {
        "error": str(error),
        "type": "Unhandled Exception",
        #"traceback": error_trace
    }
    return jsonify(response), 500
    

        
