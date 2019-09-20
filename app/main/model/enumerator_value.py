from app.main import db


class EnumeratorValue(db.Model):
    """ EnumeratorValue Model for storing enumarator value related details """
    __tablename__ = "enumerator_value"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(255), nullable=False)

    sensor_type_id = db.Column(db.Integer, db.ForeignKey('sensor_type.id'), nullable=False)
    executive_type_id = db.Column(db.Integer, db.ForeignKey('executive_type.id'), nullable=False)