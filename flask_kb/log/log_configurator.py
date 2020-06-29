'''
Log Configurator, inspired by https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
'''
import logging
import logging.config
import os
# from deprecated import deprecated
import warnings

import yaml


class LogConfigurator:

    """
    Class to configure the logging strategy.
    """

    """
    This method will try to configure the logging following this flow:
    If the LOG_CFG env variable is set to point to a
        config file in yml, that is used to configure the logging.
    If the LOG_CFG is not set, but a config file is passed directly
        in yml format, the config will be applied.
    If no file is provided, it tries to read a default config file in
    <PROJECT_FOLDER>/configs/logging.yml
    If the default logging config is not found,
        a default config is set, where the level is WARNING and no
            formatting is applied.
       :param default_path:
       :param default_level:
       :param env_key:
    """

    @staticmethod
    def setup_logging(
            default_path=os.path.join('config', 'logging.yml'),
            default_level=logging.DEBUG,
            env_key="LOG_CFG"):
        
        """Setup logging configuration """

        package_path = os.path.join(os.path.dirname(__file__), '..', 'configs/logging.yml')

        path = None
        # If a config file was set inside the Environment Variable LOG_CFG, that has precedence
        value = os.getenv(env_key, None)
        if value and os.path.exists(value):
            path = value
        elif os.path.exists(default_path):
            path = default_path
        elif os.path.exists(package_path):
            path = package_path

        if path is None:
            logging.warning("Log configuration file NOT found: " + ','.join(value, default_path, package_path))
            logging.basicConfig(level=default_level)
        else:
            logging.debug("Log configuration file found: " + path)
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)


class log_configurator:
    package_path = os.path.join(os.path.dirname(__file__), '..', 'config/logging.yml')

    '''
    Class to configure the logging strategy.
    '''

    def __init__(self):
        warnings.warn("Please use LogConfigurator class instead", DeprecationWarning)

    def setup_logging(
            self,
            default_path=os.path.join('config', 'logging.yml'),
            default_level=logging.WARNING,
            env_key="LOG_CFG"):
        '''
        This method will try to configure the logging following this flow:
        If the LOG_CFG env variable is set to point to a config file in yml, that is used to configure the logging.
        If the LOG_CFG is not set, but a config file is passed directly in yml format, the config will be applied.
        If no file is provided, it tries to read a default config file in <PROJECT_FOLDER>/config/default_logging_conf.yml
        If the default logging config is not found, a default config is set, where the level is WARNING and no formatting is applied. 
        :param default_path:
        :param default_level:
        :param env_key:
        '''

        """Setup logging configuration    
        """
        # If a config file was set inside the Environment Variable LOG_CFG, that has precedence
        value = os.getenv(env_key, None)
        if value and os.path.exists(value):
            path = value
        elif os.path.exists(default_path):
            path = default_path
        elif os.path.exists(self.package_path):
            path = self.package_path

        if path:
            logging.debug("Log configuration file found: " + path)
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        else:
            logging.warning("Log configuration file NOT found: " + ','.join(value, default_path, package_path))
            logging.basicConfig(level=default_level)
