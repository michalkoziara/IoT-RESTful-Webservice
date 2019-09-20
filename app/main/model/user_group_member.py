from app.main import db


user_group_member = db.Table('user_group_member',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('user_group_id', db.Integer, db.ForeignKey('user_group.id'), primary_key=True)
)