# Flask
from flask import Flask, jsonify, request, abort
from flask_jwt_extended import (
    JWTManager, 
    create_access_token, 
    jwt_required, 
    get_jwt_identity
)
from flask_bcrypt import Bcrypt
# App
from app.models import db, User
from app.constants import (
    SECRET_KEY,
    JWT_SECRET_KEY,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB
)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['ENV']='development'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User with email provided doesn't exists"}), 400
    if bcrypt.check_password_hash(user.hashed_password, password):
        access_token = create_access_token(identity=user.email)
        return jsonify({
            'message': 'Login successful', 
            'access_token': access_token
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


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
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], hashed_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'email': new_user.email}), 201


if __name__ == '__main__':
    app.run(port = 5000, debug=True, host='0.0.0.0')