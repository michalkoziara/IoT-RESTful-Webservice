from sqlalchemy import UniqueConstraint

from app.main import db


class StateEnumerator(db.Model):
    """ StateEnumerator Model for storing state enumerator related details """
    __tablename__ = "state_enumerator"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(255), nullable=False)

    executive_type_id = db.Column(db.Integer, db.ForeignKey('executive_type.id'), nullable=False)

    UniqueConstraint(executive_type_id, number)
