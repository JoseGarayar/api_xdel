# Flask
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required
# App
from models import *
from schemas import *
from datetime import datetime

def register_routes(api):
    # Namespaces
    ns_shipment = api.namespace('shipment', description='Shipment related operations')
    ns_event = api.namespace('event', description='Event related operations')
    ns_shipment_status = api.namespace('shipment-status', description='Shipment Status related operations')


    # Shipment Routes
    @ns_shipment.route('/')
    class ShipmentList(Resource):
        @jwt_required()
        @api.marshal_list_with(shipment_schema)
        def get(self):
            """List all shipments"""
            return Shipment.query.all()

        @jwt_required()
        @api.expect(shipment_schema_input)
        @api.marshal_with(shipment_schema)
        def post(self):
            """Create a new shipment"""
            new_shipment = Shipment(**request.json)
            db.session.add(new_shipment)
            db.session.commit()
            return new_shipment, 201
        
        
    @ns_shipment.route('/<int:shipment_id>')
    class ShipmentItem(Resource):
        @jwt_required()
        @api.marshal_with(shipment_schema)
        def get(self, shipment_id):
            """Retrieve a specific shipment by shipment ID"""
            shipment = Shipment.query.get(shipment_id)
            if not shipment:
                ns_shipment.abort(404, "Shipment not found")
            return shipment


    @ns_shipment.route('/<string:tracking_number>')
    class ShipmentItemTracking(Resource):
        @jwt_required()
        @api.marshal_with(shipment_schema)
        def get(self, tracking_number):
            """Retrieve a specific shipment by tracking number"""
            shipment = Shipment.query.filter(Shipment.tracking_number.ilike(f'%{tracking_number}%')).first()
            if not shipment:
                ns_shipment.abort(404, "Shipment with tracking number provided not found")
            return shipment


    # Event Routes
    @ns_event.route('/')
    class EventList(Resource):
        @jwt_required()
        @api.marshal_list_with(event_schema)
        def get(self):
            """List all events"""
            return Event.query.all()
        
        @jwt_required()
        @api.doc('register_an_event')
        @api.expect(event_schema_input)
        @api.marshal_with(event_schema)
        def post(self):
            """Create a new event"""

            data = request.json
            # Obtener el envío
            shipment = Shipment.query.get(data['shipment_id'])
            
            if shipment:
                # Crear un nuevo evento
                new_event = Event(
                    shipment_id=data['shipment_id'],
                    shipment_status_id=data['shipment_status_id'],
                    event_date= datetime.now(),  # Usar la fecha y hora actual como fecha del evento
                    comment=data['comment']
                )
                db.session.add(new_event)
                
                # Actualizar el estado del envío y la fecha de entrega actual (si es necesario)
                shipment.shipment_status_id = data['shipment_status_id']
                if data['shipment_status_id'] == 4:  # 4 es el ID para "Delivered"
                    shipment.actual_delivery_date = datetime.now()
                
                db.session.commit()
                return new_event                    
            else:
                api.abort(404, "Shipment not found")
            

    @ns_event.route('/<int:event_id>')
    class EventItem(Resource):
        @jwt_required()
        @api.marshal_with(event_schema)
        def get(self, event_id):
            """Retrieve a specific event"""
            event = Event.query.get(event_id)
            if not event:
                ns_shipment.abort(404, "Event not found")
            return event


    # Shipment Status Routes
    @ns_shipment_status.route('/')
    class ShipmentStatusList(Resource):
        @jwt_required()
        @api.marshal_list_with(shipment_status_schema)
        def get(self):
            """List all shipment statuses"""
            return ShipmentStatus.query.all()

        @jwt_required()
        @api.expect(shipment_status_schema_input)
        @api.marshal_with(shipment_status_schema)
        def post(self):
            """Create a new shipment status"""
            new_shipment_status = ShipmentStatus(**request.json)
            db.session.add(new_shipment_status)
            db.session.commit()
            return new_shipment_status, 201


    @ns_shipment_status.route('/<int:shipment_status_id>')
    class ShipmentStatusItem(Resource):
        @jwt_required()
        @api.marshal_with(shipment_status_schema)
        def get(self, shipment_status_id):
            shipment_status = ShipmentStatus.query.get(shipment_status_id)
            if not shipment_status:
                ns_shipment.abort(404, "Shipment status not found")
            return shipment_status
