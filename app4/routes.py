# Flask
from flask import request
from flask_restx import Resource
# App
from models import *
from schemas import *


def register_routes(api):
    # Namespaces
    ns_order = api.namespace('order', description='Order related operations')
    ns_shipment = api.namespace('shipment', description='Shipment related operations')
    ns_event = api.namespace('event', description='Event related operations')
    ns_shipment_status = api.namespace('shipment-status', description='Shipment Status related operations')

    # Test Namespace
    @api.route('/hello')
    class Hello(Resource):
        def get(self):
            """Return a simple message to any public requester."""
            return {'hello': 'world'}

    # Shipment Routes
    @ns_shipment.route('/')
    class ShipmentList(Resource):
        @api.marshal_list_with(shipment_schema)
        def get(self):
            """List all shipments"""
            return Shipment.query.all()

        @api.expect(shipment_schema)
        @api.marshal_with(shipment_schema)
        def post(self):
            """Create a new shipment"""
            new_shipment = Shipment(**request.json)
            db.session.add(new_shipment)
            db.session.commit()
            return new_shipment, 201

    @ns_shipment.route('/<int:shipment_id>')
    class ShipmentItem(Resource):
        @api.marshal_with(shipment_schema)
        def get(self, shipment_id):
            """Retrieve a specific shipment"""
            return Shipment.query.filter_by(shipment_id=shipment_id).first()

    # Event Routes
    @ns_event.route('/')
    class EventList(Resource):
        @api.marshal_list_with(event_schema)
        def get(self):
            """List all events"""
            return Event.query.all()

        @api.expect(event_schema)
        @api.marshal_with(event_schema)
        def post(self):
            """Create a new event"""
            new_event = Event(**request.json)
            db.session.add(new_event)
            db.session.commit()
            return new_event, 201

    @ns_event.route('/<int:event_id>')
    class EventItem(Resource):
        @api.marshal_with(event_schema)
        def get(self, event_id):
            """Retrieve a specific event"""
            return Event.query.filter_by(event_id=event_id).first()

    # Shipment Status Routes
    @ns_shipment_status.route('/')
    class ShipmentStatusList(Resource):
        @api.marshal_list_with(shipment_status_schema)
        def get(self):
            """List all shipment statuses"""
            return ShipmentStatus.query.all()

        @api.expect(shipment_status_schema)
        @api.marshal_with(shipment_status_schema)
        def post(self):
            """Create a new shipment status"""
            new_shipment_status = ShipmentStatus(**request.json)
            db.session.add(new_shipment_status)
            db.session.commit()
            return new_shipment_status, 201

    @ns_shipment_status.route('/<int:shipment_status_id>')
    class ShipmentStatusItem(Resource):
        
        @api.marshal_with(shipment_status_schema)
        def get(self, shipment_status_id):
            return ShipmentStatus.query.filter_by(shipment_status_id=shipment_status_id).first()
