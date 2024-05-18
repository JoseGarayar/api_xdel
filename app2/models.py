from __init__ import db

class Customer(db.Model):
    __tablename__ = "Customer"
    __table_args__ = {'schema': 'Client'}

    customer_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    type = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    company = db.Column(db.String)
    address = db.relationship("Address", back_populates = 'customer')


class Address(db.Model):
    __tablename__ = "Address"
    __table_args__ = {'schema': 'Client'}

    address_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Client.Customer.customer_id'), nullable = True)
    address = db.Column(db.String)
    suburb = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    customer = db.relationship("Customer", back_populates = 'address')