from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    hashed_password = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True)

class Person(db.Model):
    __tablename__ = 'person'

    ID_Person = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    Contact_Level = db.Column(db.String(50))

class Invoice(db.Model):
    __tablename__ = 'invoice'

    ID_Invoice = db.Column(db.Integer, primary_key=True)
    Sender_ID = db.Column(db.Integer, db.ForeignKey('person.ID_Person'))
    Receiver_ID = db.Column(db.Integer, db.ForeignKey('person.ID_Person'))
    Product_ID = db.Column(db.Integer, db.ForeignKey('product_service.ID_Product'))
    Date = db.Column(db.Date)
    Total_Amount = db.Column(db.DECIMAL(10, 2))
    User_ID = db.Column(db.Integer, db.ForeignKey('user.ID_User'))

class Invoice_Detail(db.Model):
    __tablename__ = 'invoice_detail'

    ID_Detail = db.Column(db.Integer, primary_key=True)
    Invoice_ID = db.Column(db.Integer, db.ForeignKey('invoice.ID_Invoice'))
    Package_Type = db.Column(db.String(50))
    Dimensions = db.Column(db.String(255))
    Weight = db.Column(db.DECIMAL(10, 2))
    Quantity = db.Column(db.Integer)
    Unit_Price = db.Column(db.DECIMAL(10, 2))
    Subtotal = db.Column(db.DECIMAL(10, 2))

class Product_Service(db.Model):
    __tablename__ = 'product_service'

    ID_Product = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Description = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2))

class Courier(db.Model):
    __tablename__ = 'courier'

    ID_Courier = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Address = db.Column(db.String(255))

class User(db.Model):
    __tablename__ = 'user'

    ID_User = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255))
    Password = db.Column(db.String(255))

class Role(db.Model):
    __tablename__ = 'role'

    ID_Role = db.Column(db.Integer, primary_key=True)
    Role_Name = db.Column(db.String(255))
    Description = db.Column(db.Text)

class Permission(db.Model):
    __tablename__ = 'permission'

    ID_Permission = db.Column(db.Integer, primary_key=True)
    Permission_Name = db.Column(db.String(255))
    Description = db.Column(db.Text)

class Role_Permission(db.Model):
    __tablename__ = 'role_permission'

    ID_Role = db.Column(db.Integer, db.ForeignKey('role.ID_Role'), primary_key=True)
    ID_Permission = db.Column(db.Integer, db.ForeignKey('permission.ID_Permission'), primary_key=True)

class User_Role(db.Model):
    __tablename__ = 'user_role'

    ID_User = db.Column(db.Integer, db.ForeignKey('user.ID_User'), primary_key=True)
    ID_Role = db.Column(db.Integer, db.ForeignKey('role.ID_Role'), primary_key=True)

class Shipment(db.Model):
    __tablename__ = 'shipment'

    ID_Shipment = db.Column(db.Integer, primary_key=True)
    ID_Invoice = db.Column(db.Integer, db.ForeignKey('invoice.ID_Invoice'))
    ID_Courier = db.Column(db.Integer, db.ForeignKey('courier.ID_Courier'))
    ID_Shipment_State = db.Column(db.Integer, db.ForeignKey('shipment_state.ID_Shipment_State'))
    Creation_Date = db.Column(db.Date)
    Completion_Date = db.Column(db.Date)

class Shipment_State(db.Model):
    __tablename__ = 'shipment_state'
    
    ID_Shipment_State = db.Column(db.Integer, primary_key=True)
    State_Name = db.Column(db.String(255))
