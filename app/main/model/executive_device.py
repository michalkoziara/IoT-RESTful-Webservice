from sqlalchemy import UniqueConstraint

from app.main import db


class ExecutiveDevice(db.Model):
    """ ExecutiveDevice Model for storing executive device related details """
    __tablename__ = "executive_device"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    is_updated = db.Column(db.Boolean, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    is_assigned = db.Column(db.Boolean, nullable=False)
    is_formula_used = db.Column(db.Boolean, nullable=False)
    positive_state = db.Column(db.String(255))
    negative_state = db.Column(db.String(255))
    device_key = db.Column(db.String(255), nullable=False, unique=True)

    executive_type_id = db.Column(db.Integer, db.ForeignKey('executive_type.id'), nullable=False)
    device_group_id = db.Column(db.Integer, db.ForeignKey('device_group.id'), nullable=False)
    user_group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'), nullable=True)
    formula_id = db.Column(db.Integer, db.ForeignKey('formula.id'), nullable=True)

    UniqueConstraint(device_group_id, name)
