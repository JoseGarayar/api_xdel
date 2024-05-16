# Flask
from flask import request
from flask_restx import Resource
# App
from models import *
from schemas import *


def register_routes(api):
    # Namespaces
    ns_test = api.namespace('', description='Endpoints for testing')

    # Routes
    @ns_test.route('/hello')
    class Hello(Resource):
        def get(self):
            """Return a simple message to any public requester."""
            return {'hello': 'world'}
