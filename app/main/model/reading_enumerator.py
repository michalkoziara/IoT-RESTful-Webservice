from sqlalchemy import UniqueConstraint

from app.main import db


class ReadingEnumerator(db.Model):
    """ ReadingEnumerator Model for storing reading enumerator related details """
    __tablename__ = "reading_enumerator"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(255), nullable=False)

    sensor_type_id = db.Column(db.Integer, db.ForeignKey('sensor_type.id'), nullable=False)

    UniqueConstraint('sensor_type_id', 'number', name='unique_number_in_sensor_enumerator')
