from __init__ import db

class ShipmentType(db.Model):
    __tablename__ = 'Shipment_Type'
    __table_args__ = {'schema': 'order_schema'}
    
    shipment_type_id = db.Column(db.Integer, primary_key=True)
    shipment_type_name = db.Column(db.String)
    description = db.Column(db.String)

class Order(db.Model):
    __tablename__ = 'Order'
    __table_args__ = {'schema': 'order_schema'}

    order_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    sender_address = db.Column(db.String)
    sender_name = db.Column(db.String)
    receiver_id = db.Column(db.Integer)
    receiver_name = db.Column(db.String)
    receiver_address = db.Column(db.String)
    receiver_phone = db.Column(db.String)
    order_date = db.Column(db.DateTime)
    total_amount = db.Column(db.Numeric)
    shipment_type_id = db.Column(db.Integer, db.ForeignKey('order_schema.Shipment_Type.shipment_type_id'))
    items = db.relationship("OrderItem", back_populates="order")

class OrderItem(db.Model):
    __tablename__ = 'Order_Item'
    __table_args__ = {'schema': 'order_schema'}
    
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order_schema.Order.order_id'))
    weight = db.Column(db.Numeric)
    length = db.Column(db.Numeric)
    width = db.Column(db.Numeric)
    height = db.Column(db.Numeric)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric)
    order = db.relationship("Order", back_populates="items")


