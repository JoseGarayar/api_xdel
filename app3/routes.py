# Flask
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required
# App
from models import *
from schemas import *


def register_routes(api):
    # Namespaces
    ns_order = api.namespace('order', description='Order related operations')
    ns_shipment = api.namespace('shipment-type', description='Shipment Type related operations')

    # Routes
    @ns_order.route('/')
    class OrderList(Resource):
        @jwt_required()
        @api.marshal_list_with(order_schema)
        def get(self):
            """List all orders without items"""
            return Order.query.all()

    @ns_order.route('/<int:id>')
    class OrderDetail(Resource):
        @jwt_required()
        @api.marshal_with(order_schema)
        def get(self, id):
            """Get an order by its ID with items"""
            order = Order.query.get(id)
            if not order:
                ns_order.abort(404, "Order not found")
            return order

    @ns_order.route('/search/<string:sender_name>')
    class OrderBySenderName(Resource):
        @jwt_required()
        @api.marshal_list_with(order_schema)
        def get(self, sender_name):
            """Search orders by SenderName"""
            return Order.query.filter(Order.sender_name.ilike(f'%{sender_name}%')).all()

    @ns_order.route('/create')
    class CreateOrder(Resource):
        @jwt_required()
        @api.doc('create_order')
        @api.expect(order_schema_input)
        @api.marshal_with(order_schema)
        def post(self):
            """Create a new order with items"""
            data = request.json
            order_items = data.pop('items', [])
            new_order = Order(**data)
            for item_data in order_items:
                new_item = OrderItem(**item_data)
                new_order.items.append(new_item)
            db.session.add(new_order)
            db.session.commit()
            return new_order, 201

    
    @ns_shipment.route('/')
    class ShipmentTypeCreate(Resource):
        @jwt_required()
        @api.marshal_list_with(shipment_type_schema)
        def get(self):
            """List all shipment types"""
            return ShipmentType.query.all()
        
        @jwt_required()
        @api.doc('Create_Shipment_Type')
        @api.expect(shipment_type_schema_input)
        @api.marshal_with(shipment_type_schema)
        def post(self):
            """
            Create a new shipment type.
            """
            data = request.json
            new_shipment_type = ShipmentType(
                shipment_type_name=data['shipment_type_name'],
                description=data['description']
            )
            db.session.add(new_shipment_type)
            db.session.commit()
            return new_shipment_type
        

    @ns_shipment.route('/<int:shipment_type_id>')
    class ShipmentStatusItem(Resource):
        @jwt_required()
        @api.marshal_with(shipment_type_schema)
        def get(self, shipment_type_id):
            """Retrieve a specific shipment status"""
            shipment_type = ShipmentType.query.get(shipment_type_id)
            if not shipment_type:
                ns_order.abort(404, "Shipment type not found")
            return ShipmentType.query.filter_by(shipment_type_id=shipment_type_id).first()