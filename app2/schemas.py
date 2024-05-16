from flask_restx import fields
from __init__ import api

input_customer_schema = api.model('Input_Customer', {
    'type_id': fields.Integer(description='The type ID of the customer'),
    'name': fields.String(required=True, description='The name of the customer'),
    'email': fields.String(required=True, description='The email of the customer'),
    'company': fields.String(description='The company of the customer'),
})

output_customer_schema = api.model('Output_Customer', {
    'customer_id': fields.Integer(description='The customer ID'),
    'type_id': fields.Integer(description='The type ID of the customer'),
    'name': fields.String(required=True, description='The name of the customer'),
    'email': fields.String(required=True, description='The email of the customer'),
    'company': fields.String(description='The company of the customer')
})

input_address_schema = api.model('Input_Address', {
    'customer_id': fields.Integer(description='The customer ID associated with the address'),
    'address': fields.String(description='The address'),
    'address_2': fields.String(description='The second address line'),
    'address_3': fields.String(description='The third address line'),
    'suburb': fields.String(description='The suburb'),
    'city': fields.String(description='The city'),
    'state': fields.String(description='The state'),
    'country': fields.String(description='The country')
})

output_address_schema = api.model('Output_Address', {
    'address_id': fields.Integer(description='The address ID'),
    'customer_id': fields.Integer(description='The customer ID associated with the address'),
    'address': fields.String(description='The address'),
    'address_2': fields.String(description='The second address line'),
    'address_3': fields.String(description='The third address line'),
    'suburb': fields.String(description='The suburb'),
    'city': fields.String(description='The city'),
    'state': fields.String(description='The state'),
    'country': fields.String(description='The country')
})