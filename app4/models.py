from __init__ import db

class ShipmentStatus(db.Model):
    __tablename__ = 'Shipment_Status'
    __table_args__ = {'schema': 'shipment_schema'}
    shipment_status_id = db.Column(db.Integer, primary_key=True)
    shipment_status_name = db.Column(db.String)

class Shipment(db.Model):
    __tablename__ = 'Shipment'
    __table_args__ = {'schema': 'shipment_schema'}
    
    shipment_id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String)
    order_id = db.Column(db.Integer)
    shipping_type = db.Column(db.String)
    sender_name = db.Column(db.String)
    sender_address = db.Column(db.String)
    receiver_name = db.Column(db.String)
    receiver_address = db.Column(db.String)
    shipment_status_id = db.Column(db.Integer, db.ForeignKey('shipment_schema.Shipment_Status.shipment_status_id'))
    shipment_date = db.Column(db.DateTime)
    delivery_date = db.Column(db.DateTime)
    estimated_delivery_date = db.Column(db.DateTime)
    actual_delivery_date = db.Column(db.DateTime)
    events = db.relationship("Event", back_populates="shipment")

class Event(db.Model):
    __tablename__ = 'Event'
    __table_args__ = {'schema': 'shipment_schema'}
    event_id = db.Column(db.Integer, primary_key=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment_schema.Shipment.shipment_id'))
    shipment_status_id = db.Column(db.Integer, db.ForeignKey('shipment_schema.Shipment_Status.shipment_status_id'))
    event_date = db.Column(db.DateTime)
    comment = db.Column(db.String)
    shipment = db.relationship("Shipment", back_populates="events")

