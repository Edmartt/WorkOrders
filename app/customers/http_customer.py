from flask import jsonify, request
from flask.views import MethodView
from app.models import Customer
from app import db

class CustomerHTTP(MethodView):

    def __init__(self, customer: Customer) -> None:
        self.customer = customer

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
        return jsonify({'active_users':active_users})


    def post(self):
        request_data = request.get_json()

        self.customer.first_name = request_data.get('first_name')
        self.customer.last_name = request_data.get('last_name')
        self.customer.address = request_data.get('address')

        db.session.add(self.customer)
        db.session.commit()

        return jsonify({'response': self.customer.id}), 201
