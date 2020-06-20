from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configs.load_configs import CONN_STRING


flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = CONN_STRING
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(flask_app)


from flask_kb.models import initialize_db


initialize_db()


from flask_kb import routes
