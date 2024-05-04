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

input_person_schema = api.model('Input_Person', {
    'name': fields.String(required=True, description='The person name'),
    'address': fields.String(required=True, description='The person address'),
    'contact_level': fields.String(description='The person contact level')
})

output_person_schema = api.model('Output_Person', {
    'id_person': fields.Integer(description='The person ID'),
    'name': fields.String(required=True, description='The person name'),
    'address': fields.String(required=True, description='The person address'),
    'contact_level': fields.String(description='The person contact level')
})

input_invoice_schema = api.model('Input_Invoice', {
    'id_sender': fields.Integer(description='The ID of the sender'),
    'id_recipient': fields.Integer(description='The ID of the recipient'),
    'id_product': fields.Integer(description='The ID of the product'),
    'date': fields.Date(description='The date of the invoice'),
    'total_amount': fields.Float(description='The total amount of the invoice'),
    'id_user': fields.Integer(description='The ID of the user'),
})

output_invoice_schema = api.model('Output_Invoice', {
    'id_invoice': fields.Integer(description='The invoice ID'),
    'id_sender': fields.Integer(description='The ID of the sender'),
    'id_recipient': fields.Integer(description='The ID of the recipient'),
    'id_product': fields.Integer(description='The ID of the product'),
    'date': fields.Date(description='The date of the invoice'),
    'total_amount': fields.Float(description='The total amount of the invoice'),
    'id_user': fields.Integer(description='The ID of the user'),
})

invoice_detail_schema = api.model('InvoiceDetail', {
    'id_detail': fields.Integer(description='The invoice detail ID'),
    'id_invoice': fields.Integer(description='The ID of the invoice'),
    'package_type': fields.String(description='The package type'),
    'dimensions': fields.String(description='The dimensions of the package'),
    'weight': fields.Float(description='The weight of the package'),
    'quantity': fields.Integer(description='The quantity of items'),
    'unit_price': fields.Float(description='The unit price of the item'),
    'subtotal': fields.Float(description='The subtotal of the invoice detail'),
})

product_service_schema = api.model('ProductService', {
    'id_product': fields.Integer(description='The product/service ID'),
    'name': fields.String(required=True, description='The name of the product/service'),
    'description': fields.String(description='The description of the product/service'),
    'price': fields.Float(description='The price of the product/service'),
})

courier_schema = api.model('Courier', {
    'id_courier': fields.Integer(description='The courier ID'),
    'name': fields.String(required=True, description='The name of the courier'),
    'address': fields.String(description='The address of the courier'),
})

role_schema = api.model('Role', {
    'id_role': fields.Integer(description='The role ID'),
    'role_name': fields.String(required=True, description='The name of the role'),
    'description': fields.String(description='The description of the role'),
})

permission_schema = api.model('Permission', {
    'id_permission': fields.Integer(description='The permission ID'),
    'permission_name': fields.String(required=True, description='The name of the permission'),
    'description': fields.String(description='The description of the permission'),
})

role_permission_schema = api.model('RolePermission', {
    'id_role': fields.Integer(description='The role ID'),
    'id_permission': fields.Integer(description='The permission ID'),
})

user_role_schema = api.model('UserRole', {
    'id_user': fields.Integer(description='The user ID'),
    'id_role': fields.Integer(description='The role ID'),
})

shipment_schema = api.model('Shipment', {
    'id_shipment': fields.Integer(description='The shipment ID'),
    'id_invoice': fields.Integer(description='The ID of the invoice'),
    'id_courier': fields.Integer(description='The ID of the courier'),
    'id_shipment_state': fields.Integer(description='The ID of the shipment state'),
    'creation_date': fields.Date(description='The creation date of the shipment'),
    'finish_date': fields.Date(description='The finish date of the shipment'),
})

shipment_state_schema = api.model('ShipmentState', {
    'id_shipment_state': fields.Integer(description='The shipment state ID'),
    'state_name': fields.String(required=True, description='The name of the shipment state'),
})