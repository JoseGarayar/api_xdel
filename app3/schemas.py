from flask_restx import fields
from __init__ import api

order_item_schema = api.model('Order_Item', {
    'order_item_id': fields.Integer(description='Order Item ID'),
    'order_id': fields.Integer(description='Order ID'),
    'weight': fields.Float(description='Weight'),
    'length': fields.Float(description='Length'),
    'width': fields.Float(description='Width'),
    'height': fields.Float(description='Height'),
    'quantity': fields.Integer(description='Quantity'),
    'price': fields.Float(description='Price')
})

order_schema = api.model('Order', {
    'order_id': fields.Integer(description='Order ID'),
    'sender_id': fields.Integer(description='Sender ID'),
    'sender_address': fields.String(description='Sender Address'),
    'sender_name': fields.String(description='Sender Name'),
    'receiver_id': fields.Integer(description='Receiver ID'),
    'receiver_name': fields.String(description='Receiver Name'),
    'receiver_address': fields.String(description='Receiver Address'),
    'receiver_phone': fields.String(description='Receiver Phone'),
    'order_date': fields.DateTime(description='Order Date'),
    'total_amount': fields.Float(description='Total Amount'),
    'shipment_type_id': fields.Integer(description='Shipment Type ID'),
    'items': fields.List(fields.Nested(order_item_schema))
})

shipment_type_schema = api.model('Shipment_Type', {
    'shipment_type_id': fields.Integer(description='Shipment Type ID'),
    'shipment_type_Name': fields.String(description='Shipment Type Name'),
    'description': fields.String(description='Description')
})
