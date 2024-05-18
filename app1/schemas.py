from flask_restx import fields
from __init__ import api



log_input_schema = api.model('LogInput', {
    'user_id': fields.Integer(required=True, description='User ID'),
    'action': fields.String(required=True, description='Action'),
    'timestamp': fields.DateTime(required=True, description='Timestamp')
})

log_output_schema = api.model('LogOutput', {
    'id': fields.Integer(required=True, description='Log ID'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'action': fields.String(required=True, description='Action'),
    'timestamp': fields.DateTime(required=True, description='Timestamp')
})

access_control_input_schema = api.model('AccessControlInput', {
    'role_id': fields.Integer(required=True, description='Role ID'),
    'resource': fields.String(required=True, description='Resource'),
    'read_permission': fields.Boolean(required=True, description='Read Permission'),
    'write_permission': fields.Boolean(required=True, description='Write Permission')
})

access_control_output_schema = api.model('AccessControlOutput', {
    'id': fields.Integer(required=True, description='Access Control ID'),
    'role_id': fields.Integer(required=True, description='Role ID'),
    'resource': fields.String(required=True, description='Resource'),
    'read_permission': fields.Boolean(required=True, description='Read Permission'),
    'write_permission': fields.Boolean(required=True, description='Write Permission')
})

role_input_schema = api.model('RoleInput', {
    'name': fields.String(required=True, description='Role Name')
})

role_output_schema = api.model('RoleOutput', {
    'id': fields.Integer(required=True, description='Role ID'),
    'name': fields.String(required=True, description='Role Name'),
    'access_controls': fields.List(fields.Nested(access_control_output_schema))
})

login_schema = api.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

user_input_schema = api.model('UserInput', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'role_id': fields.Integer(required=True, description='Role ID')
})

user_output_schema = api.model('UserOutput', {
    'id': fields.Integer(description='The user ID'),
    'username': fields.String(required=True, description='Username'),
    'hashed_password': fields.String(required=True, description='Password'),
    'role_id': fields.Integer(required=True, description='Role ID'),
    'role': fields.List(fields.Nested(role_output_schema))
})