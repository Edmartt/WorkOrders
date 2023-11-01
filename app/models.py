import datetime
import enum
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from . import db

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    address = db.Column(db.String(64))
    start_date = db.Column(db.DateTime(timezone=True), nullable=True)
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    orders = db.relationship('WorkOrder', backref='customer')

    def __repr__(self) -> str:
        return '<Customer %r>' % self.first_name

# enum type for work orders statuses
class WorkOrderStatus(enum.Enum):
    NEW = 'new'
    DONE = 'done'
    CANCELLED = 'cancelled'

class WorkOrder(db.Model):
    __tablename__ = 'work_orders'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('customers.id'))
    title = db.Column(db.String(64))
    planned_date_begin = db.Column(db.Date)
    planned_date_end = db.Column(db.Date)
    status = db.Column(db.Enum('new', 'done', 'cancelled', name='status type'))
    created_at = db.Column(db.Date, default=datetime.datetime.now().replace(microsecond=0))

    def __repr__(self) -> str:
        return '<WorkOrder %r>' % self.title
