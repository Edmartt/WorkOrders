from app.customers.http_customer import CustomerHTTP
from app.models import Customer
from . import customer_bp

customer = Customer()
customer_http = CustomerHTTP.as_view('customer', customer)

customer_bp.add_url_rule('/api/v1/customer', view_func=customer_http, methods=['POST'])

customer_bp.add_url_rule('/api/v1/customer', view_func=customer_http, methods=['GET'])
