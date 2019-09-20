from app.main import db

from sqlalchemy.types import Enum


class Log(db.Model):
    """ Log Model for storing log related details """
    __tablename__ = "log"
    
    _types = ('Debug', 'Error', 'Info')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(Enum(*_types, name="log_type"), nullable=False)
    error_message = db.Column(db.String(255))
    stack_trace = db.Column(db.String(255))
    payload = db.Column(db.String(255))
    time = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, nullable=False)
    
    device_group_id = db.Column(db.Integer, db.ForeignKey('device_group.id'), nullable=False)