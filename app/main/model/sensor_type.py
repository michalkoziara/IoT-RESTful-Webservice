from app.main import db

from sqlalchemy.types import Enum


class SensorType(db.Model):
    """ SensorType Model for storing sensor type related details """
    __tablename__ = "sensor_type"

    _types = ('Boolean', 'Enum', 'Decimal')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    reading_type = db.Column(Enum(*_types, name="reading_type"), nullable=False)
    range_min = db.Column(db.Float, nullable=False)
    range_max = db.Column(db.Float, nullable=False)

    device_group_id = db.Column(db.Integer, db.ForeignKey('device_group.id'), nullable=False)

    sensors = db.relationship('Sensor', backref='sensor_type', lazy=True)
    enumerator_values = db.relationship('EnumeratorValue', backref='sensor_type', lazy=True)
    sensor_readings = db.relationship('SensorReading', backref='sensor_type', lazy=True)