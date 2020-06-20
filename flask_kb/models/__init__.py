from flask_kb import db


def initialize_db():
    db.create_all()
