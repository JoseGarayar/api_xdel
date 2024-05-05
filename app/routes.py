# Flask
from flask import request
from flask_restx import Resource
from flask_jwt_extended import ( 
    create_access_token, 
    jwt_required, 
    get_jwt_identity
)
# App
from app.models import *
from app.schemas import *
from app.functions import (
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

    # Routes for InvoiceDetail
    @ns_invoice_details.route('/')
    class InvoiceDetailList(Resource):
        @ns_invoice_details.doc('list_invoice_details')
        @ns_invoice_details.marshal_list_with(output_invoice_detail_schema)
        def get(self):
            """List all invoice details"""
            return InvoiceDetail.query.all()
    
        @ns_invoice_details.doc('create_invoice_detail')
        @ns_invoice_details.expect(input_invoice_detail_schema)
        @ns_invoice_details.marshal_with(output_invoice_detail_schema)
        def post(self):
            """Create a new invoice detail"""
            data = request.json
            new_invoice_detail = InvoiceDetail(
                id_invoice=data['id_invoice'], 
                package_type=data['package_type'],
                dimensions=data['dimensions'],
                weight=data['weight'],
                quantity=data['quantity'],
                unit_price=data['unit_price'],
                subtotal=data['subtotal']
            )
            db.session.add(new_invoice_detail)
            db.session.commit()
            return new_invoice_detail
    
    @ns_invoice_details.route('/<int:detail_id>')
    @ns_invoice_details.response(404, 'Invoice detail not found')
    @ns_invoice_details.param('detail_id', 'The invoice detail identifier')
    class InvoiceDetailID(Resource):
        @ns_invoice_details.doc('get_invoice_detail')
        @ns_invoice_details.marshal_with(output_invoice_detail_schema)
        def get(self, detail_id):
            """Fetch an invoice detail given its identifier"""
            detail = InvoiceDetail.query.get(detail_id)
            if not detail:
                ns_invoice_details.abort(404, "Invoice detail not found")
            return detail

        @ns_invoice_details.doc('delete_invoice_detail')
        @ns_invoice_details.response(204, 'Invoice detail deleted')
        def delete(self, detail_id):
            """Delete an invoice detail given its identifier"""
            detail_to_delete = InvoiceDetail.query.get(detail_id)
            if not detail_to_delete:
                ns_invoice_details.abort(404, "Invoice detail not found")
            db.session.delete(detail_to_delete)
            db.session.commit()
            return f"Invoice detail with ID {detail_id} has been deleted.", 204

        @ns_invoice_details.doc('update_invoice_detail')
        @ns_invoice_details.expect(input_invoice_detail_schema)
        @ns_invoice_details.marshal_with(output_invoice_detail_schema)
        def put(self, detail_id):
            """Update an invoice detail given its identifier"""
            data = request.json
            detail_to_update = InvoiceDetail.query.get(detail_id)
            if detail_to_update:
                detail_to_update.id_invoice = data['id_invoice']
                detail_to_update.package_type = data['package_type']
                detail_to_update.dimensions = data['dimensions']
                detail_to_update.weight = data['weight']
                detail_to_update.quantity = data['quantity']
                detail_to_update.unit_price = data['unit_price']
                detail_to_update.subtotal = data['subtotal']
                db.session.commit()
                return detail_to_update
            ns_invoice_details.abort(404, "Invoice detail not found")


    # Routes for ProductService
    @ns_product_services.route('/')
    class ProductServiceList(Resource):
        @ns_product_services.doc('list_product_services')
        @ns_product_services.marshal_list_with(output_product_service_schema)
        def get(self):
            """List all product services"""
            return ProductService.query.all()

        @ns_product_services.doc('create_product_service')
        @ns_product_services.expect(input_product_service_schema)
        @ns_product_services.marshal_with(output_product_service_schema)
        def post(self):
            """Create a new product service"""
            data = request.json
            new_product_service = ProductService(
                name=data['name'],
                description=data['description'],
                price=data['price']
            )
            db.session.add(new_product_service)
            db.session.commit()
            return new_product_service

    @ns_product_services.route('/<int:product_service_id>')
    @ns_product_services.response(404, 'Product service not found')
    @ns_product_services.param('product_service_id', 'The product service identifier')
    class ProductServiceID(Resource):
        @ns_product_services.doc('get_product_service')
        @ns_product_services.marshal_with(output_product_service_schema)
        def get(self, product_service_id):
            """Fetch a product service given its identifier"""
            product_service = ProductService.query.get(product_service_id)
            if not product_service:
                ns_product_services.abort(404, "Product service not found")
            return product_service

        @ns_product_services.doc('delete_product_service')
        @ns_product_services.response(204, 'Product service deleted')
        def delete(self, product_service_id):
            """Delete a product service given its identifier"""
            product_service_to_delete = ProductService.query.get(product_service_id)
            if not product_service_to_delete:
                ns_product_services.abort(404, "Product service not found")
            db.session.delete(product_service_to_delete)
            db.session.commit()
            return f"Product service with ID {product_service_id} has been deleted.", 204

        @ns_product_services.doc('update_product_service')
        @ns_product_services.expect(input_product_service_schema)
        @ns_product_services.marshal_with(output_product_service_schema)
        def put(self, product_service_id):
            """Update a product service given its identifier"""
            data = request.json
            product_service_to_update = ProductService.query.get(product_service_id)
            if product_service_to_update:
                product_service_to_update.name = data['name']
                product_service_to_update.description = data['description']
                product_service_to_update.price = data['price']
                db.session.commit()
                return product_service_to_update
            ns_product_services.abort(404, "Product service not found")


    # Routes for Courier
    @ns_couriers.route('/')
    class CourierList(Resource):
        @ns_couriers.doc('list_couriers')
        @ns_couriers.marshal_list_with(output_courier_schema)
        def get(self):
            """List all couriers"""
            return Courier.query.all()

        @ns_couriers.doc('create_courier')
        @ns_couriers.expect(input_courier_schema)
        @ns_couriers.marshal_with(output_courier_schema)
        def post(self):
            """Create a new courier"""
            data = request.json
            new_courier = Courier(
                name=data['name'],
                address=data['address']
            )
            db.session.add(new_courier)
            db.session.commit()
            return new_courier

    @ns_couriers.route('/<int:courier_id>')
    @ns_couriers.response(404, 'Courier not found')
    @ns_couriers.param('courier_id', 'The courier identifier')
    class CourierID(Resource):
        @ns_couriers.doc('get_courier')
        @ns_couriers.marshal_with(output_courier_schema)
        def get(self, courier_id):
            """Fetch a courier given its identifier"""
            courier = Courier.query.get(courier_id)
            if not courier:
                ns_couriers.abort(404, "Courier not found")
            return courier

        @ns_couriers.doc('delete_courier')
        @ns_couriers.response(204, 'Courier deleted')
        def delete(self, courier_id):
            """Delete a courier given its identifier"""
            courier_to_delete = Courier.query.get(courier_id)
            if not courier_to_delete:
                ns_couriers.abort(404, "Courier not found")
            db.session.delete(courier_to_delete)
            db.session.commit()
            return f"Courier with ID {courier_id} has been deleted.", 204

        @ns_couriers.doc('update_courier')
        @ns_couriers.expect(input_courier_schema)
        @ns_couriers.marshal_with(output_courier_schema)
        def put(self, courier_id):
            """Update a courier given its identifier"""
            data = request.json
            courier_to_update = Courier.query.get(courier_id)
            if courier_to_update:
                courier_to_update.name = data['name']
                courier_to_update.address = data['address']
                db.session.commit()
                return courier_to_update
            ns_couriers.abort(404, "Courier not found")

    # Routes for Role
    @ns_roles.route('/')
    class RoleList(Resource):
        @ns_roles.doc('list_roles')
        @ns_roles.marshal_list_with(output_role_schema)
        def get(self):
            """List all roles"""
            return Role.query.all()

        @ns_roles.doc('create_role')
        @ns_roles.expect(input_role_schema)
        @ns_roles.marshal_with(output_role_schema)
        def post(self):
            """Create a new role"""
            data = request.json
            new_role = Role(
                role_name=data['role_name'],
                description=data['description']
            )
            db.session.add(new_role)
            db.session.commit()
            return new_role

    @ns_roles.route('/<int:role_id>')
    @ns_roles.response(404, 'Role not found')
    @ns_roles.param('role_id', 'The role identifier')
    class RoleID(Resource):
        @ns_roles.doc('get_role')
        @ns_roles.marshal_with(output_role_schema)
        def get(self, role_id):
            """Fetch a role given its identifier"""
            role = Role.query.get(role_id)
            if not role:
                ns_roles.abort(404, "Role not found")
            return role

        @ns_roles.doc('delete_role')
        @ns_roles.response(204, 'Role deleted')
        def delete(self, role_id):
            """Delete a role given its identifier"""
            role_to_delete = Role.query.get(role_id)
            if not role_to_delete:
                ns_roles.abort(404, "Role not found")
            db.session.delete(role_to_delete)
            db.session.commit()
            return f"Role with ID {role_id} has been deleted.", 204

        @ns_roles.doc('update_role')
        @ns_roles.expect(input_role_schema)
        @ns_roles.marshal_with(output_role_schema)
        def put(self, role_id):
            """Update a role given its identifier"""
            data = request.json
            role_to_update = Role.query.get(role_id)
            if role_to_update:
                role_to_update.role_name = data['role_name']
                role_to_update.description = data['description']
                db.session.commit()
                return role_to_update
            ns_roles.abort(404, "Role not found")

    # Routes for Permission
    @ns_permissions.route('/')
    class PermissionList(Resource):
        @ns_permissions.doc('list_permissions')
        @ns_permissions.marshal_list_with(output_permission_schema)
        def get(self):
            """List all permissions"""
            return Permission.query.all()

        @ns_permissions.doc('create_permission')
        @ns_permissions.expect(input_permission_schema)
        @ns_permissions.marshal_with(output_permission_schema)
        def post(self):
            """Create a new permission"""
            data = request.json
            new_permission = Permission(
                permission_name=data['permission_name'],
                description=data['description']
            )
            db.session.add(new_permission)
            db.session.commit()
            return new_permission

    @ns_permissions.route('/<int:permission_id>')
    @ns_permissions.response(404, 'Permission not found')
    @ns_permissions.param('permission_id', 'The permission identifier')
    class PermissionID(Resource):
        @ns_permissions.doc('get_permission')
        @ns_permissions.marshal_with(output_permission_schema)
        def get(self, permission_id):
            """Fetch a permission given its identifier"""
            permission = Permission.query.get(permission_id)
            if not permission:
                ns_permissions.abort(404, "Permission not found")
            return permission

        @ns_permissions.doc('delete_permission')
        @ns_permissions.response(204, 'Permission deleted')
        def delete(self, permission_id):
            """Delete a permission given its identifier"""
            permission_to_delete = Permission.query.get(permission_id)
            if not permission_to_delete:
                ns_permissions.abort(404, "Permission not found")
            db.session.delete(permission_to_delete)
            db.session.commit()
            return f"Permission with ID {permission_id} has been deleted.", 204

        @ns_permissions.doc('update_permission')
        @ns_permissions.expect(input_permission_schema)
        @ns_permissions.marshal_with(output_permission_schema)
        def put(self, permission_id):
            """Update a permission given its identifier"""
            data = request.json
            permission_to_update = Permission.query.get(permission_id)
            if permission_to_update:
                permission_to_update.permission_name = data['permission_name']
                permission_to_update.description = data['description']
                db.session.commit()
                return permission_to_update
            ns_permissions.abort(404, "Permission not found")

    # Routes for RolePermission
    @ns_role_permissions.route('/')
    class RolePermissionList(Resource):
        @ns_role_permissions.doc('list_role_permissions')
        @ns_role_permissions.marshal_list_with(output_role_permission_schema)
        def get(self):
            """List all role permissions"""
            return RolePermission.query.all()

        @ns_role_permissions.doc('create_role_permission')
        @ns_role_permissions.expect(input_role_permission_schema)
        @ns_role_permissions.marshal_with(output_role_permission_schema)
        def post(self):
            """Create a new role permission"""
            data = request.json
            new_role_permission = RolePermission(
                id_role=data['id_role'],
                id_permission=data['id_permission']
            )
            db.session.add(new_role_permission)
            db.session.commit()
            return new_role_permission

    @ns_role_permissions.route('/<int:role_id>/<int:permission_id>')
    @ns_role_permissions.response(404, 'Role permission not found')
    @ns_role_permissions.param('role_id', 'The role identifier')
    @ns_role_permissions.param('permission_id', 'The permission identifier')
    class RolePermissionID(Resource):
        @ns_role_permissions.doc('get_role_permission')
        @ns_role_permissions.marshal_with(output_role_permission_schema)
        def get(self, role_id, permission_id):
            """Fetch a role permission given its identifiers"""
            role_permission = RolePermission.query.filter_by(id_role=role_id, id_permission=permission_id).first()
            if not role_permission:
                ns_role_permissions.abort(404, "Role permission not found")
            return role_permission

        @ns_role_permissions.doc('delete_role_permission')
        @ns_role_permissions.response(204, 'Role permission deleted')
        def delete(self, role_id, permission_id):
            """Delete a role permission given its identifiers"""
            role_permission_to_delete = RolePermission.query.filter_by(id_role=role_id, id_permission=permission_id).first()
            if not role_permission_to_delete:
                ns_role_permissions.abort(404, "Role permission not found")
            db.session.delete(role_permission_to_delete)
            db.session.commit()
            return f"Role permission with Role ID {role_id} and Permission ID {permission_id} has been deleted.", 204

    # Routes for UserRole
    @ns_user_roles.route('/')
    class UserRoleList(Resource):
        @ns_user_roles.doc('list_user_roles')
        @ns_user_roles.marshal_list_with(output_user_role_schema)
        def get(self):
            """List all user roles"""
            return UserRole.query.all()

        @ns_user_roles.doc('create_user_role')
        @ns_user_roles.expect(input_user_role_schema)
        @ns_user_roles.marshal_with(output_user_role_schema)
        def post(self):
            """Create a new user role"""
            data = request.json
            new_user_role = UserRole(
                id_user=data['id_user'],
                id_role=data['id_role']
            )
            db.session.add(new_user_role)
            db.session.commit()
            return new_user_role

    @ns_user_roles.route('/<int:user_id>/<int:role_id>')
    @ns_user_roles.response(404, 'User role not found')
    @ns_user_roles.param('user_id', 'The user identifier')
    @ns_user_roles.param('role_id', 'The role identifier')
    class UserRoleID(Resource):
        @ns_user_roles.doc('get_user_role')
        @ns_user_roles.marshal_with(output_user_role_schema)
        def get(self, user_id, role_id):
            """Fetch a user role given its identifiers"""
            user_role = UserRole.query.filter_by(id_user=user_id, id_role=role_id).first()
            if not user_role:
                ns_user_roles.abort(404, "User role not found")
            return user_role

        @ns_user_roles.doc('delete_user_role')
        @ns_user_roles.response(204, 'User role deleted')
        def delete(self, user_id, role_id):
            """Delete a user role given its identifiers"""
            user_role_to_delete = UserRole.query.filter_by(id_user=user_id, id_role=role_id).first()
            if not user_role_to_delete:
                ns_user_roles.abort(404, "User role not found")
            db.session.delete(user_role_to_delete)
            db.session.commit()
            return f"User role with User ID {user_id} and Role ID {role_id} has been deleted.", 204

    # Routes for Shipment
    @ns_shipments.route('/')
    class ShipmentList(Resource):
        @ns_shipments.doc('list_shipments')
        @ns_shipments.marshal_list_with(output_shipment_schema)
        def get(self):
            """List all shipments"""
            return Shipment.query.all()

        @ns_shipments.doc('create_shipment')
        @ns_shipments.expect(input_shipment_schema)
        @ns_shipments.marshal_with(output_shipment_schema)
        def post(self):
            """Create a new shipment"""
            data = request.json
            new_shipment = Shipment(
                id_invoice=data['id_invoice'],
                id_courier=data['id_courier'],
                id_shipment_state=data['id_shipment_state'],
                creation_date=data['creation_date'],
                finish_date=data['finish_date']
            )
            db.session.add(new_shipment)
            db.session.commit()
            return new_shipment

    @ns_shipments.route('/<int:shipment_id>')
    @ns_shipments.response(404, 'Shipment not found')
    @ns_shipments.param('shipment_id', 'The shipment identifier')
    class ShipmentID(Resource):
        @ns_shipments.doc('get_shipment')
        @ns_shipments.marshal_with(output_shipment_schema)
        def get(self, shipment_id):
            """Fetch a shipment given its identifier"""
            shipment = Shipment.query.get(shipment_id)
            if not shipment:
                ns_shipments.abort(404, "Shipment not found")
            return shipment

        @ns_shipments.doc('delete_shipment')
        @ns_shipments.response(204, 'Shipment deleted')
        def delete(self, shipment_id):
            """Delete a shipment given its identifier"""
            shipment_to_delete = Shipment.query.get(shipment_id)
            if not shipment_to_delete:
                ns_shipments.abort(404, "Shipment not found")
            db.session.delete(shipment_to_delete)
            db.session.commit()
            return f"Shipment with ID {shipment_id} has been deleted.", 204

        @ns_shipments.doc('update_shipment')
        @ns_shipments.expect(input_shipment_schema)
        @ns_shipments.marshal_with(output_shipment_schema)
        def put(self, shipment_id):
            """Update a shipment given its identifier"""
            data = request.json
            shipment_to_update = Shipment.query.get(shipment_id)
            if shipment_to_update:
                shipment_to_update.id_invoice = data['id_invoice']
                shipment_to_update.id_courier = data['id_courier']
                shipment_to_update.id_shipment_state = data['id_shipment_state']
                shipment_to_update.creation_date = data['creation_date']
                shipment_to_update.finish_date = data['finish_date']
                db.session.commit()
                return shipment_to_update
            ns_shipments.abort(404, "Shipment not found")

    # Routes for ShipmentState
    @ns_shipment_states.route('/')
    class ShipmentStateList(Resource):
        @ns_shipment_states.doc('list_shipment_states')
        @ns_shipment_states.marshal_list_with(output_shipment_state_schema)
        def get(self):
            """List all shipment states"""
            return ShipmentState.query.all()

        @ns_shipment_states.doc('create_shipment_state')
        @ns_shipment_states.expect(input_shipment_state_schema)
        @ns_shipment_states.marshal_with(output_shipment_state_schema)
        def post(self):
            """Create a new shipment state"""
            data = request.json
            new_shipment_state = ShipmentState(
                state_name=data['state_name']
            )
            db.session.add(new_shipment_state)
            db.session.commit()
            return new_shipment_state

    @ns_shipment_states.route('/<int:shipment_state_id>')
    @ns_shipment_states.response(404, 'Shipment state not found')
    @ns_shipment_states.param('shipment_state_id', 'The shipment state identifier')
    class ShipmentStateID(Resource):
        @ns_shipment_states.doc('get_shipment_state')
        @ns_shipment_states.marshal_with(output_shipment_state_schema)
        def get(self, shipment_state_id):
            """Fetch a shipment state given its identifier"""
            shipment_state = ShipmentState.query.get(shipment_state_id)
            if not shipment_state:
                ns_shipment_states.abort(404, "Shipment state not found")
            return shipment_state

        @ns_shipment_states.doc('delete_shipment_state')
        @ns_shipment_states.response(204, 'Shipment state deleted')
        def delete(self, shipment_state_id):
            """Delete a shipment state given its identifier"""
            shipment_state_to_delete = ShipmentState.query.get(shipment_state_id)
            if not shipment_state_to_delete:
                ns_shipment_states.abort(404, "Shipment state not found")
            db.session.delete(shipment_state_to_delete)
            db.session.commit()
            return f"Shipment state with ID {shipment_state_id} has been deleted.", 204

        @ns_shipment_states.doc('update_shipment_state')
        @ns_shipment_states.expect(input_shipment_state_schema)
        @ns_shipment_states.marshal_with(output_shipment_state_schema)
        def put(self, shipment_state_id):
            """Update a shipment state given its identifier"""
            data = request.json
            shipment_state_to_update = ShipmentState.query.get(shipment_state_id)
            if shipment_state_to_update:
                shipment_state_to_update.state_name = data['state_name']
                db.session.commit()
                return shipment_state_to_update
            ns_shipment_states.abort(404, "Shipment state not found")