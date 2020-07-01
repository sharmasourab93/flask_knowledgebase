from flask_kb import db, login_manager
from flask_kb.models.users import User
from flask_kb.models.dict_table import Dictionary
from log.log_configurator import LogConfigurator


LogConfigurator.setup_logging()
logger = LogConfigurator.get_logger(__name__)
logger.info("At Model Initialization")


def initialize_db():
    logger.info("Initializing Databases: {0} & {1}"
                .format(User.__name__, Dictionary.__name__))
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    cred = User.query.get(int(user_id))
    logger.info("Loading Users")
    return cred
