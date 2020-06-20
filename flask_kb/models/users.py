from flask_kb import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user = db.Column(db.String(50),
                     unique=True,
                     nullable=False)
    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(50),
                         nullable=False)
    created_ = db.Column(db.dateTime,
                         default=datetime.now())
    
    def __repr__(self):
        return f"User('{self.user}', '{self.email}', '{self.created_}')"