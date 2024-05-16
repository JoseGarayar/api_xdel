# Flask
from flask import request
from flask_restx import Resource
from flask_jwt_extended import ( 
    create_access_token, 
    jwt_required, 
    get_jwt_identity
)
# App
from models import *
from schemas import *
from functions import (
    check_valid_password,
    hash_password
)



def register_routes(api):
    # Namespaces
    ns_test = api.namespace('', description='Endpoints for testing')
    ns_login = api.namespace('login', description='Endpoints for login')
    ns_users = api.namespace('users', description='User operations')

    ns_persons = api.namespace('persons', description='Person operations')
    ns_invoices = api.namespace('invoices', description='Invoice operations')
    ns_invoice_details = api.namespace('invoice_details', description='Invoice detail operations')
    ns_product_services = api.namespace('product_services', description='Product service operations')
    ns_couriers = api.namespace('couriers', description='Courier operations')
    ns_roles = api.namespace('roles', description='Role operations')
    ns_permissions = api.namespace('permissions', description='Permission operations')
    ns_role_permissions = api.namespace('role_permissions', description='Role permission operations')
    ns_user_roles = api.namespace('user_roles', description='User role operations')
    ns_shipments = api.namespace('shipments', description='Shipment operations')
    ns_shipment_states = api.namespace('shipment_states', description='Shipment state operations')

    # Routes
    @ns_test.route('/hello')
    class Hello(Resource):
        def get(self):
            """Return a simple message to any public requester."""
            return {'hello': 'world'}
        
    @ns_test.route('/protected')
    class Protected(Resource):
        @jwt_required()
        def get(self):
            """
            Provide the current logged-in user's identifier to authenticated requests. 
            It requires the requester to be authenticated.
            This endpoint is useful for verifying token validity and user authentication status.
            """
            current_user = get_jwt_identity()
            return {'logged_in_as': current_user}
    
    @ns_login.route('/')
    class Login(Resource):
        @ns_login.expect(login_schema)
        def post(self):
            """
            Authenticate a user based on email and password and return a JWT access token.
            """
            data = request.json
            email = data.get('email')
            password = data.get('password')
            if not email or not password:
                ns_login.abort(400, "Email and password are required")
            user = User.query.filter_by(email=email).first()
            if not user:
                ns_login.abort(400, "User with email provided doesn't exist")
            if check_valid_password(user.hashed_password, password):
                access_token = create_access_token(identity=user.email)
                return {
                    'message': 'Login successful', 
                    'access_token': access_token
                }
            ns_login.abort(400, "Invalid credentials")

    @ns_users.route('/')
    class UserList(Resource):
        @ns_users.doc('list_users')
        @ns_users.marshal_list_with(user_schema)
        def get(self):
            """List all users"""
            return User.query.all()
        
        @ns_users.doc('create_user')
        @ns_users.expect(login_schema)
        @ns_users.marshal_with(user_schema)
        def post(self):
            """Create a new user"""
            data = request.json
            if User.query.filter_by(email=data['email']).first() is not None:
                ns_users.abort(400, "Email already exists")
            new_user = User(
                email=data['email'], 
                hashed_password=hash_password(data['password'])
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        
    @ns_users.route('/<int:user_id>')
    @ns_users.response(404, 'User not found')
    @ns_users.param('user_id', 'The user identifier')
    class UserID(Resource):
        @ns_users.doc('get_user')
        @ns_users.marshal_with(user_schema)
        def get(self, user_id):
            """Fetch a user given its identifier"""
            user = User.query.get(user_id)
            if not user:
                ns_users.abort(404, "User not found")
            return user

        @ns_users.doc('delete_user')
        @ns_users.response(204, 'User deleted')
        def delete(self, user_id):
            """Delete a user given its identifier"""
            user_to_delete = User.query.get(user_id)
            if not user_to_delete:
                ns_users.abort(404, "User not found")
            db.session.delete(user_to_delete)
            db.session.commit()
            return f"User with ID {user_id} has been deleted.", 204
            

        @ns_users.doc('update_user')
        @ns_users.expect(login_schema)
        @ns_users.marshal_with(user_schema)
        def put(self, user_id):
            """Update a user given its identifier"""
            data = request.json
            user_to_update = User.query.get(user_id)
            if user_to_update:
                user_to_update.email = data['email']
                user_to_update.hashed_password = hash_password(data['password'])
                db.session.commit()
                return user_to_update
            ns_users.abort(404, "User not found")

    # Routes for Person
    @ns_persons.route('/')
    class PersonList(Resource):
        @ns_persons.doc('list_persons')
        @ns_persons.marshal_list_with(output_person_schema)
        def get(self):
            """List all persons"""
            return Person.query.all()
    
        @ns_persons.doc('create_person')
        @ns_persons.expect(input_person_schema)
        @ns_persons.marshal_with(output_person_schema)
        def post(self):
            """Create a new person"""
            data = request.json
            new_person = Person(
                name=data['name'], 
                address=data['address'],
                contact_level=data['contact_level']
            )
            db.session.add(new_person)
            db.session.commit()
            return new_person
    
    @ns_persons.route('/<int:person_id>')
    @ns_persons.response(404, 'Person not found')
    @ns_persons.param('person_id', 'The person identifier')
    class PersonID(Resource):
        @ns_persons.doc('get_person')
        @ns_persons.marshal_with(output_person_schema)
        def get(self, person_id):
            """Fetch a person given its identifier"""
            person = Person.query.get(person_id)
            if not person:
                ns_persons.abort(404, "Person not found")
            return person

        @ns_persons.doc('delete_person')
        @ns_persons.response(204, 'Person deleted')
        def delete(self, person_id):
            """Delete a person given its identifier"""
            person_to_delete = Person.query.get(person_id)
            if not person_to_delete:
                ns_persons.abort(404, "Person not found")
            db.session.delete(person_to_delete)
            db.session.commit()
            return f"Person with ID {person_id} has been deleted.", 204

        @ns_persons.doc('update_person')
        @ns_persons.expect(input_person_schema)
        @ns_persons.marshal_with(output_person_schema)
        def put(self, person_id):
            """Update a person given its identifier"""
            data = request.json
            person_to_update = Person.query.get(person_id)
            if person_to_update:
                person_to_update.name = data['name']
                person_to_update.address = data['address']
                person_to_update.contact_level = data['contact_level']
                db.session.commit()
                return person_to_update
            ns_persons.abort(404, "Person not found")

    # Routes for Invoice
    @ns_invoices.route('/')
    class InvoiceList(Resource):
        @ns_invoices.doc('list_invoices')
        @ns_invoices.marshal_list_with(output_invoice_schema)
        def get(self):
            """List all invoices"""
            return Invoice.query.all()
    
        @ns_invoices.doc('create_invoice')
        @ns_invoices.expect(input_invoice_schema)
        @ns_invoices.marshal_with(output_invoice_schema)
        def post(self):
            """Create a new invoice"""
            data = request.json
            id_sender = data['id_sender']
            id_recipient = data['id_recipient']
            id_product = data['id_product']
            id_user = data['id_user']

            if not Person.query.get(id_sender):
                ns_invoices.abort(404, "Sender not found")

            if not Person.query.get(id_recipient):
                ns_invoices.abort(404, "Recipient not found")

            if not ProductService.query.get(id_product):
                ns_invoices.abort(404, "Product not found")

            if not User.query.get(id_user):
                ns_invoices.abort(404, "User not found")
            
            
            new_invoice = Invoice(
                id_sender=data['id_sender'], 
                id_recipient=data['id_recipient'],
                id_product=data['id_product'],
                date=data['date'],
                total_amount=data['total_amount'],
                id_user=data['id_user']
        )
            db.session.add(new_invoice)
            db.session.commit()
            return new_invoice
    
    @ns_invoices.route('/<int:invoice_id>')
    @ns_invoices.response(404, 'Invoice not found')
    @ns_invoices.param('invoice_id', 'The invoice identifier')
    class InvoiceID(Resource):
        @ns_invoices.doc('get_invoice')
        @ns_invoices.marshal_with(output_invoice_schema)
        def get(self, invoice_id):
            """Fetch an invoice given its identifier"""
            invoice = Invoice.query.get(invoice_id)
            if not invoice:
                ns_invoices.abort(404, "Invoice not found")
            return invoice

        @ns_invoices.doc('delete_invoice')
        @ns_invoices.response(204, 'Invoice deleted')
        def delete(self, invoice_id):
            """Delete an invoice given its identifier"""
            invoice_to_delete = Invoice.query.get(invoice_id)
            if not invoice_to_delete:
                ns_invoices.abort(404, "Invoice not found")
            db.session.delete(invoice_to_delete)
            db.session.commit()
            return f"Invoice with ID {invoice_id} has been deleted.", 204

        @ns_invoices.doc('update_invoice')
        @ns_invoices.expect(input_invoice_schema)
        @ns_invoices.marshal_with(output_invoice_schema)
        def put(self, invoice_id):
            """Update an invoice given its identifier"""
            data = request.json
            invoice_to_update = Invoice.query.get(invoice_id)
            if invoice_to_update:
                invoice_to_update.id_sender = data['id_sender']
                invoice_to_update.id_recipient = data['id_recipient']
                invoice_to_update.id_product = data['id_product']
                invoice_to_update.date = data['date']
                invoice_to_update.total_amount = data['total_amount']
                invoice_to_update.id_user = data['id_user']
                db.session.commit()
                return invoice_to_update
            ns_invoices.abort(404, "Invoice not found")