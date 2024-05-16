from __init__ import db


class Role(db.Model):
    __tablename__ = 'Role'
    __table_args__ = {'schema': 'Security'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship("User", back_populates="role")
    access_controls = db.relationship("AccessControl", back_populates="role")


class User(db.Model):
    __tablename__ = "User"
    __table_args__ = {'schema': 'Security'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, index=True)
    hashed_password = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('Security.Role.id'), nullable=False)
    role = db.relationship("Role", back_populates="users")
    logs = db.relationship("Log", back_populates="user")


class Log(db.Model):
    __tablename__ = 'Log'
    __table_args__ = {'schema': 'Security'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Security.User.id'), nullable=False)
    user = db.relationship("User", back_populates="logs")
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)


class AccessControl(db.Model):
    __tablename__ = 'AccessControl'
    __table_args__ = {'schema': 'Security'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('Security.Role.id'), nullable=False)
    role = db.relationship("Role", back_populates="access_controls")
    resource = db.Column(db.String(255), nullable=False)
    read_permission = db.Column(db.Boolean, nullable=False, default=False)
    write_permission = db.Column(db.Boolean, nullable=False, default=False)