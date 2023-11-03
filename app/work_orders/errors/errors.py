from flask import make_response, jsonify
from app import work_orders

@work_orders.orders_bp.errorhandler(401)
def not_authorized(error):
    return make_response(jsonify({'response': 'not authorized'}), 401)
