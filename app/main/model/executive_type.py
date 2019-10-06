from app.main import db

from sqlalchemy.types import Enum


class ExecutiveType(db.Model):
    """ ExecutiveType Model for storing executive type related details """
    __tablename__ = "executive_type"

    _types = ('Boolean', 'Enum', 'Decimal')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    state_type = db.Column(Enum(*_types, name="state_type"), nullable=False)
    state_range_min = db.Column(db.Float, nullable=False)
    state_range_max = db.Column(db.Float, nullable=False)

    device_group_id = db.Column(db.Integer, db.ForeignKey('device_group.id'), nullable=False)

    executive_devices = db.relationship('ExecutiveDevice', backref='executive_type', lazy=True)
    state_enumerators = db.relationship('StateEnumerator', backref='executive_type', lazy=True)
