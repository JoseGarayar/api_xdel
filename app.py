from flask import Flask, jsonify, request, abort
from app.models import db, User

import os

app = Flask(__name__)


SECRET_KEY = os.environ.get("SECRET_KEY", None)
POSTGRES_USER = os.environ.get("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", None)
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", None)
POSTGRES_DB = os.environ.get("POSTGRES_DB", None)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['ENV']='development'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'email': user.email} for user in users])

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, description="Please provide email and password")

    if User.query.filter_by(email=data['email']).first() is not None:
        abort(400, description="Email already exists")

    fake_hashed_password = data['password'] + "notreallyhashed"

    new_user = User(email=data['email'], hashed_password=fake_hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'email': new_user.email}), 201


if __name__ == '__main__':
    app.run(port = 5000, debug=True, host='0.0.0.0')