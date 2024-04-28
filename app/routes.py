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
from app import bcrypt



def register_routes(api):
    # Namespaces
    ns_test = api.namespace('', description='Endpoints for testing')
    ns_login = api.namespace('login', description='Endpoints for login')
    ns_users = api.namespace('users', description='Endpoints for users')

    # Routes
    @ns_test.route('/hello')
    class Hello(Resource):
        def get(self):
            return {'hello': 'world'}
        
    @ns_test.route('/protected')
    class Protected(Resource):
        @jwt_required()
        def get(self):
            current_user = get_jwt_identity()
            return {'logged_in_as': current_user}
    
    @ns_login.route('/')
    class Login(Resource):
        @ns_login.expect(login_schema)
        def post(self):
            data = request.json
            email = data.get('email')
            password = data.get('password')
            print(email)
            if not email or not password:
                ns_login.abort(400, 'Email and password are required')
            user = User.query.filter_by(email=email).first()
            if not user:
                ns_login.abort(400, "User with email provided doesn't exist")
            if bcrypt.check_password_hash(user.hashed_password, password):
                access_token = create_access_token(identity=user.email)
                return {
                    'message': 'Login successful', 
                    'access_token': access_token
                }
            else:
                return {'error': 'Invalid credentials'}

    @ns_users.route('/')
    class UserList(Resource):
        @ns_users.marshal_list_with(user_schema)
        def get(self):
            return User.query.all()
        
        @ns_users.expect(login_schema)
        @ns_users.marshal_with(user_schema)
        def post(self):
            data = request.json
            if not data or 'email' not in data or 'password' not in data:
                ns_users.abort(400, 'Please provide email and password')
            if User.query.filter_by(email=data['email']).first() is not None:
                ns_users.abort(400, 'Email already exists')
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            new_user = User(email=data['email'], hashed_password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        
        