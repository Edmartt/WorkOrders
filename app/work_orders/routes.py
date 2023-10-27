from app.models import Customer, WorkOrder
from app.work_orders.http_orders import OrdersHTTP, HTTPOrderID, StatusOrderChange
from . import orders_bp

order = WorkOrder()
customer = Customer()

orders_http = OrdersHTTP.as_view('orders', order, customer)
order_get_id = HTTPOrderID.as_view('by id')
order_status_change = StatusOrderChange.as_view('change')

orders_bp.add_url_rule('/api/v1/orders', view_func=orders_http, methods=['POST'])

orders_bp.add_url_rule('/api/v1/orders/<string:id>', view_func=order_get_id, methods=['GET'])

orders_bp.add_url_rule('/api/v1/orders/range', view_func=orders_http, methods=['GET'])

orders_bp.add_url_rule('/api/v1/orders/status', view_func=order_status_change, methods=['POST'])
