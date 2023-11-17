import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from . import db


class Customer:
    def __init__(self, first_name: str | None=None, last_name: str | None=None, address: str | None=None, start_date: datetime.datetime | None=None, end_date: datetime.datetime | None=None, is_active: bool = False) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active

class CustomerTable(db.Model):
    __tablename__ = 'customers'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    address = db.Column(db.String(64))
    start_date = db.Column(db.DateTime(timezone=True), nullable=True)
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    orders = db.relationship('WorkOrderTable', backref='customer')

    def __repr__(self) -> str:
        return '<Customer %r>' % self.first_name

class CustomerORM(CustomerTable):
    @property
    def model(self):
        return Customer(self.first_name, self.last_name, self.address, self.start_date, self.end_date, self.is_active)

class WorkOrder():
    def __init__(self, title: str|None=None, planned_date_begin: datetime.datetime|None=None, planned_date_end: datetime.datetime|None=None, status: str|None=None) -> None:
        self.title = title
        self.planned_date_begin = planned_date_begin
        self.planned_date_end = planned_date_end
        self.status = status

class WorkOrderTable(db.Model):
    __tablename__ = 'work_orders'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('customers.id'))
    title = db.Column(db.String(64))
    planned_date_begin = db.Column(db.DateTime)
    planned_date_end = db.Column(db.DateTime)
    status = db.Column(db.Enum('new', 'done', 'cancelled', name='status type'))
    created_at = db.Column(db.Date, default=datetime.datetime.now().replace(microsecond=0))

    def __repr__(self) -> str:
        return '<WorkOrder %r>' % self.title

class WorkOrderORM(WorkOrderTable):
    @property
    def model(self):
        return WorkOrder(self.title, self.planned_date_begin, self.planned_date_end, self.status)
