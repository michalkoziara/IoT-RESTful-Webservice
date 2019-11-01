from sqlalchemy import UniqueConstraint
from sqlalchemy.types import Enum

from app.main import db


class SensorType(db.Model):
    """ SensorType Model for storing sensor type related details """
    __tablename__ = "sensor_type"

    _types = ('Boolean', 'Enum', 'Decimal')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    reading_type = db.Column(Enum(*_types, name="reading_type"), nullable=False)
    range_min = db.Column(db.Float, nullable=False)
    range_max = db.Column(db.Float, nullable=False)

    device_group_id = db.Column(db.Integer, db.ForeignKey('device_group.id', ondelete="CASCADE"), nullable=False)

    sensors = db.relationship('Sensor', backref='sensor_type', lazy=True, passive_deletes=True)
    reading_enumerators = db.relationship('ReadingEnumerator', backref='sensor_type', lazy=True, passive_deletes=True)

    UniqueConstraint('device_group_id', 'name', name='unique_sensor_type_in_device_group')
