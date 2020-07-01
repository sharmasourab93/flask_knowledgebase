from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from configs.load_configs import CONN_STRING
from log.log_configurator import LogConfigurator


LogConfigurator.setup_logging()
logger = LogConfigurator.get_logger(__name__)
logger.info("Initializing Flask-kb")


flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = CONN_STRING
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.secret_key = 'basicsecret'
db = SQLAlchemy(flask_app)

bcrypt = Bcrypt(flask_app)

login_manager = LoginManager(flask_app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from flask_kb.models import initialize_db


initialize_db()


from flask_kb import routes
