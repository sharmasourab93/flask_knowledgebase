from flask_kb import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user = db.Column(db.String(50),
                     unique=True,
                     nullable=False)
    email = db.Column(db.String(50),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(100),
                         nullable=False)
    created_ = db.Column(db.DateTime,
                         default=datetime.now())
    
    def __repr__(self):
        return f"User('{self.user}', " \
               f"'{self.email}', " \
               f"'{self.created_}')"
