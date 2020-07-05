"""
Flask Application
The application should be able to do the following
over HTTP Protocols namely `GET`, `POST`, `PUT` and `DELETE`:

    1. Get all the Knowledge Items
    2. Get a Knowledge Item based on UID
    3. Get a Knowledge Item based on a Row Value
    4. Insert Values
    5. Alter Values
    6. Delete Values
    
    
This file also holds the components which initializes Database table.
Configurations are handled by `load_configs.py` which seeks manual
inputs from `config.yaml`
"""
from flask_kb import flask_app as application
from flask_kb.log.log_configurator import LogConfigurator


if __name__ == '__main__':
    LogConfigurator.setup_logging()
    logger = LogConfigurator.get_logger(__name__)
    logger.info("Server Started")
    application.run(host='0.0.0.0', port=5000)
