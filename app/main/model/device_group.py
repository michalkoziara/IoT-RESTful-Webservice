from app.main import db


class DeviceGroup(db.Model):
    """ DeviceGroup Model for storing device group related details """
    __tablename__ = "device_group"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    product_key = db.Column(db.String(255), nullable=False, unique=True)

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id', ondelete="CASCADE"), nullable=True)

    executive_devices = db.relationship('ExecutiveDevice', backref='device_group', lazy=True, passive_deletes=True)
    executive_types = db.relationship('ExecutiveType', backref='device_group', lazy=True, passive_deletes=True)
    sensors = db.relationship('Sensor', backref='device_group', lazy=True, passive_deletes=True)
    sensor_types = db.relationship('SensorType', backref='device_group', lazy=True, passive_deletes=True)
    unconfigured_devices = db.relationship('UnconfiguredDevice', backref='device_group', lazy=True,
                                           passive_deletes=True)
    user_groups = db.relationship('UserGroup', backref='device_group', lazy=True, passive_deletes=True)
    logs = db.relationship('Log', backref='device_group', lazy=True, passive_deletes=True)
