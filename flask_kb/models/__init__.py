from flask_kb import db, login_manager
from flask_kb.models.users import User


def initialize_db():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    cred = User.query.get(int(user_id))
    return cred
