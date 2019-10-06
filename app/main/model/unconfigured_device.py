from app.main import db


class UnconfiguredDevice(db.Model):
    """ UnconfiguredDevice Model for storing unconfigured device related details """
    __tablename__ = "unconfigured_device"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_key = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    device_group_id = db.Column(db.Integer, db.ForeignKey('device_group.id'), nullable=False)
