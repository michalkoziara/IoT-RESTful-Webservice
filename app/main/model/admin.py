from app.main import db


class Admin(db.Model):
    """ Admin Model for storing admin related details """
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    device_group = db.relationship('DeviceGroup', backref='admin', lazy=True,
                                   uselist=False, passive_deletes=True)
