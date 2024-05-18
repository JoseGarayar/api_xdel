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
    # ns_test = api.namespace('', description='Endpoints for testing')
    ns_login = api.namespace('login', description='Endpoints for login')
    ns_users = api.namespace('users', description='User operations')
    ns_roles = api.namespace('roles', description='User roles')
    ns_logs = api.namespace('logs', description='User logs')
    ns_access_controls = api.namespace('access_controls', description='User access controls')

    # Routes
    # @ns_test.route('/hello')
    # class Hello(Resource):
    #     def get(self):
    #         """Return a simple message to any public requester."""
    #         return {'hello': 'world'}
        
    # @ns_test.route('/protected')
    # class Protected(Resource):
    #     @jwt_required()
    #     def get(self):
    #         """
    #         Provide the current logged-in user's identifier to authenticated requests. 
    #         It requires the requester to be authenticated.
    #         This endpoint is useful for verifying token validity and user authentication status.
    #         """
    #         current_user = get_jwt_identity()
    #         return {'logged_in_as': current_user}
    
    @ns_login.route('/')
    class Login(Resource):
        @ns_login.expect(login_schema)
        def post(self):
            """
            Authenticate a user based on username and password and return a JWT access token.
            """
            data = request.json
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                ns_login.abort(400, "Username and password are required")
            user = User.query.filter_by(username=username).first()
            if not user:
                ns_login.abort(400, "User with username provided doesn't exist")
            if check_valid_password(user.hashed_password, password):
                access_token = create_access_token(identity=user.username)
                return {
                    'message': 'Login successful', 
                    'access_token': access_token
                }
            ns_login.abort(400, "Invalid credentials")

    @ns_users.route('/')
    class UserList(Resource):
        @jwt_required()
        @ns_users.doc('list_users')
        @ns_users.marshal_list_with(user_output_schema)
        def get(self):
            """List all users"""
            return User.query.order_by(User.id).all()
        
        @jwt_required()
        @ns_users.doc('create_user')
        @ns_users.expect(user_input_schema)
        @ns_users.marshal_with(user_output_schema)
        def post(self):
            """Create a new user"""
            data = request.json
            if User.query.filter_by(username=data['username']).first() is not None:
                ns_users.abort(400, "Username already exists")
            if not Role.query.get(data['role_id']):
                ns_users.abort(400, "Role not found")
            new_user = User(
                username=data['username'], 
                hashed_password=hash_password(data['password']),
                role_id=data['role_id']
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        
    @ns_users.route('/<int:user_id>')
    @ns_users.response(404, 'User not found')
    @ns_users.param('user_id', 'The user identifier')
    class UserID(Resource):
        @jwt_required()
        @ns_users.doc('get_user')
        @ns_users.marshal_with(user_output_schema)
        def get(self, user_id):
            """Fetch a user given its identifier"""
            user = User.query.get(user_id)
            if not user:
                ns_users.abort(404, "User not found")
            return user

        @jwt_required()
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
            
        @jwt_required()
        @ns_users.doc('update_user')
        @ns_users.expect(user_input_schema)
        @ns_users.marshal_with(user_output_schema)
        def put(self, user_id):
            """Update a user given its identifier"""
            data = request.json
            user_to_update = User.query.get(user_id)
            if user_to_update:
                if User.query.filter_by(username=data['username']).first() and user_to_update.username != data['username']:
                    ns_users.abort(400, "Username already exists")
                user_to_update.username = data['username']
                user_to_update.hashed_password = hash_password(data['password'])
                user_to_update.role_id = data['role_id']
                db.session.commit()
                return user_to_update
            ns_users.abort(404, "User not found")

    # Routes for Role
    @ns_roles.route('/')
    class RoleList(Resource):
        @jwt_required()
        @ns_roles.doc('list_roles')
        @ns_roles.marshal_list_with(role_output_schema)
        def get(self):
            """List all roles"""
            return Role.query.order_by(Role.id).all()
    
        @jwt_required()
        @ns_roles.doc('create_person')
        @ns_roles.expect(role_input_schema)
        @ns_roles.marshal_with(role_output_schema)
        def post(self):
            """Create a new role"""
            data = request.json
            new_person = Role(name=data['name'])
            db.session.add(new_person)
            db.session.commit()
            return new_person
    
    @ns_roles.route('/<int:role_id>')
    @ns_roles.response(404, 'Role not found')
    @ns_roles.param('role_id', 'The role identifier')
    class RoleID(Resource):
        @jwt_required()
        @ns_roles.doc('get_role')
        @ns_roles.marshal_with(role_output_schema)
        def get(self, role_id):
            """Fetch a role given its identifier"""
            role = Role.query.get(role_id)
            if not role:
                ns_roles.abort(404, "Role not found")
            return role

        @jwt_required()
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

        @jwt_required()
        @ns_roles.doc('update_role')
        @ns_roles.expect(role_input_schema)
        @ns_roles.marshal_with(role_output_schema)
        def put(self, role_id):
            """Update a role given its identifier"""
            data = request.json
            role_to_update = Role.query.get(role_id)
            if role_to_update:
                role_to_update.name = data['name']
                db.session.commit()
                return role_to_update
            ns_roles.abort(404, "Role not found")

    # Routes for Log
    @ns_logs.route('/')
    class LogList(Resource):
        @jwt_required()
        @ns_logs.doc('list_logs')
        @ns_logs.marshal_list_with(log_output_schema)
        def get(self):
            """List all logs"""
            return Log.query.order_by(Log.id).all()
    
        @jwt_required()
        @ns_logs.doc('create_log')
        @ns_logs.expect(log_input_schema)
        @ns_logs.marshal_with(log_output_schema)
        def post(self):
            """Create a new log"""
            data = request.json
            user_id = data['user_id']
            action = data['action']
            timestamp = data['timestamp']

            if not User.query.get(user_id):
                ns_logs.abort(404, "User not found")
            
            new_log = Log(
                user_id=user_id, 
                action=action,
                timestamp=timestamp,
        )
            db.session.add(new_log)
            db.session.commit()
            return new_log
    
    @ns_logs.route('/<int:log_id>')
    @ns_logs.response(404, 'Log not found')
    @ns_logs.param('log_id', 'The log identifier')
    class LogID(Resource):
        @jwt_required()
        @ns_logs.doc('get_log')
        @ns_logs.marshal_with(log_output_schema)
        def get(self, log_id):
            """Fetch a log given its identifier"""
            log = Log.query.get(log_id)
            if not log:
                ns_logs.abort(404, "Log not found")
            return log

    # Routes for Access Control
    @ns_access_controls.route('/')
    class AccessControlList(Resource):
        @jwt_required()
        @ns_access_controls.doc('list_access_control')
        @ns_access_controls.marshal_list_with(access_control_output_schema)
        def get(self):
            """List all access controls"""
            return AccessControl.query.order_by(AccessControl.id).all()
    
        @jwt_required()
        @ns_access_controls.doc('create_access_control')
        @ns_access_controls.expect(access_control_input_schema)
        @ns_access_controls.marshal_with(access_control_output_schema)
        def post(self):
            """Create a new access control"""
            data = request.json
            role_id = data['role_id']
            resource = data['resource']
            read_permission = data['read_permission']
            write_permission = data['write_permission']

            if not Role.query.get(role_id):
                ns_access_controls.abort(404, "Role not found")
            
            new_access_control = AccessControl(
                role_id=role_id, 
                resource=resource,
                read_permission=read_permission,
                write_permission=write_permission
        )
            db.session.add(new_access_control)
            db.session.commit()
            return new_access_control
    
    @ns_access_controls.route('/<int:access_control_id>')
    @ns_access_controls.response(404, 'Access Control not found')
    @ns_access_controls.param('access_control_id', 'The access control identifier')
    class AccessControlID(Resource):
        @jwt_required()
        @ns_access_controls.doc('get_access_control')
        @ns_access_controls.marshal_with(access_control_output_schema)
        def get(self, access_control_id):
            """Fetch an access control given its identifier"""
            access_control = AccessControl.query.get(access_control_id)
            if not access_control:
                ns_access_controls.abort(404, "Access Control not found")
            return access_control

        @jwt_required()
        @ns_access_controls.doc('delete_access_control')
        @ns_access_controls.response(204, 'Access control deleted')
        def delete(self, access_control_id):
            """Delete an access control given its identifier"""
            access_control_to_delete = AccessControl.query.get(access_control_id)
            if not access_control_to_delete:
                ns_access_controls.abort(404, "Access control not found")
            db.session.delete(access_control_to_delete)
            db.session.commit()
            return f"Access control with ID {access_control_id} has been deleted.", 204

        @jwt_required()
        @ns_access_controls.doc('update_access_control')
        @ns_access_controls.expect(access_control_input_schema)
        @ns_access_controls.marshal_with(access_control_output_schema)
        def put(self, access_control_id):
            """Update an access control given its identifier"""
            data = request.json
            access_control_to_update = AccessControl.query.get(access_control_id)
            if access_control_to_update:
                access_control_to_update.role_id = data['role_id']
                access_control_to_update.resource = data['resource']
                access_control_to_update.read_permission = data['read_permission']
                access_control_to_update.write_permission = data['write_permission']
                db.session.commit()
                return access_control_to_update
            ns_access_controls.abort(404, "Access control not found")