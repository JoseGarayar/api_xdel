# Flask
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required
# App
from models import *
from schemas import *


def register_routes(api):
    # Namespaces
    ns_customer = api.namespace('customer', description = 'Endpoints for customer')
    ns_address = api.namespace('address', description = 'Endpoints for address')

    # Routes
        
    @ns_customer.route('/')
    class CustomerList(Resource):
        @jwt_required()
        @ns_customer.doc('list_customers')
        @ns_customer.marshal_list_with(output_customer_schema)
        def get(self):
            """List all customers"""
            return Customer.query.all()
        
        @jwt_required()
        @ns_customer.doc('create_customer')
        @ns_customer.expect(input_customer_schema)
        @ns_customer.marshal_with(output_customer_schema)
        def post(self):
            """Create a new customer"""
            data = request.json
            if Customer.query.filter_by(email = data['email']).first() is not None:
                ns_customer.abort(400, "Customer already exists")
            new_customer = Customer(type = data['type'],
                                    name = data['name'],
                                    email = data['email'],
                                    company = data['company'])
            db.session.add(new_customer)
            db.session.commit()
            return new_customer
   
    @ns_customer.route('/<int:customer_id>')
    @ns_customer.response(404, 'Customer not found')
    @ns_customer.param('customer_id', 'The customer identifier')
    class CustomerID(Resource):
        @jwt_required()
        @ns_customer.doc('get_customer')
        @ns_customer.marshal_with(output_customer_schema)
        def get(self, customer_id):
            """Fetch a customer given its identifier"""
            customer = Customer.query.get(customer_id)
            if not customer:
                ns_customer.abort(404, "Customer not found")
            return customer

        @jwt_required()
        @ns_customer.doc('delete_customer')
        @ns_customer.response(204, 'Customer deleted')
        def delete(self, customer_id):
            """Delete a customer given its identifier"""
            customer_to_delete = Customer.query.get(customer_id)
            if not customer_to_delete:
                ns_customer.abort(404, "Customer not found")
            db.session.delete(customer_to_delete)
            db.session.commit()
            return f"Customer with ID {customer_id} has been deleted.", 204
            
        @jwt_required()
        @ns_customer.doc('update_customer')
        @ns_customer.expect(input_customer_schema)
        @ns_customer.marshal_with(output_customer_schema)
        def put(self, customer_id):
            """Update a customer given its identifier"""
            data = request.json
            customer_to_update = Customer.query.get(customer_id)
            if customer_to_update:
                if Customer.query.filter_by(email = data['email']).first() is not None and customer_to_update.email != data['email']:
                    ns_customer.abort(400, "Customer already exists")
                customer_to_update.type = data['type']
                customer_to_update.name = data['name']
                customer_to_update.email = data['email']
                customer_to_update.company = data['company']
                db.session.commit()
                return customer_to_update
            ns_customer.abort(404, "Customer not found")


    @ns_address.route('/')
    class AddressList(Resource):
        @jwt_required()
        @ns_address.doc('list_address')
        @ns_address.marshal_list_with(output_address_schema)
        def get(self):
            """List all addresses"""
            return Address.query.all()
        
        @jwt_required()
        @ns_address.doc('create_address')
        @ns_address.expect(input_address_schema)
        @ns_address.marshal_with(output_address_schema)
        def post(self):
            """Create a new address"""
            data = request.json

            if Customer.query.get(data['customer_id']) is None:
                ns_address.abort(400, "Customer does not exist")

            new_address = Address(customer_id = data['customer_id'],
                                  address = data['address'],
                                  suburb = data['suburb'],
                                  city = data['city'],
                                  state = data['state'],
                                  country = data['country'])

            db.session.add(new_address)
            db.session.commit()
            return new_address

    @ns_address.route('/<int:address_id>')
    @ns_address.response(404, 'Address not found')
    @ns_address.param('address_id', 'The Address identifier')
    class AddressID(Resource):
        @jwt_required()
        @ns_address.doc('get_address')
        @ns_address.marshal_with(output_address_schema)
        def get(self, address_id):
            """Fetch an address given its identifier"""
            address = Address.query.get(address_id)
            if not address:
                ns_address.abort(404, "Address not found")
            return address

        @jwt_required()
        @ns_address.doc('delete_address')
        @ns_address.response(204, 'Address deleted')
        def delete(self, address_id):
            """Delete an address given its identifier"""
            address_to_delete = Address.query.get(address_id)
            if not address_to_delete:
                ns_address.abort(404, "Address not found")
            db.session.delete(address_to_delete)
            db.session.commit()
            return f"Address with ID {address_id} has been deleted.", 204
            
        @jwt_required()
        @ns_address.doc('update_address')
        @ns_address.expect(input_address_schema)
        @ns_address.marshal_with(output_address_schema)
        def put(self, address_id):
            """Update an address given its identifier"""
            data = request.json
            if Customer.query.get(data['customer_id']) is None:
                ns_address.abort(400, "Customer does not exist")
            address_to_update = Address.query.get(address_id)
            if address_to_update:
                address_to_update.customer_id = data['customer_id']
                address_to_update.address = data['address']
                address_to_update.suburb = data['suburb']
                address_to_update.city = data['city']
                address_to_update.state = data['state']
                address_to_update.country = data['country']
                db.session.commit()
                return address_to_update
            ns_address.abort(404, "Address not found")