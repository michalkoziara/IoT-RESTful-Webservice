from sqlalchemy import UniqueConstraint

from app.main import db
from app.main.model.user_group_member import user_group_member


class UserGroup(db.Model):
    """ UserGroup Model for storing user group related details """
    __tablename__ = "user_group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    device_group_id = db.Column(db.Integer, db.ForeignKey('device_group.id', ondelete="CASCADE"), nullable=False)

    formulas = db.relationship('Formula', backref='user_group', lazy=True, passive_deletes=True)
    sensors = db.relationship('Sensor', backref='user_group', lazy=True, passive_deletes=True)
    executive_devices = db.relationship('ExecutiveDevice', backref='user_group', lazy=True, passive_deletes=True)

    users = db.relationship('User', secondary=user_group_member,
                            lazy='subquery', backref=db.backref('user_groups', lazy=True), passive_deletes=True)

    UniqueConstraint('device_group_id', 'name', name='unique_name_in_device_group')
