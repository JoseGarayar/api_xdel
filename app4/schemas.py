from flask_restx import fields
from __init__ import api


event_schema = api.model('Event', {
    'event_id': fields.Integer(description='Event ID'),
    'shipment_id': fields.Integer(description='Shipment ID'),
    'shipment_status_id': fields.Integer(description='Shipment Status ID'),
    'event_date': fields.DateTime(description='Event Date'),
    'comment': fields.String(description='Comment')
})


event_schema_input = api.model('Event', {    
    'shipment_id': fields.Integer(description='Shipment ID'),
    'shipment_status_id': fields.Integer(description='Shipment Status ID'),
    'comment': fields.String(description='Comment')
})


shipment_schema = api.model('Shipment', {
    'shipment_id': fields.Integer(description='Shipment ID'),
    'tracking_number': fields.String(description='Tracking Number'),
    'order_id': fields.Integer(description='Order ID'),
    'shipping_type': fields.String(description='Shipping Type'),
    'sender_name': fields.String(description='Sender Name'),
    'sender_address': fields.String(description='Sender Address'),
    'receiver_name': fields.String(description='Receiver Name'),
    'receiver_address': fields.String(description='Receiver Address'),
    'shipment_status_id': fields.Integer(description='Shipment Status'),
    'shipment_date': fields.DateTime(description='Shipment Date'),
    'delivery_date': fields.DateTime(description='Delivery Date'),
    'estimated_delivery_date': fields.DateTime(description='Estimated Delivery Date'),
    'actual_delivery_date': fields.DateTime(description='Actual Delivery Date'),
    'events': fields.List(fields.Nested(event_schema))

})

shipment_schema_input = api.model('Shipment', {
    'tracking_number': fields.String(description='Tracking Number'),
    'order_id': fields.Integer(description='Order ID'),
    'shipping_type': fields.String(description='Shipping Type'),
    'sender_name': fields.String(description='Sender Name'),
    'sender_address': fields.String(description='Sender Address'),
    'receiver_name': fields.String(description='Receiver Name'),
    'receiver_address': fields.String(description='Receiver Address'),
    'shipment_status_id': fields.Integer(description='Shipment Status'),
    'shipment_date': fields.DateTime(description='Shipment Date'),
    'delivery_date': fields.DateTime(description='Delivery Date'),
    'estimated_delivery_date': fields.DateTime(description='Estimated Delivery Date'),
})






shipment_status_schema = api.model('ShipmentStatus', {
    'shipment_status_id': fields.Integer(description='Shipment Status ID'),
    'shipment_status_name': fields.String(description='Shipment Status Name')
})


shipment_status_schema_input = api.model('ShipmentStatus', {    
    'shipment_status_name': fields.String(description='Shipment Status Name')
})
