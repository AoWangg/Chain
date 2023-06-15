from flask_sqlalchemy import SQLAlchemy

from __init__ import app
db = SQLAlchemy(app)

'''----------------------------------------------原本-----------------------------------------------------'''
class Enterprise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")
    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")
    contract_addr = db.Column(db.String(1024), default="")
    license_addr = db.Column(db.String(1024), default="")
    
    evaluation_addr = db.Column(db.String(1024), default="")
    started_evaluation = db.Column(db.Boolean, default=False)

    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

    ent_name = db.Column(db.String(1024),default="")
    rep_name = db.Column(db.String(1024),default="")
    ent_addr = db.Column(db.String(1024),default="")
    ent_type = db.Column(db.String(1024),default="")
    ent_range = db.Column(db.String(1024),default="")
    
class Engineer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    eid = db.Column(db.String(1024), default="")
    field = db.Column(db.String(1024), default="")
    index = db.Column(db.String(1024), default="")
    agency = db.Column(db.Integer, db.ForeignKey('agency.id'))

class Agency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")
    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")
    contract_addr = db.Column(db.String(1024), default="")

    engineer_list_addr = db.Column(db.String(1024), default="")
    engineers = db.relationship('Engineer', backref='Agency', lazy=True)

    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

'''----------------------------------------------有用-----------------------------------------------------'''

class IPFSObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(1024), nullable = False)
    name = db.Column(db.String(1024), default="")
    secret = db.Column(db.String(1024), default="")
    idx = db.Column(db.Integer)
    audit = db.Column(db.Integer, db.ForeignKey('audit.id'))
    container = db.Column(db.Integer, db.ForeignKey('container.id'))
    consignee = db.Column(db.Integer, db.ForeignKey('consignee.id'))
    carrier = db.Column(db.Integer, db.ForeignKey('carrier.id'))
    warehouse = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    maritime = db.Column(db.Integer, db.ForeignKey('maritime.id'))
    emergency = db.Column(db.Integer, db.ForeignKey('emergency.id'))
    transport = db.Column(db.Integer, db.ForeignKey('transport.id'))
    police = db.Column(db.Integer, db.ForeignKey('police.id'))

class Audit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")
    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")
    files = db.relationship('IPFSObject', backref='Audit', lazy=True)

    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")

    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")

    files = db.relationship('IPFSObject', backref='Container', lazy=True)
    contract_addr = db.Column(db.String(1024), default="")
    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

    report_goods_info_addr = db.Column(db.String(1024), default="")

class Consignee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")

    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")

    files = db.relationship('IPFSObject', backref='Consignee', lazy=True)
    contract_addr = db.Column(db.String(1024), default="")
    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

class Carrier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")

    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")

    files = db.relationship('IPFSObject', backref='Carrier', lazy=True)
    contract_addr = db.Column(db.String(1024), default="")
    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")

    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")

    files = db.relationship('IPFSObject', backref='Warehouse', lazy=True)
    contract_addr = db.Column(db.String(1024), default="")
    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

class Maritime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")

    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")

    files = db.relationship('IPFSObject', backref='Maritime', lazy=True)
    contract_addr = db.Column(db.String(1024), default="")
    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

class Emergency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")

    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")

    files = db.relationship('IPFSObject', backref='Emergency', lazy=True)
    contract_addr = db.Column(db.String(1024), default="")
    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

class Transport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")

    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")

    files = db.relationship('IPFSObject', backref='Transport', lazy=True)
    contract_addr = db.Column(db.String(1024), default="")
    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")

class Police(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False, default="")

    account_pub = db.Column(db.String(1024), default="")
    account_priv = db.Column(db.String(1024), default="")
    account_addr = db.Column(db.String(1024), default="")

    files = db.relationship('IPFSObject', backref='Police', lazy=True)
    contract_addr = db.Column(db.String(1024), default="")
    envelope_pub = db.Column(db.String(2048), default="")
    envelope_priv = db.Column(db.String(2048), default="")


class Contracts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    addr = db.Column(db.String(1024), default="")

class Arbitrate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(1024), default="")

def count_numbers():
    container_count = Container.query.count()
    consignee_count = Consignee.query.count()
    carrier_count = Carrier.query.count()
    warehouse_count = Warehouse.query.count()
    maritime_count = Maritime.query.count()
    emergency_count = Emergency.query.count()
    transport_count = Transport.query.count()
    police_count = Police.query.count()

    # el = Enterprise.query.count()
    # al = Agency.query.count()
    # aal = Audit.query.count()
    # eel = Engineer.query.count()
    return (container_count, consignee_count, carrier_count, warehouse_count, maritime_count, emergency_count, transport_count, police_count)

if __name__ == "__main__":
    db.drop_all()
    db.create_all()