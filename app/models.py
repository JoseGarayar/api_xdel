from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    hashed_password = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)

class Person(db.Model):
    __tablename__ = "person"

    id_person = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    contact_level = db.Column(db.String(50))


class Invoice(db.Model):
    __tablename__ = "invoice"

    id_invoice = db.Column(db.Integer, primary_key=True)
    id_sender = db.Column(db.Integer, db.ForeignKey('person.id_person'))
    id_recipient = db.Column(db.Integer, db.ForeignKey('person.id_person'))
    id_product = db.Column(db.Integer, db.ForeignKey('product_service.id_product'))
    date = db.Column(db.Date)
    total_amount = db.Column(db.DECIMAL(10, 2))
    id_user = db.Column(db.Integer)
    sender = db.relationship("Person", foreign_keys=[id_sender])
    recipient = db.relationship("Person", foreign_keys=[id_recipient])


class InvoiceDetail(db.Model):
    __tablename__ = "invoice_detail"

    id_detail = db.Column(db.Integer, primary_key=True)
    id_invoice = db.Column(db.Integer, db.ForeignKey('invoice.id_invoice'))
    package_type = db.Column(db.String(50))
    dimensions = db.Column(db.String(255))
    weight = db.Column(db.DECIMAL(10, 2))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.DECIMAL(10, 2))
    subtotal = db.Column(db.DECIMAL(10, 2))


class ProductService(db.Model):
    __tablename__ = "product_service"

    id_product = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.DECIMAL(10, 2))


class Courier(db.Model):
    __tablename__ = "courier"

    id_courier = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))

class Role(db.Model):
    __tablename__ = "role"

    id_role = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255))
    description = db.Column(db.Text)


class Permission(db.Model):
    __tablename__ = "permission"

    id_permission = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(255))
    description = db.Column(db.Text)


class RolePermission(db.Model):
    __tablename__ = "role_permission"

    id_role = db.Column(db.Integer, db.ForeignKey('role.id_role'), primary_key=True)
    id_permission = db.Column(db.Integer, db.ForeignKey('permission.id_permission'), primary_key=True)


class UserRole(db.Model):
    __tablename__ = "user_role"

    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_role = db.Column(db.Integer, db.ForeignKey('role.id_role'), primary_key=True)


class Shipment(db.Model):
    __tablename__ = "shipment"

    id_shipment = db.Column(db.Integer, primary_key=True)
    id_invoice = db.Column(db.Integer, db.ForeignKey('invoice.id_invoice'))
    id_courier = db.Column(db.Integer, db.ForeignKey('courier.id_courier'))
    id_shipment_state = db.Column(db.Integer, db.ForeignKey('shipment_state.id_shipment_state'))
    creation_date = db.Column(db.Date)
    finish_date = db.Column(db.Date)


class ShipmentState(db.Model):
    __tablename__ = "shipment_state"

    id_shipment_state = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(255))