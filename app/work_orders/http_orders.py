from datetime import datetime
from collections import OrderedDict
from flask import json, request, jsonify
from flask.views import MethodView
from app import db
from app.redis_pkg.redis import RedisConnection
from app.models import Customer, WorkOrder
from .helpers.date_format_check import check_date_format


class OrdersHTTP(MethodView):

    def __init__(self, order: WorkOrder, customer: Customer) -> None:
        self.order = order
        self.customer = customer

    #orders by date range
    def get(self):
        since = request.args.get('since')
        until = request.args.get('until')

        if since is None or until is None:
            return jsonify({'response': 'wrong date parameter'}), 400

        check_since_date = check_date_format(since)
        check_until_date = check_date_format(until)

        if type(check_since_date) == ValueError or \
                type(check_until_date) == ValueError:
                    return jsonify({'response': 'wrong date format. Use YYYY-MM-DD'}), 400

        orders = (db.session.query(WorkOrder, Customer).join(Customer, WorkOrder.customer_id == Customer.id).filter(WorkOrder.created_at.between(since, until)).all())

        data = []

        for order, customer in orders:
            customer_orders = OrderedDict()
            customer_orders['order_id'] = order.id
            customer_orders['order_title'] = order.title
            customer_orders['order_planned_date_begin'] = order.planned_date_begin
            customer_orders['order_planned_date_end'] = order.planned_date_end
            customer_orders['order_status'] = order.status
            customer_orders['order_created_at'] = order.created_at
            customer_orders['customer_id'] = customer.id
            customer_orders['customer_first_name'] = customer.first_name
            customer_orders['customer_last_name'] = customer.last_name
            customer_orders['customer_address'] = customer.address
            customer_orders['customer_start_date'] = customer.start_date
            customer_orders['customer_end_date'] = customer.end_date
            customer_orders['customer_is_active'] = customer.is_active
                    
            data.append(customer_orders)

        return jsonify({'orders': data})
    
    #creates order
    def post(self):
        request_data = request.get_json()
        self.order.customer_id = request_data.get('customer_id')
        self.order.planned_date_begin = datetime.now()
        self.order.title = request_data.get('title')
        self.order.status = request_data.get('status')

        customer = self.customer.query.filter_by(id=self.order.customer_id).first()

        if customer is None:
            return jsonify({'response': 'customer_id not found: {}'.format(self.order.customer_id)}), 404

        if self.order.customer_id is None:
            return jsonify({'response': 'customer id empty'}), 400

        db.session.add(self.order)
        db.session.commit()

        owner_active = self.customer.query.filter_by(id=self.order.customer_id).first()
        owner_active.is_active = True

        if owner_active.start_date is None:
            owner_active.start_date = datetime.now()

        db.session.add(owner_active)
        db.session.commit()
        
        return jsonify({'response': self.order.id}), 201

    def put(self):

        data = request.get_json()
        new_status = data.get('status')

        allowed_statuses = ['new', 'cancelled', 'done']

        if new_status not in allowed_statuses:
            return jsonify({'response': 'this status is not allowed: {}'.format(new_status)}), 400

        order_id = data.get('order_id')
        result = WorkOrder.query.filter_by(id=order_id).first()

        if result is None:
            return jsonify({'response': 'this order ID does not exists: {}'.format(order_id)}), 404

        result.status = new_status

        db.session.commit()

        order_dict = {'id': str(result.id), 'order_title': result.title, 'order_planned_date_begin': str(result.planned_date_begin), 'planned_date_end': str(result.planned_date_end), 'customer_id': str(result.customer_id), 'status': result.status}

        if result.status == 'done':
            redis_object = RedisConnection()
            redis_connection = redis_object.get_connection()
            redis_connection.xadd('order_done', order_dict, '*')

        return jsonify({'response': 'status updated', 'object': order_dict}), 200

class HTTPOrderID(MethodView):

    #get order by customer id
    def get(self, id:str):
        #data = request.get_json()
        customer_id = id
        if customer_id is None or customer_id == '':
            return jsonify({'response': 'customer id not sent'}), 400

        customer_result = Customer.query.filter_by(id=customer_id).first()

        if customer_result is None:
            return jsonify({'response': 'customer ID not found: {}'.format(customer_id)}), 404

        
        orders = (db.session.query(WorkOrder, Customer).join(Customer, WorkOrder.customer_id == Customer.id).filter(WorkOrder.customer_id==customer_id).all())

        data = []


        for order, customer in orders:

            customer_orders = {}
            customer_orders['customer_orders'] = {}
            customer_data = {}
            customer_data['customer_data'] = {}
            data_dict ={}
            customer_orders['order_id'] = order.id
            customer_orders['customer_id'] = order.customer_id
            customer_orders['order_title'] = order.title
            customer_orders['order_planned_date_begin'] = order.planned_date_begin
            customer_orders['order_planned_date_end'] = order.planned_date_end
            customer_orders['order_status'] = order.status
            customer_orders['order_created_at'] = order.created_at
            customer_data['customer_data']['customer_id'] = customer.id
            customer_data['customer_data']['customer_first_name'] = customer.first_name
            customer_data['customer_data']['customer_last_name'] = customer.last_name
            customer_data['customer_data']['customer_address'] = customer.address
            customer_data['customer_data']['customer_start_date'] = customer.start_date
            customer_data['customer_data']['customer_end_date'] = customer.end_date
            customer_data['customer_data']['customer_is_active'] = customer.is_active

            customer_data['customer_orders'] = customer_orders
            data_dict['order_response'] = customer_data

            data.append(data_dict)

        return jsonify({'orders': data})
