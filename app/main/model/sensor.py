from sqlalchemy import UniqueConstraint

from app.main import db


class Sensor(db.Model):
    """ Sensor Model for storing sensor related details """
    __tablename__ = "sensor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    is_updated = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_assigned = db.Column(db.Boolean, nullable=False)
    device_key = db.Column(db.String(255), nullable=False, unique=True)

    sensor_type_id = db.Column(db.Integer, db.ForeignKey('sensor_type.id', ondelete="CASCADE"), nullable=False)
    user_group_id = db.Column(db.Integer, db.ForeignKey('user_group.id', ondelete="SET NULL"), nullable=True)
    device_group_id = db.Column(db.Integer, db.ForeignKey('device_group.id', ondelete="CASCADE"), nullable=False)

    sensor_readings = db.relationship('SensorReading', backref='sensor', lazy=True, passive_deletes=True)

    UniqueConstraint('device_group_id', 'name', name='unique_sensor_name_in_group')
