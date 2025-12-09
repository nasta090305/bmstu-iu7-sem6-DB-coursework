import sys
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from safrs import SAFRSBase, SafrsApi

db = SQLAlchemy()

assignment_table = db.Table(
    'assignment',
    db.Column('equipment_id', db.BigInteger, db.ForeignKey('equipments.equipment_id'), primary_key=True),
    db.Column('employee_id', db.BigInteger, db.ForeignKey('employees.employee_id'), primary_key=True)
)

class ComponentType(SAFRSBase, db.Model):
    __tablename__ = 'component_types'
    component_type_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String)
    service_life = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    components = db.relationship('Component', backref='component_type', lazy=True)

class EquipmentType(SAFRSBase, db.Model):
    __tablename__ = 'equipment_types'
    equipment_type_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String)
    service_life = db.Column(db.Integer)

    equipments = db.relationship('Equipment', backref='equipment_type', lazy=True)

class Equipment(SAFRSBase, db.Model):
    __tablename__ = 'equipments'
    equipment_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    equipment_type_id = db.Column(db.BigInteger, db.ForeignKey('equipment_types.equipment_type_id'), nullable=False)
    commissioning_date = db.Column(db.Date)
    status = db.Column(db.String)

    components = db.relationship('Component', backref='equipment', lazy=True)
    sensors = db.relationship('Sensor', backref='equipment', lazy=True)
    maintenance_records = db.relationship('MaintenanceJournal', backref='equipment', lazy=True)
    employees = db.relationship('Employee', secondary=assignment_table, backref=db.backref('equipments', lazy=True))

class Component(SAFRSBase, db.Model):
    __tablename__ = 'components'
    component_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    component_type_id = db.Column(db.BigInteger, db.ForeignKey('component_types.component_type_id'), nullable=False)
    equipment_id = db.Column(db.BigInteger, db.ForeignKey('equipments.equipment_id'), nullable=True)
    commissioning_date = db.Column(db.Date)
    status = db.Column(db.String)

class Role(SAFRSBase, db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    employees = db.relationship('Employee', backref='role', lazy=True)

class Employee(SAFRSBase, db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    job_title = db.Column(db.String)
    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.role_id'))

    maintenance = db.relationship('MaintenanceJournal', backref='employee', lazy=True)

class MaintenanceJournal(SAFRSBase, db.Model):
    __tablename__ = 'maintenance_journal'
    maintenance_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    equipment_id = db.Column(db.BigInteger, db.ForeignKey('equipments.equipment_id'), nullable=False)
    employee_id = db.Column(db.BigInteger, db.ForeignKey('employees.employee_id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    comment = db.Column(db.String)

class Sensor(SAFRSBase, db.Model):
    __tablename__ = 'sensors'
    sensor_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    equipment_id = db.Column(db.BigInteger, db.ForeignKey('equipments.equipment_id'), nullable=False)
    lower_limit = db.Column(db.Float)
    upper_limit = db.Column(db.Float)

    readings = db.relationship('SensorReading', backref='sensor', lazy=True)

class SensorReading(SAFRSBase, db.Model):
    __tablename__ = 'sensor_readings'
    sensor_id = db.Column(db.BigInteger, db.ForeignKey('sensors.sensor_id'), primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)
    value = db.Column(db.Float, nullable=False)
    measurement_unit = db.Column(db.String, nullable=False)


def create_api(app, host="localhost", port=5000, api_prefix="/api"):
    api = SafrsApi(app, host=host, port=port, prefix=api_prefix)
    for cls in (ComponentType, Component, EquipmentType, Equipment,
                Role, Employee, MaintenanceJournal, Sensor, SensorReading):
        api.expose_object(cls)
    print(f"Created API: http://{host}:{port}{api_prefix}")
    print(f"Swagger UI available at: http://{host}:{port}{api_prefix}/")

def create_app(db_uri=None, host="127.0.0.1"):
    app = Flask("tractor_factory")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri or "postgresql://postgres:Postgres@localhost:5432/tractor_factory"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_api(app, host=host)
    return app

if __name__ == "__main__":
    host = sys.argv[1] if sys.argv[1:] else "127.0.0.1"
    app = create_app(host=host)
    app.run(host=host, debug=True)
