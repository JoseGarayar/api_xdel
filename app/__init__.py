# Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
# App
from app.constants import (
    SECRET_KEY,
    JWT_SECRET_KEY,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB
)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* field below: 'Bearer <JWT>' where <JWT> is your token."
    }
}

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
api = Api(version='1.0', title='XDel API',
        description='API for XDel Singapore',
        authorizations=authorizations,
        security='Bearer Auth')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['ENV']='development'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    from .routes import register_routes
    register_routes(api)

    with app.app_context():
        db.create_all()

    return app