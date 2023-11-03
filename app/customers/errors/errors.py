from flask import jsonify, make_response
from app import customers

@customers.customer_bp.errorhandler(401)
def not_authorized(error):
    return make_response(jsonify({'response': 'not authorized'}), 401)
