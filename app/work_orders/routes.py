from app.models import CustomerORM, WorkOrderORM
from app.work_orders.http_orders import OrdersHTTP, HTTPOrderID
from . import orders_bp

order = WorkOrderORM()
customer = CustomerORM()

orders_http = OrdersHTTP.as_view('orders', order, customer)
order_get_id = HTTPOrderID.as_view('by id')

orders_bp.add_url_rule('/api/v1/orders', view_func=orders_http, methods=['GET'])
orders_bp.add_url_rule('/api/v1/orders/<string:id>', view_func=order_get_id, methods=['GET'])
orders_bp.add_url_rule('/api/v1/orders', view_func=orders_http, methods=['POST'])
orders_bp.add_url_rule('/api/v1/orders', view_func=orders_http, methods=['PUT'])
