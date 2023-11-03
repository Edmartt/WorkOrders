from flask import jsonify, request
from flask.views import MethodView
from app.models import Customer
from app import db
from app.security import auth_decorator
from app.customers.errors.errors import not_authorized

class CustomerHTTP(MethodView):

    decorators = [auth_decorator]

    def __init__(self, customer: Customer) -> None:
        self.customer = customer

    #customer by active status
    def get(self):
        active_customer_list_objects = Customer.query.filter(Customer.is_active).all()
        active_users =[]

        for user in active_customer_list_objects:
            active_users.append({
                'id':user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'address': user.address,
                'start_date': user.start_date,
                'end_date': user.end_date,
                'is_active': user.is_active
                })
        if len(active_users) == 0:
            return jsonify({'response': 'there is no customers with active status'}), 200
        return jsonify({'active_users':active_users}), 200


    #creates customer
    def post(self):
        request_data = request.get_json()

        self.customer.first_name = request_data.get('first_name')
        self.customer.last_name = request_data.get('last_name')
        self.customer.address = request_data.get('address')

        if self.customer.first_name == None or \
                self.customer.last_name == None or \
                self.customer.address == None:
                    return jsonify({'response': 'Mandatory information missing'}), 400

        db.session.add(self.customer)
        db.session.commit()

        return jsonify({'response': self.customer.id}), 201
