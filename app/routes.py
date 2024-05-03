# Flask
from flask import request
from flask_restx import Resource
from flask_jwt_extended import ( 
    create_access_token, 
    jwt_required, 
    get_jwt_identity
)
# App
from app.models import db, User
from app.schemas import (
    login_schema, 
    user_schema
)
from app.functions import (
    check_valid_password,
    hash_password
)



def register_routes(api):
    # Namespaces
    ns_test = api.namespace('', description='Endpoints for testing')
    ns_login = api.namespace('login', description='Endpoints for login')
    ns_users = api.namespace('users', description='User operations')

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