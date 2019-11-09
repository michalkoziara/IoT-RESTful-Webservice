from app.main import db


class DeletedDevice(db.Model):
    """ DeletedDevice Model for storing deleted device related details """
    __tablename__ = "deleted_device"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_key = db.Column(db.String(255), nullable=False, unique=True)

    device_group_id = db.Column(db.Integer, db.ForeignKey('device_group.id', ondelete="CASCADE"), nullable=False)
