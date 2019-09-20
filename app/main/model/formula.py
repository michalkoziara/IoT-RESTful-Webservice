from app.main import db


class Formula(db.Model):
    """ Formula Model for storing formula related details """
    __tablename__ = "formula"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    rule = db.Column(db.String(255), nullable=False)

    user_group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'), nullable=False)
    
    executive_devices = db.relationship('ExecutiveDevice', backref='formula', lazy=True)