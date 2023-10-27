from datetime import datetime
from typing import OrderedDict
from flask import request, jsonify
from flask.views import MethodView
from app import db
from app.models import Customer, WorkOrder


class OrdersHTTP(MethodView):

    def __init__(self, order: WorkOrder, customer: Customer) -> None:
        self.order = order
        self.customer = customer

    def get(self):
        since = request.args.get('since')
        until = request.args.get('until')

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

    
    def post(self):
        request_data = request.get_json()
        self.order.customer_id = request_data.get('customer_id')
        self.order.planned_date_begin = datetime.now()
        self.order.title = request_data.get('title')
        self.order.status = request_data.get('status')

        db.session.add(self.order)
        db.session.commit()

        owner_active = self.customer.query.filter_by(id=self.order.customer_id).first()
        owner_active.is_active = True

        if owner_active.start_date == None:
            owner_active.start_date = datetime.now()

        db.session.add(owner_active)
        db.session.commit()
        
        return jsonify({'response': self.order.id}), 201

class HTTPOrderID(MethodView):

    def get(self, id:str):
        #data = request.get_json()
        customer_id = id
        if customer_id is None or customer_id == '':
            return jsonify({'response': 'customer id not sent'}), 401

        
        orders = (db.session.query(WorkOrder, Customer).join(Customer, WorkOrder.customer_id == Customer.id).filter(WorkOrder.customer_id==customer_id).all())

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

        return jsonify({'response': data})

class StatusOrderChange(MethodView):

    def post(self):
        data = request.get_json()
        new_status = data.get('status')
        order_id = data.get('order_id')
        work_order = WorkOrder()
        result = WorkOrder.query.filter_by(id=order_id).first()
        result.status = new_status
        work_order.status = new_status

        db.session.add(result)
        db.session.commit()

        return jsonify({'response': 'status updated'}), 201
