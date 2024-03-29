from datetime import datetime

from app.main import db


class SensorReading(db.Model):
    """ SensorReading Model for storing sensor reading related details """
    __tablename__ = "sensor_reading"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id', ondelete="CASCADE"), nullable=False)
