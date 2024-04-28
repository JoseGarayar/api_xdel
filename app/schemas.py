from flask_restx import fields
from app import api

login_schema = api.model('Login', {
    'email': fields.String(required=True, description='The user email address'),
    'password': fields.String(required=True, description='The user email address')
})

user_schema = api.model('User', {
    'id': fields.Integer(description='The user ID'),
    'email': fields.String(required=True, description='The user email address'),
    'hashed_password': fields.String(required=True, description='The user email address'),
    'is_active': fields.Boolean(description='Indicates whether user exists')
})