from __init__ import db

class Customer(db.Model):
    __tablename__ = "Customer"
    __table_args__ = {'schema': 'Client'}

    customer_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    type_id = db.Column(db.Integer)
    name = db.Column(db.String)
    company = db.Column(db.String)
    default_address_id = db.Column(db.Integer, db.ForeignKey('Client.Address.address_id'))
    default_address = db.relationship("Address", foreign_keys = [default_address_id])


class Address(db.Model):
    __tablename__ = "Address"
    __table_args__ = {'schema': 'Client'}

    address_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Client.Customer.customer_id'))
    address = db.Column(db.String)
    address_2 = db.Column(db.String)
    address_3 = db.Column(db.String)
    suburb = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    sms_enabled = db.Column(db.Boolean)
    vat_tax_id = db.Column(db.String)